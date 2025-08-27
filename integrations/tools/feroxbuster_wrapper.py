#!/usr/bin/env python3
"""
Feroxbuster Tool Integration Wrapper
Fast Content Discovery Tool
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.base_tool_wrapper import BaseToolWrapper


class FeroxbusterWrapper(BaseToolWrapper):
    """Wrapper for Feroxbuster content discovery tool"""

    def __init__(self):
        super().__init__(
            name="Feroxbuster",
            executable_path="tools/feroxbuster/target/release/feroxbuster",
            config_file="config/feroxbuster.conf",
            description="Fast Content Discovery Tool",
            category="Web Security",
            port=7021,
        )
        self.logger = logging.getLogger(__name__)

    async def execute_scan(
        self, target: str, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute Feroxbuster content discovery"""
        if options is None:
            options = {}

        try:
            # Build command
            cmd = [str(self.executable_path)]

            # Add URL
            cmd.extend(["--url", target])

            # Add wordlist
            wordlist = options.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
            cmd.extend(["--wordlist", wordlist])

            # Add threads
            threads = options.get("threads", 50)
            cmd.extend(["--threads", str(threads)])

            # Add depth
            depth = options.get("depth", 4)
            cmd.extend(["--depth", str(depth)])

            # Add extensions
            extensions = options.get("extensions", ["php", "html", "js", "txt"])
            if extensions:
                cmd.extend(["--extensions", ",".join(extensions)])

            # Add status codes to filter
            status_codes = options.get("status_codes", [200, 301, 302, 401, 403])
            if status_codes:
                cmd.extend(["--status-codes", ",".join(map(str, status_codes))])

            # Add timeout
            timeout = options.get("timeout", 7)
            cmd.extend(["--timeout", str(timeout)])

            # Add user agent
            user_agent = options.get("user_agent", "Feroxbuster/2.7.1")
            cmd.extend(["--user-agent", user_agent])

            # Output format
            cmd.extend(["--output", "/tmp/feroxbuster_output.json"])
            cmd.append("--json")

            # Execute command
            result = await self._execute_command(cmd, timeout=300)

            # Read JSON output
            output_data = await self._read_json_output("/tmp/feroxbuster_output.json")

            return {
                "success": True,
                "tool": self.name,
                "target": target,
                "wordlist": wordlist,
                "threads": threads,
                "depth": depth,
                "extensions": extensions,
                "results": output_data,
                "raw_output": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Feroxbuster execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": self.name,
                "target": target,
                "timestamp": self._get_timestamp(),
            }

    async def directory_brute_force(
        self, target: str, wordlist: str = None
    ) -> Dict[str, Any]:
        """Perform directory brute force attack"""
        try:
            cmd = [str(self.executable_path)]
            cmd.extend(["--url", target])

            if wordlist:
                cmd.extend(["--wordlist", wordlist])
            else:
                # Use default wordlist
                cmd.extend(["--wordlist", "/usr/share/wordlists/dirb/common.txt"])

            # Focus on directories
            cmd.extend(["--add-slash"])
            cmd.extend(["--status-codes", "200,301,302,403"])
            cmd.extend(["--threads", "30"])

            result = await self._execute_command(cmd)

            return {
                "success": True,
                "scan_type": "directory_brute_force",
                "target": target,
                "wordlist": wordlist,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Directory brute force failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def file_discovery(
        self, target: str, extensions: List[str] = None
    ) -> Dict[str, Any]:
        """Discover files with specific extensions"""
        try:
            if extensions is None:
                extensions = [
                    "php",
                    "asp",
                    "aspx",
                    "jsp",
                    "html",
                    "js",
                    "txt",
                    "xml",
                    "json",
                ]

            cmd = [str(self.executable_path)]
            cmd.extend(["--url", target])
            cmd.extend(["--extensions", ",".join(extensions)])
            cmd.extend(["--status-codes", "200,403"])
            cmd.extend(["--threads", "40"])

            result = await self._execute_command(cmd)

            return {
                "success": True,
                "scan_type": "file_discovery",
                "target": target,
                "extensions": extensions,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"File discovery failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def recursive_scan(self, target: str, max_depth: int = 3) -> Dict[str, Any]:
        """Perform recursive directory scanning"""
        try:
            cmd = [str(self.executable_path)]
            cmd.extend(["--url", target])
            cmd.extend(["--depth", str(max_depth)])
            cmd.extend(["--auto-tune"])
            cmd.extend(["--smart"])

            result = await self._execute_command(cmd)

            return {
                "success": True,
                "scan_type": "recursive_scan",
                "target": target,
                "max_depth": max_depth,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Recursive scan failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def _read_json_output(self, output_file: str) -> Dict[str, Any]:
        """Read JSON output from file"""
        try:
            output_path = Path(output_file)
            if output_path.exists():
                with open(output_path, "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.warning(f"Failed to read JSON output: {e}")
            return {}

    def parse_results(self, output: str) -> Dict[str, Any]:
        """Parse Feroxbuster output"""
        try:
            # Parse text output for discovered URLs
            lines = output.strip().split("\n")
            discovered_urls = []
            statistics = {}

            for line in lines:
                if "200" in line or "301" in line or "302" in line or "403" in line:
                    # Extract URL and status code
                    parts = line.split()
                    if len(parts) >= 3:
                        status_code = parts[0]
                        size = parts[1] if parts[1].isdigit() else "unknown"
                        url = parts[-1]

                        discovered_urls.append(
                            {"url": url, "status_code": status_code, "size": size}
                        )

                # Extract statistics
                if "Discovered URLs:" in line:
                    statistics["total_discovered"] = int(line.split(":")[-1].strip())
                elif "Total requests:" in line:
                    statistics["total_requests"] = int(line.split(":")[-1].strip())

            return {
                "discovered_urls": discovered_urls,
                "statistics": statistics,
                "total_found": len(discovered_urls),
                "raw_output": output,
            }

        except Exception as e:
            return {
                "error": f"Failed to parse Feroxbuster output: {e}",
                "raw_output": output,
            }

    async def build_from_source(self) -> Dict[str, Any]:
        """Build Feroxbuster from source if binary not available"""
        try:
            work_dir = Path(self.executable_path).parent.parent

            # Check if Rust is installed
            rust_check = subprocess.run(
                ["cargo", "--version"], capture_output=True, text=True
            )

            if rust_check.returncode != 0:
                return {
                    "success": False,
                    "error": "Rust/Cargo not installed. Please install Rust to build Feroxbuster.",
                    "timestamp": self._get_timestamp(),
                }

            # Build the project
            build_cmd = ["cargo", "build", "--release"]
            result = await self._execute_command(build_cmd, work_dir)

            # Check if binary was created
            binary_path = work_dir / "target" / "release" / "feroxbuster"
            if binary_path.exists():
                return {
                    "success": True,
                    "message": "Feroxbuster built successfully",
                    "binary_path": str(binary_path),
                    "build_output": result,
                    "timestamp": self._get_timestamp(),
                }
            else:
                return {
                    "success": False,
                    "error": "Build completed but binary not found",
                    "build_output": result,
                    "timestamp": self._get_timestamp(),
                }

        except Exception as e:
            self.logger.error(f"Build from source failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def check_dependencies(self) -> Dict[str, Any]:
        """Check Feroxbuster dependencies"""
        try:
            # Check if binary exists
            binary_exists = Path(self.executable_path).exists()

            # Check Rust/Cargo for building
            rust_result = subprocess.run(
                ["cargo", "--version"], capture_output=True, text=True
            )

            dependencies = {
                "binary": {
                    "available": binary_exists,
                    "path": str(self.executable_path),
                },
                "rust": {
                    "available": rust_result.returncode == 0,
                    "version": (
                        rust_result.stdout.strip()
                        if rust_result.returncode == 0
                        else None
                    ),
                },
            }

            ready_to_use = binary_exists
            can_build = rust_result.returncode == 0

            return {
                "success": ready_to_use or can_build,
                "dependencies": dependencies,
                "ready_to_use": ready_to_use,
                "can_build": can_build,
                "message": (
                    "Ready to use"
                    if ready_to_use
                    else (
                        "Can build from source" if can_build else "Dependencies missing"
                    )
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
_feroxbuster_wrapper = None


def get_feroxbuster_wrapper() -> FeroxbusterWrapper:
    """Get global Feroxbuster wrapper instance"""
    global _feroxbuster_wrapper
    if _feroxbuster_wrapper is None:
        _feroxbuster_wrapper = FeroxbusterWrapper()
    return _feroxbuster_wrapper
