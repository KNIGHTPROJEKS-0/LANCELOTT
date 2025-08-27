#!/usr/bin/env python3
"""
Crush CLI File Manager Integration Wrapper
Terminal file manager and tool orchestrator with CliWrap integration
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.integration_manager import BaseToolWrapper


class CrushWrapper(BaseToolWrapper):
    """Wrapper for Crush CLI file manager - the main tool orchestrator with CliWrap integration"""

    def __init__(self):
        # Create a ToolConfig for Crush
        from integrations.integration_manager import ToolConfig

        config = ToolConfig(
            name="Crush",
            executable_path="tools/crush/crush",
            wrapper_module="integrations.tools.crush_wrapper",
            port=8000,
        )
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self._cliwrap_wrapper = None

        # Legacy attributes for backward compatibility
        self.executable_path = Path(config.executable_path)
        self.config_file = "config/crush.conf"
        self.description = (
            "Terminal file manager and tool orchestrator with CliWrap integration"
        )
        self.category = "Orchestration"
        self.name = config.name
        self.port = config.port

    async def initialize(self) -> bool:
        """Initialize Crush CLI tool"""
        try:
            # Check if executable exists
            if not self.executable_path.exists():
                self.logger.error(
                    f"Crush executable not found at {self.executable_path}"
                )
                return False

            # Test basic execution
            result = await self.health_check()
            if result:
                self.logger.info("Crush initialized successfully")
                return True
            else:
                self.logger.error("Crush initialization failed")
                return False

        except Exception as e:
            self.logger.error(f"Crush initialization error: {e}")
            return False

    async def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute a command using Crush"""
        try:
            # For Crush, the command is typically a target path or operation
            target = kwargs.get("target", command)
            options = kwargs.get("options", {})

            result = await self.execute_scan(target, options)
            return result

        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def health_check(self) -> bool:
        """Check if Crush is healthy and responsive"""
        try:
            # Check if binary exists
            if not self.executable_path.exists():
                return False

            # Try to get version (basic health check)
            cmd = [str(self.executable_path), "--version"]
            try:
                await self._execute_command(cmd, timeout=10)
                return True
            except:
                # If version fails, try basic execution
                return self.executable_path.exists()

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

    @property
    def cliwrap_wrapper(self):
        """Lazy load CliWrap wrapper to avoid circular imports"""
        if self._cliwrap_wrapper is None:
            try:
                from integrations.tools.cliwrap_wrapper import get_cliwrap_wrapper

                self._cliwrap_wrapper = get_cliwrap_wrapper()
            except ImportError as e:
                self.logger.warning(f"CliWrap wrapper not available: {e}")
                self._cliwrap_wrapper = None
        return self._cliwrap_wrapper

    async def execute_scan(
        self, target: str, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute file management operations"""
        if options is None:
            options = {}

        try:
            # Build command based on operation type
            operation = options.get("operation", "browse")

            if operation == "browse":
                cmd = [str(self.executable_path)]
                if target:
                    cmd.append(target)
            elif operation == "script":
                # Execute a script file
                script_path = options.get("script_path")
                cmd = [str(self.executable_path), "--script", script_path]
            elif operation == "command":
                # Execute specific command
                command = options.get("command")
                cmd = [str(self.executable_path), "--exec", command]
            else:
                cmd = [str(self.executable_path)]

            # Execute command
            result = await self._execute_command(cmd, timeout=300)

            return {
                "success": True,
                "tool": self.name,
                "operation": operation,
                "target": target,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Crush execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": self.name,
                "target": target,
                "timestamp": self._get_timestamp(),
            }

    async def orchestrate_tools(
        self, tools: List[str], target: str, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Orchestrate multiple security tools"""
        if options is None:
            options = {}

        try:
            results = {}
            execution_plan = []

            # Create execution plan
            for tool in tools:
                tool_config = {
                    "name": tool,
                    "target": target,
                    "status": "pending",
                    "depends_on": options.get(f"{tool}_depends_on", []),
                }
                execution_plan.append(tool_config)

            # Execute tools based on dependencies
            for tool_config in execution_plan:
                tool_name = tool_config["name"]

                # Check dependencies
                dependencies_met = True
                for dep in tool_config["depends_on"]:
                    if dep not in results or not results[dep].get("success", False):
                        dependencies_met = False
                        break

                if not dependencies_met:
                    tool_config["status"] = "skipped"
                    results[tool_name] = {
                        "success": False,
                        "error": "Dependencies not met",
                        "tool": tool_name,
                    }
                    continue

                # Execute tool
                tool_result = await self._execute_tool(
                    tool_name, target, options.get(f"{tool_name}_options", {})
                )
                results[tool_name] = tool_result
                tool_config["status"] = (
                    "completed" if tool_result.get("success") else "failed"
                )

            return {
                "success": True,
                "orchestrator": self.name,
                "tools": tools,
                "target": target,
                "execution_plan": execution_plan,
                "results": results,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Tool orchestration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "orchestrator": self.name,
                "timestamp": self._get_timestamp(),
            }

    async def execute_with_cliwrap(
        self, command: str, arguments: List[str] = None, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute command using CliWrap for enhanced process management"""
        if arguments is None:
            arguments = []
        if options is None:
            options = {}

        try:
            if self.cliwrap_wrapper:
                # Use CliWrap for enhanced command execution
                result = await self.cliwrap_wrapper.wrap_command(
                    command, arguments, options
                )
                return {
                    "success": result.get("success", False),
                    "method": "cliwrap",
                    "command": command,
                    "arguments": arguments,
                    "output": result.get("execution_output", ""),
                    "cliwrap_details": result,
                    "timestamp": self._get_timestamp(),
                }
            else:
                # Fallback to direct execution
                cmd = [command] + arguments
                result = await self._execute_command(
                    cmd, timeout=options.get("timeout", 300)
                )
                return {
                    "success": True,
                    "method": "direct",
                    "command": command,
                    "arguments": arguments,
                    "output": result,
                    "timestamp": self._get_timestamp(),
                }

        except Exception as e:
            self.logger.error(f"CliWrap enhanced execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "command": command,
                "timestamp": self._get_timestamp(),
            }

    async def orchestrate_with_cliwrap(
        self, tools: List[str], target: str, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Enhanced orchestration using CliWrap for better process management"""
        if options is None:
            options = {}

        try:
            results = {}
            execution_plan = []

            # Enhanced tool commands with CliWrap support
            enhanced_tool_commands = {
                "nmap": {
                    "command": "nmap",
                    "args": ["-sV", "-sC", target],
                    "timeout": 300,
                },
                "feroxbuster": {
                    "command": "feroxbuster",
                    "args": ["-u", target],
                    "timeout": 600,
                },
                "intel-scan": {
                    "command": "python3",
                    "args": ["tools/Intel-Scan/intel-scan.py", "-t", target],
                    "timeout": 300,
                },
                "argus": {
                    "command": "python3",
                    "args": ["tools/Argus/argus.py", target],
                    "timeout": 600,
                },
                "sherlock": {
                    "command": "python3",
                    "args": ["tools/SHERLOCK/sherlock.py", target],
                    "timeout": 300,
                },
            }

            # Create enhanced execution plan
            for tool in tools:
                if tool in enhanced_tool_commands:
                    tool_config = enhanced_tool_commands[tool]
                    execution_plan.append(
                        {
                            "name": tool,
                            "command": tool_config["command"],
                            "args": tool_config["args"],
                            "timeout": tool_config["timeout"],
                            "status": "pending",
                        }
                    )

            # Execute tools using CliWrap
            for tool_plan in execution_plan:
                tool_name = tool_plan["name"]
                self.logger.info(f"Executing {tool_name} via CliWrap orchestration")

                result = await self.execute_with_cliwrap(
                    tool_plan["command"],
                    tool_plan["args"],
                    {"timeout": tool_plan["timeout"]},
                )

                results[tool_name] = result
                tool_plan["status"] = "completed" if result.get("success") else "failed"

            return {
                "success": True,
                "orchestrator": f"{self.name} + CliWrap",
                "tools": tools,
                "target": target,
                "execution_plan": execution_plan,
                "results": results,
                "enhancement": "CliWrap process management enabled",
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Enhanced CliWrap orchestration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "orchestrator": f"{self.name} + CliWrap",
                "timestamp": self._get_timestamp(),
            }

    async def _execute_tool(
        self, tool_name: str, target: str, options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a specific security tool"""
        try:
            # Map tool names to their execution commands
            tool_commands = {
                "nmap": ["nmap", "-sV", "-sC", target],
                "feroxbuster": ["feroxbuster", "-u", target],
                "intel-scan": [
                    "python3",
                    "tools/Intel-Scan/intel-scan.py",
                    "-t",
                    target,
                ],
                "redeye": ["node", "tools/RedEye/dist/index.js", "analyze", target],
                "mhddos": ["python3", "tools/MHDDoS/start.py", target],
                "argus": ["python3", "tools/Argus/argus.py", target],
                "sherlock": ["python3", "tools/SHERLOCK/sherlock.py", target],
                "web-check": ["npm", "run", "scan", "--", target],
            }

            if tool_name not in tool_commands:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}",
                    "tool": tool_name,
                }

            cmd = tool_commands[tool_name]

            # Add additional options
            if options.get("verbose"):
                cmd.append("-v")
            if options.get("output_file"):
                cmd.extend(["-o", options["output_file"]])

            # Execute the tool
            result = await self._execute_command(cmd, timeout=600)

            return {
                "success": True,
                "tool": tool_name,
                "target": target,
                "output": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name,
                "timestamp": self._get_timestamp(),
            }

    async def create_workflow(
        self, workflow_name: str, tools: List[str], target: str
    ) -> Dict[str, Any]:
        """Create a security testing workflow"""
        try:
            workflow = {
                "name": workflow_name,
                "target": target,
                "tools": tools,
                "created": self._get_timestamp(),
                "status": "created",
            }

            # Save workflow to file
            workflow_path = Path("workflows") / f"{workflow_name}.json"
            workflow_path.parent.mkdir(exist_ok=True)

            with open(workflow_path, "w") as f:
                json.dump(workflow, f, indent=2)

            return {
                "success": True,
                "workflow": workflow,
                "path": str(workflow_path),
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Workflow creation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def execute_workflow(self, workflow_path: str) -> Dict[str, Any]:
        """Execute a saved workflow"""
        try:
            # Load workflow
            with open(workflow_path, "r") as f:
                workflow = json.load(f)

            # Execute orchestration
            result = await self.orchestrate_tools(
                workflow["tools"],
                workflow["target"],
                {"workflow_name": workflow["name"]},
            )

            return result

        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    def parse_results(self, output: str) -> Dict[str, Any]:
        """Parse Crush output"""
        try:
            lines = output.strip().split("\n")

            return {
                "lines": lines,
                "total_lines": len(lines),
                "summary": f"Crush output with {len(lines)} lines",
                "raw_output": output,
            }

        except Exception as e:
            return {
                "error": f"Failed to parse Crush output: {e}",
                "raw_output": output,
            }

    async def check_dependencies(self) -> Dict[str, Any]:
        """Check Crush dependencies"""
        try:
            # Check if crush binary exists
            binary_exists = Path(self.executable_path).exists()

            # Try to get version
            version_result = None
            if binary_exists:
                try:
                    version_result = subprocess.run(
                        [str(self.executable_path), "--version"],
                        capture_output=True,
                        text=True,
                        timeout=10,
                    )
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    version_result = None

            dependencies = {
                "binary": {
                    "available": binary_exists,
                    "path": str(self.executable_path),
                },
                "version": {
                    "available": version_result is not None
                    and version_result.returncode == 0,
                    "info": (
                        version_result.stdout.strip()
                        if version_result and version_result.returncode == 0
                        else None
                    ),
                },
            }

            all_available = binary_exists

            return {
                "success": all_available,
                "dependencies": dependencies,
                "message": (
                    "All dependencies available"
                    if all_available
                    else "Dependencies missing"
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
_crush_wrapper = None


def get_crush_wrapper() -> CrushWrapper:
    """Get global Crush wrapper instance"""
    global _crush_wrapper
    if _crush_wrapper is None:
        _crush_wrapper = CrushWrapper()
    return _crush_wrapper
