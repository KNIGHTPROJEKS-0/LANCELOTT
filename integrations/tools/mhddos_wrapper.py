#!/usr/bin/env python3
"""
MHDDoS Tool Integration Wrapper
DDoS Testing and Stress Testing Tool
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.base_tool_wrapper import BaseToolWrapper


class MHDDoSWrapper(BaseToolWrapper):
    """Wrapper for MHDDoS DDoS testing tool"""

    def __init__(self):
        super().__init__(
            name="MHDDoS",
            executable_path="tools/MHDDoS/start.py",
            config_file="config/mhddos.conf",
            description="DDoS Testing and Stress Testing Tool",
            category="Stress Testing",
            port=7019,
        )
        self.logger = logging.getLogger(__name__)

    async def execute_scan(
        self, target: str, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute MHDDoS stress test"""
        if options is None:
            options = {}

        try:
            # Build command
            cmd = ["python3", "start.py"]

            # Add method
            method = options.get("method", "GET")
            cmd.extend(["--method", method])

            # Add threads
            threads = options.get("threads", 100)
            cmd.extend(["--threads", str(threads)])

            # Add duration
            duration = options.get("duration", 60)
            cmd.extend(["--time", str(duration)])

            # Add proxy list if provided
            if "proxy_list" in options:
                cmd.extend(["--proxy-list", options["proxy_list"]])

            # Add target
            cmd.append(target)

            # Set working directory
            work_dir = Path(self.executable_path).parent

            # Execute command with timeout
            result = await self._execute_command(cmd, work_dir, timeout=duration + 30)

            return {
                "success": True,
                "tool": self.name,
                "target": target,
                "method": method,
                "threads": threads,
                "duration": duration,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"MHDDoS execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": self.name,
                "target": target,
                "timestamp": self._get_timestamp(),
            }

    async def stress_test(
        self, target: str, test_config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Perform stress test with specific configuration"""
        if test_config is None:
            test_config = {
                "method": "GET",
                "threads": 50,
                "duration": 30,
                "rate_limit": True,
            }

        try:
            cmd = ["python3", "start.py"]

            # Configure stress test parameters
            cmd.extend(["--method", test_config.get("method", "GET")])
            cmd.extend(["--threads", str(test_config.get("threads", 50))])
            cmd.extend(["--time", str(test_config.get("duration", 30))])

            # Add rate limiting if enabled
            if test_config.get("rate_limit", True):
                cmd.extend(["--rpc", "200"])  # Requests per connection

            # Add target
            cmd.append(target)

            work_dir = Path(self.executable_path).parent
            result = await self._execute_command(cmd, work_dir)

            return {
                "success": True,
                "test_type": "stress_test",
                "target": target,
                "configuration": test_config,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"MHDDoS stress test failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def check_target_availability(self, target: str) -> Dict[str, Any]:
        """Check if target is reachable before testing"""
        try:
            import requests

            response = requests.get(target, timeout=10)
            available = response.status_code < 500

            return {
                "success": True,
                "target": target,
                "available": available,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            return {
                "success": False,
                "target": target,
                "available": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    def parse_results(self, output: str) -> Dict[str, Any]:
        """Parse MHDDoS output"""
        try:
            lines = output.strip().split("\n")

            # Extract key metrics
            metrics = {
                "requests_sent": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_response_time": 0.0,
            }

            for line in lines:
                if "Requests sent:" in line:
                    metrics["requests_sent"] = int(line.split(":")[-1].strip())
                elif "Successful:" in line:
                    metrics["successful_requests"] = int(line.split(":")[-1].strip())
                elif "Failed:" in line:
                    metrics["failed_requests"] = int(line.split(":")[-1].strip())
                elif "Average response time:" in line:
                    metrics["average_response_time"] = float(
                        line.split(":")[-1].strip().replace("ms", "")
                    )

            return {
                "metrics": metrics,
                "raw_output": output,
                "summary": f"Sent {metrics['requests_sent']} requests with {metrics['successful_requests']} successful",
            }

        except Exception as e:
            return {
                "error": f"Failed to parse MHDDoS output: {e}",
                "raw_output": output,
            }

    async def get_methods(self) -> List[str]:
        """Get available HTTP methods for testing"""
        return [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "HEAD",
            "OPTIONS",
            "PATCH",
            "CONNECT",
            "TRACE",
        ]

    async def check_dependencies(self) -> Dict[str, Any]:
        """Check MHDDoS dependencies"""
        try:
            # Check Python
            python_result = subprocess.run(
                ["python3", "--version"], capture_output=True, text=True
            )

            # Check required packages
            packages_to_check = ["requests", "aiohttp", "pysocks"]
            package_results = {}

            for package in packages_to_check:
                try:
                    __import__(package)
                    package_results[package] = {"available": True, "version": "unknown"}
                except ImportError:
                    package_results[package] = {"available": False, "version": None}

            dependencies = {
                "python": {
                    "available": python_result.returncode == 0,
                    "version": (
                        python_result.stdout.strip()
                        if python_result.returncode == 0
                        else None
                    ),
                },
                "packages": package_results,
            }

            all_available = dependencies["python"]["available"] and all(
                pkg["available"] for pkg in package_results.values()
            )

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
_mhddos_wrapper = None


def get_mhddos_wrapper() -> MHDDoSWrapper:
    """Get global MHDDoS wrapper instance"""
    global _mhddos_wrapper
    if _mhddos_wrapper is None:
        _mhddos_wrapper = MHDDoSWrapper()
    return _mhddos_wrapper
