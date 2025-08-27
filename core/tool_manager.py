"""
Tool Manager for CERBERUS-FANGS LANCELOTT
Manages all security tools and their execution
"""

import asyncio
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import settings
from core.logger_config import get_tool_logger


class ToolStatus(str, Enum):
    """Tool status enumeration"""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    RUNNING = "running"
    ERROR = "error"


class ToolManager:
    """Manages all security tools"""

    def __init__(self):
        self.tools = {}
        self.running_processes = {}
        self.logger = get_tool_logger("tool_manager")

    async def initialize(self):
        """Initialize all tools and check their availability"""
        self.logger.info("Initializing tool manager...")

        tools_config = {
            "nmap": {
                "path": settings.NMAP_PATH,
                "check_command": ["nmap", "--version"],
                "description": "Network discovery and security auditing",
                "category": "network_scanning",
            },
            "argus": {
                "path": settings.ARGUS_PATH,
                "check_command": ["python3", "argus.py", "--help"],
                "description": "Network monitoring and flow analysis",
                "category": "network_monitoring",
            },
            "kraken": {
                "path": settings.KRAKEN_PATH,
                "check_command": ["python3", "kraken.py", "--help"],
                "description": "Multi-tool security framework",
                "category": "multi_tool",
            },
            "metabigor": {
                "path": settings.METABIGOR_PATH,
                "check_command": ["./metabigor", "--help"],
                "description": "Intelligence gathering and OSINT",
                "category": "osint",
            },
            "dismap": {
                "path": settings.DISMAP_PATH,
                "check_command": ["./dismap", "--help"],
                "description": "Asset discovery and mapping",
                "category": "asset_discovery",
            },
            "osmedeus": {
                "path": settings.OSMEDEUS_PATH,
                "check_command": ["osmedeus", "--help"],
                "description": "Automated reconnaissance framework",
                "category": "reconnaissance",
            },
            "spiderfoot": {
                "path": settings.SPIDERFOOT_PATH,
                "check_command": ["python3", "sf.py", "--help"],
                "description": "Open source intelligence automation",
                "category": "osint",
            },
            "social_analyzer": {
                "path": settings.SOCIAL_ANALYZER_PATH,
                "check_command": ["python3", "analyzer.py", "--help"],
                "description": "Social media analysis and profiling",
                "category": "social_engineering",
            },
            "storm_breaker": {
                "path": settings.STORM_BREAKER_PATH,
                "check_command": ["python3", "st.py", "--help"],
                "description": "Social engineering and OSINT tool",
                "category": "social_engineering",
            },
            "phonesploit": {
                "path": settings.PHONESPLOIT_PATH,
                "check_command": ["python3", "main.py", "--help"],
                "description": "Android device exploitation",
                "category": "mobile_security",
            },
            "vajra": {
                "path": settings.VAJRA_PATH,
                "check_command": ["python3", "vajra.py", "--help"],
                "description": "User interface testing and automation",
                "category": "ui_testing",
            },
            "redteam_toolkit": {
                "path": settings.REDTEAM_TOOLKIT_PATH,
                "check_command": ["ls"],
                "description": "Comprehensive red team utilities",
                "category": "red_team",
            },
        }

        for tool_name, config in tools_config.items():
            status = await self._check_tool_availability(tool_name, config)
            self.tools[tool_name] = {
                **config,
                "status": status,
                "last_checked": datetime.utcnow().isoformat(),
            }

        self.logger.info(f"Initialized {len(self.tools)} tools")

    async def _check_tool_availability(
        self, tool_name: str, config: Dict
    ) -> ToolStatus:
        """Check if a tool is available and working"""
        try:
            tool_path = Path(config["path"])

            # Check if path exists
            if not tool_path.exists():
                self.logger.warning(f"Tool path not found: {tool_path}")
                return ToolStatus.UNAVAILABLE

            # Try to run the check command
            if "check_command" in config:
                process = await asyncio.create_subprocess_exec(
                    *config["check_command"],
                    cwd=str(tool_path) if tool_path.is_dir() else str(tool_path.parent),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(), timeout=10
                    )
                    if process.returncode == 0 or process.returncode is None:
                        self.logger.info(f"Tool {tool_name} is available")
                        return ToolStatus.AVAILABLE
                    else:
                        self.logger.warning(
                            f"Tool {tool_name} check failed with return code {process.returncode}"
                        )
                        return ToolStatus.ERROR
                except asyncio.TimeoutError:
                    self.logger.warning(f"Tool {tool_name} check timed out")
                    process.kill()
                    return ToolStatus.ERROR

            return ToolStatus.AVAILABLE

        except Exception as e:
            self.logger.error(f"Error checking tool {tool_name}: {str(e)}")
            return ToolStatus.ERROR

    async def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        return [
            name
            for name, config in self.tools.items()
            if config["status"] == ToolStatus.AVAILABLE
        ]

    async def get_tool_status(self, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """Get status of tools"""
        if tool_name:
            return self.tools.get(tool_name, {})
        return self.tools

    async def execute_tool(
        self, tool_name: str, command: List[str], **kwargs
    ) -> Dict[str, Any]:
        """Execute a tool with given command"""
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        tool_config = self.tools[tool_name]
        if tool_config["status"] != ToolStatus.AVAILABLE:
            raise ValueError(f"Tool {tool_name} is not available")

        # Mark tool as running
        self.tools[tool_name]["status"] = ToolStatus.RUNNING

        try:
            # Prepare execution environment
            tool_path = Path(tool_config["path"])
            working_dir = (
                str(tool_path) if tool_path.is_dir() else str(tool_path.parent)
            )

            # Execute command
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=working_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=os.environ.copy(),
            )

            # Store process for potential cancellation
            process_id = f"{tool_name}_{datetime.utcnow().timestamp()}"
            self.running_processes[process_id] = process

            # Wait for completion or timeout
            timeout = kwargs.get("timeout", settings.SCAN_TIMEOUT)
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )

                result = {
                    "success": True,
                    "return_code": process.returncode,
                    "stdout": stdout.decode("utf-8", errors="ignore"),
                    "stderr": stderr.decode("utf-8", errors="ignore"),
                    "process_id": process_id,
                    "tool": tool_name,
                    "command": command,
                    "timestamp": datetime.utcnow().isoformat(),
                }

                self.logger.info(f"Tool {tool_name} execution completed successfully")
                return result

            except asyncio.TimeoutError:
                self.logger.warning(f"Tool {tool_name} execution timed out")
                process.kill()
                return {
                    "success": False,
                    "error": "Execution timed out",
                    "process_id": process_id,
                    "tool": tool_name,
                    "command": command,
                    "timestamp": datetime.utcnow().isoformat(),
                }

        except Exception as e:
            self.logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name,
                "command": command,
                "timestamp": datetime.utcnow().isoformat(),
            }

        finally:
            # Reset tool status
            self.tools[tool_name]["status"] = ToolStatus.AVAILABLE
            # Clean up process reference
            if process_id in self.running_processes:
                del self.running_processes[process_id]

    async def cancel_execution(self, process_id: str) -> bool:
        """Cancel a running tool execution"""
        if process_id in self.running_processes:
            process = self.running_processes[process_id]
            try:
                process.terminate()
                await asyncio.sleep(5)  # Give it time to terminate gracefully
                if process.returncode is None:
                    process.kill()  # Force kill if still running
                del self.running_processes[process_id]
                self.logger.info(f"Process {process_id} cancelled successfully")
                return True
            except Exception as e:
                self.logger.error(f"Error cancelling process {process_id}: {str(e)}")
                return False
        return False

    async def get_running_processes(self) -> Dict[str, Any]:
        """Get list of currently running processes"""
        return {
            pid: {
                "tool": pid.split("_")[0],
                "start_time": pid.split("_")[1],
                "status": "running" if process.returncode is None else "completed",
            }
            for pid, process in self.running_processes.items()
        }

    async def cleanup(self):
        """Cleanup all running processes"""
        self.logger.info("Cleaning up tool manager...")

        for process_id in list(self.running_processes.keys()):
            await self.cancel_execution(process_id)

        self.logger.info("Tool manager cleanup completed")
