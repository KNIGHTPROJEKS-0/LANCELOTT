#!/usr/bin/env python3
"""
LANCELOTT Vanguard Manager
Obfuscation and Security Tools Integration
"""

import asyncio
import json
import logging
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ObfuscationType(Enum):
    """Types of obfuscation supported"""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    BINARY = "binary"
    NETWORK = "network"
    SHELLCODE = "shellcode"


@dataclass
class ObfuscationRequest:
    """Request for obfuscation operation"""

    tool: str
    target_file: str
    obfuscation_type: ObfuscationType
    options: Dict[str, Any]
    output_path: Optional[str] = None


@dataclass
class ObfuscationResult:
    """Result of obfuscation operation"""

    success: bool
    output_file: Optional[str]
    tool_used: str
    obfuscation_type: str
    protection_level: str
    size_change: Optional[float]
    execution_time: float
    warnings: List[str]
    error_message: Optional[str] = None


class VanguardManager:
    """Manager for Vanguard obfuscation and security tools"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.vanguard_path = self.project_root / "tools" / "security" / "vanguard"
        self.logger = self._setup_logging()
        self.tools_config = self._load_tools_config()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for Vanguard manager"""
        return logging.getLogger(__name__)

    def _load_tools_config(self) -> Dict[str, Dict[str, Any]]:
        """Load configuration for all Vanguard tools"""
        return {
            # Python obfuscation tools
            "pyarmor": {
                "name": "PyArmor",
                "type": ObfuscationType.PYTHON,
                "path": self.vanguard_path / "pyarmor",
                "command": ["python", "pyarmor.py"],
                "supported_extensions": [".py"],
                "protection_level": "high",
                "description": "Professional Python obfuscation and protection",
                "build_required": False,
            },
            "de4py": {
                "name": "de4py",
                "type": ObfuscationType.PYTHON,
                "path": self.vanguard_path / "de4py",
                "command": ["python", "main.py"],
                "supported_extensions": [".py"],
                "protection_level": "medium",
                "description": "Python deobfuscation and analysis tool",
                "build_required": False,
            },
            # JavaScript obfuscation tools
            "javascript-obfuscator": {
                "name": "JavaScript Obfuscator",
                "type": ObfuscationType.JAVASCRIPT,
                "path": self.vanguard_path / "javascript-obfuscator",
                "command": ["node", "index.cli.ts"],
                "supported_extensions": [".js", ".ts", ".jsx", ".tsx"],
                "protection_level": "high",
                "description": "Advanced JavaScript obfuscation",
                "build_required": True,
            },
            # Java obfuscation tools
            "skidfuscator": {
                "name": "Skidfuscator",
                "type": ObfuscationType.JAVA,
                "path": self.vanguard_path / "skidfuscator-java-obfuscator",
                "command": ["java", "-jar", "skidfuscator.jar"],
                "supported_extensions": [".jar", ".class"],
                "protection_level": "high",
                "description": "Advanced Java obfuscation framework",
                "build_required": True,
            },
            # Binary/Shellcode obfuscation tools
            "boaz": {
                "name": "BOAZ",
                "type": ObfuscationType.SHELLCODE,
                "path": self.vanguard_path / "BOAZ",
                "command": ["python", "Boaz.py"],
                "supported_extensions": [".exe", ".dll", ".bin"],
                "protection_level": "very_high",
                "description": "Advanced shellcode and binary obfuscation",
                "build_required": False,
            },
            "hyperion": {
                "name": "Hyperion",
                "type": ObfuscationType.BINARY,
                "path": self.vanguard_path / "Hyperion",
                "command": ["python", "hyperion.py"],
                "supported_extensions": [".exe", ".bin"],
                "protection_level": "high",
                "description": "Binary encryption and obfuscation",
                "build_required": False,
            },
            # Network obfuscation tools
            "utls": {
                "name": "uTLS",
                "type": ObfuscationType.NETWORK,
                "path": self.vanguard_path / "utls",
                "command": ["go", "build"],
                "supported_extensions": [".go"],
                "protection_level": "high",
                "description": "TLS fingerprint obfuscation",
                "build_required": True,
            },
            "fake-http": {
                "name": "FakeHTTP",
                "type": ObfuscationType.NETWORK,
                "path": self.vanguard_path / "FakeHTTP",
                "command": ["make"],
                "supported_extensions": [".c", ".h"],
                "protection_level": "medium",
                "description": "HTTP protocol obfuscation",
                "build_required": True,
            },
            # Binary analysis and obfuscation
            "bitmono": {
                "name": "BitMono",
                "type": ObfuscationType.BINARY,
                "path": self.vanguard_path / "BitMono",
                "command": ["dotnet", "run"],
                "supported_extensions": [".exe", ".dll"],
                "protection_level": "medium",
                "description": ".NET binary obfuscation and analysis",
                "build_required": True,
            },
        }

    async def list_available_tools(self) -> List[Dict[str, Any]]:
        """List all available Vanguard obfuscation tools"""
        tools = []
        for tool_id, config in self.tools_config.items():
            tool_info = {
                "id": tool_id,
                "name": config["name"],
                "type": config["type"].value,
                "protection_level": config["protection_level"],
                "description": config["description"],
                "supported_extensions": config["supported_extensions"],
                "available": config["path"].exists(),
                "build_required": config["build_required"],
            }
            tools.append(tool_info)
        return tools

    async def get_tool_info(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific tool"""
        if tool_id not in self.tools_config:
            return None

        config = self.tools_config[tool_id]
        return {
            "id": tool_id,
            "name": config["name"],
            "type": config["type"].value,
            "path": str(config["path"]),
            "protection_level": config["protection_level"],
            "description": config["description"],
            "supported_extensions": config["supported_extensions"],
            "available": config["path"].exists(),
            "build_required": config["build_required"],
            "command": config["command"],
        }

    async def build_tool(self, tool_id: str) -> bool:
        """Build a Vanguard tool if required"""
        if tool_id not in self.tools_config:
            raise ValueError(f"Unknown tool: {tool_id}")

        config = self.tools_config[tool_id]
        if not config["build_required"]:
            self.logger.info(f"Tool {tool_id} does not require building")
            return True

        try:
            self.logger.info(f"Building Vanguard tool: {tool_id}")
            tool_path = config["path"]

            if tool_id == "javascript-obfuscator":
                # Build JavaScript obfuscator
                process = await asyncio.create_subprocess_exec(
                    "npm",
                    "install",
                    cwd=tool_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await process.communicate()

                if process.returncode != 0:
                    self.logger.error(
                        f"Failed to install dependencies for {tool_id}: {stderr.decode()}"
                    )
                    return False

                process = await asyncio.create_subprocess_exec(
                    "npm",
                    "run",
                    "build",
                    cwd=tool_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await process.communicate()

                if process.returncode != 0:
                    self.logger.error(f"Failed to build {tool_id}: {stderr.decode()}")
                    return False

            elif tool_id == "skidfuscator":
                # Build Java obfuscator
                process = await asyncio.create_subprocess_exec(
                    "./gradlew",
                    "build",
                    cwd=tool_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await process.communicate()

                if process.returncode != 0:
                    self.logger.error(f"Failed to build {tool_id}: {stderr.decode()}")
                    return False

            elif tool_id == "utls":
                # Build Go TLS library
                process = await asyncio.create_subprocess_exec(
                    "go",
                    "mod",
                    "tidy",
                    cwd=tool_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await process.communicate()

                process = await asyncio.create_subprocess_exec(
                    "go",
                    "build",
                    ".",
                    cwd=tool_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await process.communicate()

                if process.returncode != 0:
                    self.logger.error(f"Failed to build {tool_id}: {stderr.decode()}")
                    return False

            elif tool_id == "fake-http":
                # Build C HTTP obfuscator
                process = await asyncio.create_subprocess_exec(
                    "make",
                    cwd=tool_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await process.communicate()

                if process.returncode != 0:
                    self.logger.error(f"Failed to build {tool_id}: {stderr.decode()}")
                    return False

            elif tool_id == "bitmono":
                # Build .NET tool
                process = await asyncio.create_subprocess_exec(
                    "dotnet",
                    "build",
                    cwd=tool_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await process.communicate()

                if process.returncode != 0:
                    self.logger.error(f"Failed to build {tool_id}: {stderr.decode()}")
                    return False

            self.logger.info(f"Successfully built {tool_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to build {tool_id}: {e}")
            return False

    async def obfuscate_file(self, request: ObfuscationRequest) -> ObfuscationResult:
        """Obfuscate a file using the specified Vanguard tool"""
        start_time = asyncio.get_event_loop().time()

        try:
            if request.tool not in self.tools_config:
                return ObfuscationResult(
                    success=False,
                    output_file=None,
                    tool_used=request.tool,
                    obfuscation_type=request.obfuscation_type.value,
                    protection_level="none",
                    size_change=None,
                    execution_time=0,
                    warnings=[],
                    error_message=f"Unknown tool: {request.tool}",
                )

            config = self.tools_config[request.tool]
            tool_path = config["path"]

            # Check if file exists
            target_file = Path(request.target_file)
            if not target_file.exists():
                return ObfuscationResult(
                    success=False,
                    output_file=None,
                    tool_used=request.tool,
                    obfuscation_type=request.obfuscation_type.value,
                    protection_level="none",
                    size_change=None,
                    execution_time=0,
                    warnings=[],
                    error_message=f"Target file not found: {request.target_file}",
                )

            # Check file extension
            file_ext = target_file.suffix
            if file_ext not in config["supported_extensions"]:
                return ObfuscationResult(
                    success=False,
                    output_file=None,
                    tool_used=request.tool,
                    obfuscation_type=request.obfuscation_type.value,
                    protection_level="none",
                    size_change=None,
                    execution_time=0,
                    warnings=[],
                    error_message=f"Unsupported file extension: {file_ext}",
                )

            # Build tool if required
            if config["build_required"]:
                build_success = await self.build_tool(request.tool)
                if not build_success:
                    return ObfuscationResult(
                        success=False,
                        output_file=None,
                        tool_used=request.tool,
                        obfuscation_type=request.obfuscation_type.value,
                        protection_level="none",
                        size_change=None,
                        execution_time=0,
                        warnings=[],
                        error_message=f"Failed to build tool: {request.tool}",
                    )

            # Prepare output path
            output_path = request.output_path
            if not output_path:
                output_path = str(
                    target_file.parent
                    / f"{target_file.stem}_obfuscated{target_file.suffix}"
                )

            # Execute obfuscation
            result = await self._execute_obfuscation(
                request.tool, str(target_file), output_path, request.options
            )

            end_time = asyncio.get_event_loop().time()
            execution_time = end_time - start_time

            # Calculate size change if output file exists
            size_change = None
            if result.success and Path(output_path).exists():
                original_size = target_file.stat().st_size
                obfuscated_size = Path(output_path).stat().st_size
                size_change = (obfuscated_size - original_size) / original_size * 100

            return ObfuscationResult(
                success=result.success,
                output_file=output_path if result.success else None,
                tool_used=request.tool,
                obfuscation_type=request.obfuscation_type.value,
                protection_level=config["protection_level"],
                size_change=size_change,
                execution_time=execution_time,
                warnings=result.warnings,
                error_message=result.error_message,
            )

        except Exception as e:
            end_time = asyncio.get_event_loop().time()
            execution_time = end_time - start_time

            return ObfuscationResult(
                success=False,
                output_file=None,
                tool_used=request.tool,
                obfuscation_type=request.obfuscation_type.value,
                protection_level="none",
                size_change=None,
                execution_time=execution_time,
                warnings=[],
                error_message=str(e),
            )

    async def _execute_obfuscation(
        self, tool_id: str, input_file: str, output_file: str, options: Dict[str, Any]
    ) -> "ExecutionResult":
        """Execute the obfuscation command for a specific tool"""
        config = self.tools_config[tool_id]
        tool_path = config["path"]
        warnings = []

        try:
            if tool_id == "pyarmor":
                # PyArmor obfuscation
                cmd = [
                    "python",
                    "pyarmor.py",
                    "obfuscate",
                    "--output",
                    str(Path(output_file).parent),
                    input_file,
                ]

                # Add options
                if options.get("advanced", False):
                    cmd.extend(["--advanced", "2"])
                if options.get("restrict", True):
                    cmd.append("--restrict")

            elif tool_id == "javascript-obfuscator":
                # JavaScript obfuscator
                cmd = ["node", "index.cli.ts", input_file, "--output", output_file]

                # Add options
                if options.get("compact", True):
                    cmd.append("--compact")
                if options.get("controlFlowFlattening", True):
                    cmd.append("--control-flow-flattening")
                if options.get("stringArray", True):
                    cmd.append("--string-array")

            elif tool_id == "boaz":
                # BOAZ shellcode obfuscation
                cmd = [
                    "python",
                    "Boaz.py",
                    "--input",
                    input_file,
                    "--output",
                    output_file,
                ]

                # Add encryption options
                if options.get("encryption", "aes"):
                    cmd.extend(["--encryption", options["encryption"]])

            else:
                # Generic command construction
                cmd = config["command"].copy()
                cmd.extend([input_file, output_file])

            # Execute the command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=tool_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            # Check for warnings in output
            output_text = stdout.decode() + stderr.decode()
            if "warning" in output_text.lower():
                warnings.append("Tool generated warnings during obfuscation")

            success = process.returncode == 0 and Path(output_file).exists()

            return ExecutionResult(
                success=success,
                warnings=warnings,
                error_message=stderr.decode() if not success else None,
            )

        except Exception as e:
            return ExecutionResult(
                success=False, warnings=warnings, error_message=str(e)
            )

    async def get_protection_recommendations(
        self, file_path: str
    ) -> List[Dict[str, Any]]:
        """Get protection recommendations for a file"""
        file_ext = Path(file_path).suffix.lower()
        recommendations = []

        for tool_id, config in self.tools_config.items():
            if file_ext in config["supported_extensions"]:
                recommendations.append(
                    {
                        "tool": tool_id,
                        "name": config["name"],
                        "protection_level": config["protection_level"],
                        "description": config["description"],
                        "confidence": self._calculate_confidence(file_ext, config),
                    }
                )

        # Sort by protection level and confidence
        protection_levels = {"very_high": 4, "high": 3, "medium": 2, "low": 1}
        recommendations.sort(
            key=lambda x: (
                protection_levels.get(x["protection_level"], 0),
                x["confidence"],
            ),
            reverse=True,
        )

        return recommendations

    def _calculate_confidence(self, file_ext: str, config: Dict[str, Any]) -> float:
        """Calculate confidence score for tool recommendation"""
        # Base confidence on extension match and tool characteristics
        confidence = 0.7

        if file_ext in config["supported_extensions"]:
            confidence += 0.2

        if config["protection_level"] in ["high", "very_high"]:
            confidence += 0.1

        return min(confidence, 1.0)

    def get_status(self) -> Dict[str, Any]:
        """Get Vanguard manager status"""
        available_tools = sum(
            1 for config in self.tools_config.values() if config["path"].exists()
        )
        total_tools = len(self.tools_config)

        return {
            "vanguard_path": str(self.vanguard_path),
            "total_tools": total_tools,
            "available_tools": available_tools,
            "tools_by_type": {
                obf_type.value: sum(
                    1
                    for config in self.tools_config.values()
                    if config["type"] == obf_type and config["path"].exists()
                )
                for obf_type in ObfuscationType
            },
        }


@dataclass
class ExecutionResult:
    """Result of tool execution"""

    success: bool
    warnings: List[str]
    error_message: Optional[str] = None


# Global Vanguard manager instance
_vanguard_manager = None


def get_vanguard_manager() -> VanguardManager:
    """Get global Vanguard manager instance"""
    global _vanguard_manager
    if _vanguard_manager is None:
        _vanguard_manager = VanguardManager()
    return _vanguard_manager
