#!/usr/bin/env python3
"""
CliWrap Integration Wrapper
.NET library for wrapping command line processes
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.integration_manager import BaseToolWrapper


class CliWrapWrapper(BaseToolWrapper):
    """Wrapper for CliWrap .NET command line process wrapper"""

    def __init__(self):
        # Create a ToolConfig for CliWrap
        from integrations.integration_manager import ToolConfig

        config = ToolConfig(
            name="CliWrap",
            executable_path="tools/CliWrap",
            wrapper_module="integrations.tools.cliwrap_wrapper",
            port=8001,
        )
        super().__init__(config)
        self.logger = logging.getLogger(__name__)

        # Legacy attributes for backward compatibility
        self.executable_path = Path(config.executable_path)
        self.config_file = "config/cliwrap.conf"
        self.description = ".NET library for wrapping command line processes"
        self.category = "Utilities"
        self.name = config.name
        self.port = config.port

    async def initialize(self) -> bool:
        """Initialize CliWrap tool"""
        try:
            # Check if project directory exists
            if not self.executable_path.exists():
                self.logger.error(
                    f"CliWrap directory not found at {self.executable_path}"
                )
                return False

            # Check .NET SDK availability
            deps = await self.check_dependencies()
            if deps["success"]:
                self.logger.info("CliWrap initialized successfully")
                return True
            else:
                self.logger.error(
                    "CliWrap initialization failed - missing dependencies"
                )
                return False

        except Exception as e:
            self.logger.error(f"CliWrap initialization error: {e}")
            return False

    async def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute a command using CliWrap"""
        try:
            arguments = kwargs.get("arguments", [])
            options = kwargs.get("options", {})

            result = await self.wrap_command(command, arguments, options)
            return result

        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def health_check(self) -> bool:
        """Check if CliWrap is healthy and responsive"""
        try:
            # Check if project directory exists
            if not self.executable_path.exists():
                return False

            # Check .NET SDK availability
            deps = await self.check_dependencies()
            return deps["success"]

        except Exception as e:
            self.logger.warning(f"Health check failed: {e}")
            return False

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime

        return datetime.now().isoformat()

    async def _execute_command(
        self, cmd: List[str], timeout: int = 300, work_dir: Path = None
    ) -> str:
        """Execute a command and return output"""
        try:
            if work_dir:
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(work_dir),
                )
            else:
                process = await asyncio.create_subprocess_exec(
                    *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )

            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(
                    f"Command failed with return code {process.returncode}: {error_msg}"
                )

            return stdout.decode()

        except asyncio.TimeoutError:
            if process:
                process.kill()
                await process.wait()
            raise Exception(f"Command timed out after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Command execution failed: {e}")

    async def execute_scan(
        self, target: str, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute command wrapping operations"""
        if options is None:
            options = {}

        try:
            # Build command
            operation = options.get("operation", "build")

            if operation == "build":
                cmd = ["dotnet", "build"]
                work_dir = Path(self.executable_path)
            elif operation == "test":
                cmd = ["dotnet", "test"]
                work_dir = Path(self.executable_path)
            elif operation == "run":
                cmd = ["dotnet", "run"]
                work_dir = Path(self.executable_path)
                if target:
                    cmd.extend(["--", target])
            else:
                cmd = ["dotnet", "build"]
                work_dir = Path(self.executable_path)

            # Execute command
            result = await self._execute_command(cmd, work_dir)

            return {
                "success": True,
                "tool": self.name,
                "operation": operation,
                "target": target,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"CliWrap execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": self.name,
                "target": target,
                "timestamp": self._get_timestamp(),
            }

    async def wrap_command(
        self, command: str, arguments: List[str] = None, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Wrap a command using CliWrap functionality"""
        if arguments is None:
            arguments = []
        if options is None:
            options = {}

        try:
            # Create a temporary C# script that uses CliWrap
            script_content = f"""
using System;
using System.Threading.Tasks;
using CliWrap;

class Program
{{
    static async Task Main(string[] args)
    {{
        var result = await Cli.Wrap("{command}")
            .WithArguments({json.dumps(arguments)})
            .WithValidation(CommandResultValidation.None)
            .ExecuteAsync();

        Console.WriteLine($"Exit Code: {{result.ExitCode}}");
        Console.WriteLine($"Start Time: {{result.StartTime}}");
        Console.WriteLine($"Exit Time: {{result.ExitTime}}");
        Console.WriteLine($"Run Time: {{result.RunTime}}");
    }}
}}
"""

            # Save the script
            script_path = Path("/tmp/cliwrap_script.cs")
            with open(script_path, "w") as f:
                f.write(script_content)

            # Create a temporary project
            project_dir = Path("/tmp/cliwrap_temp")
            project_dir.mkdir(exist_ok=True)

            # Create project file
            project_content = """
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net6.0</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="CliWrap" Version="3.6.6" />
  </ItemGroup>
</Project>
"""

            with open(project_dir / "temp.csproj", "w") as f:
                f.write(project_content)

            # Copy script to project
            with open(project_dir / "Program.cs", "w") as f:
                f.write(script_content)

            # Build and run
            build_result = await self._execute_command(
                ["dotnet", "build"], work_dir=project_dir
            )

            if "Build FAILED" in build_result:
                raise Exception(f"Build failed: {build_result}")

            run_result = await self._execute_command(
                ["dotnet", "run"],
                work_dir=project_dir,
                timeout=options.get("timeout", 30),
            )

            return {
                "success": True,
                "tool": self.name,
                "command": command,
                "arguments": arguments,
                "build_output": build_result,
                "execution_output": run_result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Command wrapping failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "command": command,
                "timestamp": self._get_timestamp(),
            }

    async def execute_batch_commands(
        self, commands: List[Dict[str, Any]], options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute multiple commands using CliWrap"""
        if options is None:
            options = {}

        try:
            results = []

            for i, cmd_config in enumerate(commands):
                command = cmd_config.get("command")
                arguments = cmd_config.get("arguments", [])
                cmd_options = cmd_config.get("options", {})

                self.logger.info(f"Executing command {i+1}/{len(commands)}: {command}")

                result = await self.wrap_command(command, arguments, cmd_options)
                results.append({"index": i, "command": command, "result": result})

            return {
                "success": True,
                "tool": self.name,
                "total_commands": len(commands),
                "results": results,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Batch command execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    def parse_results(self, output: str) -> Dict[str, Any]:
        """Parse CliWrap output"""
        try:
            lines = output.strip().split("\n")

            # Parse exit code if present
            exit_code = None
            start_time = None
            exit_time = None
            run_time = None

            for line in lines:
                if line.startswith("Exit Code:"):
                    exit_code = line.split(":")[1].strip()
                elif line.startswith("Start Time:"):
                    start_time = line.split(":", 1)[1].strip()
                elif line.startswith("Exit Time:"):
                    exit_time = line.split(":", 1)[1].strip()
                elif line.startswith("Run Time:"):
                    run_time = line.split(":", 1)[1].strip()

            return {
                "lines": lines,
                "total_lines": len(lines),
                "exit_code": exit_code,
                "start_time": start_time,
                "exit_time": exit_time,
                "run_time": run_time,
                "raw_output": output,
            }

        except Exception as e:
            return {
                "error": f"Failed to parse CliWrap output: {e}",
                "raw_output": output,
            }

    async def check_dependencies(self) -> Dict[str, Any]:
        """Check CliWrap dependencies"""
        try:
            # Check .NET SDK
            dotnet_result = subprocess.run(
                ["dotnet", "--version"], capture_output=True, text=True
            )

            # Check if CliWrap directory exists
            cliwrap_exists = Path(self.executable_path).exists()

            dependencies = {
                "dotnet": {
                    "available": dotnet_result.returncode == 0,
                    "version": (
                        dotnet_result.stdout.strip()
                        if dotnet_result.returncode == 0
                        else None
                    ),
                },
                "cliwrap_source": {
                    "available": cliwrap_exists,
                    "path": str(self.executable_path),
                },
            }

            all_available = all(dep["available"] for dep in dependencies.values())

            return {
                "success": all_available,
                "dependencies": dependencies,
                "message": (
                    "All dependencies available"
                    if all_available
                    else "Missing dependencies"
                ),
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }


# Global wrapper instance
_cliwrap_wrapper = None


def get_cliwrap_wrapper() -> CliWrapWrapper:
    """Get global CliWrap wrapper instance"""
    global _cliwrap_wrapper
    if _cliwrap_wrapper is None:
        _cliwrap_wrapper = CliWrapWrapper()
    return _cliwrap_wrapper
