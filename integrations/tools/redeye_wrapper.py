#!/usr/bin/env python3
"""
RedEye Tool Integration Wrapper
Red Team Analysis and Campaign Management Platform
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.base_tool_wrapper import BaseToolWrapper


class RedEyeWrapper(BaseToolWrapper):
    """Wrapper for RedEye red team analysis platform"""

    def __init__(self):
        super().__init__(
            name="RedEye",
            executable_path="tools/RedEye",
            config_file="config/redeye.conf",
            description="Red Team Analysis and Campaign Management Platform",
            category="Red Team",
            port=7018,
        )
        self.logger = logging.getLogger(__name__)

    async def execute_scan(
        self, target: str, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute RedEye analysis"""
        if options is None:
            options = {}

        try:
            # Build command
            cmd = ["npm", "run", "dev"]

            # Set working directory to RedEye
            work_dir = Path(self.executable_path)

            # Environment variables
            env = {
                "NODE_ENV": options.get("env", "development"),
                "PORT": str(options.get("port", 3000)),
            }

            # Execute command
            result = await self._execute_command(cmd, work_dir, env)

            return {
                "success": True,
                "tool": self.name,
                "target": target,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"RedEye execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": self.name,
                "target": target,
                "timestamp": self._get_timestamp(),
            }

    async def setup_database(
        self, database_config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Setup RedEye database"""
        try:
            if database_config is None:
                database_config = {"type": "sqlite", "database": ":memory:"}

            # Run database setup
            cmd = ["npm", "run", "db:setup"]
            work_dir = Path(self.executable_path)

            result = await self._execute_command(cmd, work_dir)

            return {
                "success": True,
                "message": "Database setup completed",
                "config": database_config,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"RedEye database setup failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def import_campaign(
        self, campaign_path: str, parser_type: str = "cobalt-strike"
    ) -> Dict[str, Any]:
        """Import campaign data into RedEye"""
        try:
            cmd = [
                "node",
                "parsers/cobalt-strike-parser/dist/index.js",
                "parse-campaign",
                campaign_path,
            ]

            work_dir = Path(self.executable_path)
            result = await self._execute_command(cmd, work_dir)

            return {
                "success": True,
                "message": "Campaign imported successfully",
                "campaign_path": campaign_path,
                "parser": parser_type,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"RedEye campaign import failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def start_server(self, port: int = 3000) -> Dict[str, Any]:
        """Start RedEye server"""
        try:
            cmd = ["npm", "run", "start"]
            work_dir = Path(self.executable_path)

            env = {"PORT": str(port)}

            # Start server in background
            process = subprocess.Popen(
                cmd,
                cwd=work_dir,
                env={**dict(subprocess.os.environ), **env},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            return {
                "success": True,
                "message": f"RedEye server started on port {port}",
                "pid": process.pid,
                "port": port,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"RedEye server start failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    def parse_results(self, output: str) -> Dict[str, Any]:
        """Parse RedEye output"""
        try:
            # Try to parse JSON output
            if output.strip().startswith("{"):
                return json.loads(output)

            # Parse text output
            lines = output.strip().split("\n")

            return {
                "raw_output": output,
                "lines": lines,
                "summary": f"RedEye output with {len(lines)} lines",
            }

        except Exception as e:
            return {
                "error": f"Failed to parse RedEye output: {e}",
                "raw_output": output,
            }

    async def get_campaigns(self) -> Dict[str, Any]:
        """Get list of campaigns in RedEye"""
        try:
            # This would typically query the RedEye API
            return {
                "success": True,
                "campaigns": [],
                "message": "Campaign list retrieved",
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Failed to get campaigns: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def check_dependencies(self) -> Dict[str, Any]:
        """Check RedEye dependencies"""
        try:
            # Check Node.js
            node_result = subprocess.run(
                ["node", "--version"], capture_output=True, text=True
            )

            # Check npm
            npm_result = subprocess.run(
                ["npm", "--version"], capture_output=True, text=True
            )

            dependencies = {
                "node": {
                    "available": node_result.returncode == 0,
                    "version": (
                        node_result.stdout.strip()
                        if node_result.returncode == 0
                        else None
                    ),
                },
                "npm": {
                    "available": npm_result.returncode == 0,
                    "version": (
                        npm_result.stdout.strip()
                        if npm_result.returncode == 0
                        else None
                    ),
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
_redeye_wrapper = None


def get_redeye_wrapper() -> RedEyeWrapper:
    """Get global RedEye wrapper instance"""
    global _redeye_wrapper
    if _redeye_wrapper is None:
        _redeye_wrapper = RedEyeWrapper()
    return _redeye_wrapper
