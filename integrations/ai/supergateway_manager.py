#!/usr/bin/env python3
"""
LANCELOTT SuperGateway Integration
MCP (Model Context Protocol) Gateway for AI interactions
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp

from fastapi import HTTPException


class SuperGatewayManager:
    """Manager for SuperGateway MCP protocol bridge"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.gateway_path = self.project_root / "integrations" / "ai" / "supergateway"
        self.logger = self._setup_logging()
        self.process: Optional[subprocess.Popen] = None
        self.base_url = "http://localhost:3000"
        self.is_running = False

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for SuperGateway manager"""
        return logging.getLogger(__name__)

    async def start_gateway(self, port: int = 3000) -> bool:
        """Start the SuperGateway MCP server"""
        try:
            if self.is_running:
                self.logger.info("SuperGateway is already running")
                return True

            # Check if Node.js dependencies are installed
            package_json = self.gateway_path / "package.json"
            if not package_json.exists():
                raise FileNotFoundError("SuperGateway package.json not found")

            node_modules = self.gateway_path / "node_modules"
            if not node_modules.exists():
                self.logger.info("Installing SuperGateway dependencies...")
                await self._install_dependencies()

            # Start the SuperGateway server
            self.logger.info(f"Starting SuperGateway on port {port}...")

            cmd = ["npm", "start"]
            env = {"PORT": str(port)}

            self.process = subprocess.Popen(
                cmd,
                cwd=self.gateway_path,
                env={**dict(subprocess.os.environ), **env},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Wait a moment for startup
            await asyncio.sleep(3)

            # Check if process is still running
            if self.process.poll() is None:
                self.is_running = True
                self.base_url = f"http://localhost:{port}"
                self.logger.info(
                    f"SuperGateway started successfully on {self.base_url}"
                )
                return True
            else:
                stdout, stderr = self.process.communicate()
                self.logger.error(f"SuperGateway failed to start: {stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to start SuperGateway: {e}")
            return False

    async def stop_gateway(self) -> bool:
        """Stop the SuperGateway server"""
        try:
            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait(timeout=10)
                self.is_running = False
                self.logger.info("SuperGateway stopped successfully")
                return True
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop SuperGateway: {e}")
            if self.process:
                self.process.kill()
            return False

    async def _install_dependencies(self) -> None:
        """Install Node.js dependencies for SuperGateway"""
        try:
            process = subprocess.run(
                ["npm", "install"],
                cwd=self.gateway_path,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if process.returncode != 0:
                raise RuntimeError(f"npm install failed: {process.stderr}")

            self.logger.info("SuperGateway dependencies installed successfully")

        except subprocess.TimeoutExpired:
            raise RuntimeError("npm install timed out")
        except Exception as e:
            raise RuntimeError(f"Failed to install dependencies: {e}")

    async def health_check(self) -> bool:
        """Check if SuperGateway is healthy and responding"""
        try:
            if not self.is_running:
                return False

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/health", timeout=5
                ) as response:
                    return response.status == 200

        except Exception as e:
            self.logger.warning(f"SuperGateway health check failed: {e}")
            return False

    async def create_mcp_connection(
        self, server_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create MCP server connection through SuperGateway"""
        try:
            if not self.is_running:
                raise HTTPException(status_code=503, detail="SuperGateway not running")

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/mcp/connect", json=server_config, timeout=10
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"MCP connection failed: {error_text}",
                        )

        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=503, detail=f"SuperGateway connection error: {e}"
            )

    async def execute_mcp_tool(
        self, connection_id: str, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute an MCP tool through SuperGateway"""
        try:
            if not self.is_running:
                raise HTTPException(status_code=503, detail="SuperGateway not running")

            payload = {
                "connection_id": connection_id,
                "tool_name": tool_name,
                "arguments": arguments,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/mcp/execute", json=payload, timeout=30
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"MCP tool execution failed: {error_text}",
                        )

        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=503, detail=f"SuperGateway connection error: {e}"
            )

    async def list_mcp_tools(self, connection_id: str) -> List[Dict[str, Any]]:
        """List available MCP tools for a connection"""
        try:
            if not self.is_running:
                raise HTTPException(status_code=503, detail="SuperGateway not running")

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/mcp/tools/{connection_id}", timeout=10
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("tools", [])
                    else:
                        error_text = await response.text()
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"Failed to list MCP tools: {error_text}",
                        )

        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=503, detail=f"SuperGateway connection error: {e}"
            )

    async def stream_mcp_interaction(
        self, connection_id: str, messages: List[Dict[str, Any]]
    ):
        """Stream MCP interaction through SuperGateway"""
        try:
            if not self.is_running:
                raise HTTPException(status_code=503, detail="SuperGateway not running")

            payload = {"connection_id": connection_id, "messages": messages}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/mcp/stream", json=payload, timeout=None
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line:
                                try:
                                    data = json.loads(line.decode().strip())
                                    yield data
                                except json.JSONDecodeError:
                                    continue
                    else:
                        error_text = await response.text()
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"MCP streaming failed: {error_text}",
                        )

        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=503, detail=f"SuperGateway connection error: {e}"
            )

    def get_status(self) -> Dict[str, Any]:
        """Get SuperGateway status information"""
        return {
            "running": self.is_running,
            "base_url": self.base_url,
            "process_id": self.process.pid if self.process else None,
            "gateway_path": str(self.gateway_path),
        }

    async def get_gateway_info(self) -> Dict[str, Any]:
        """Get SuperGateway service information"""
        try:
            if not self.is_running:
                return {"status": "stopped", "version": None, "features": []}

            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/info", timeout=5) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"status": "error", "message": await response.text()}

        except Exception as e:
            return {"status": "error", "message": str(e)}


# Global SuperGateway manager instance
_gateway_manager = None


def get_supergateway_manager() -> SuperGatewayManager:
    """Get global SuperGateway manager instance"""
    global _gateway_manager
    if _gateway_manager is None:
        _gateway_manager = SuperGatewayManager()
    return _gateway_manager
