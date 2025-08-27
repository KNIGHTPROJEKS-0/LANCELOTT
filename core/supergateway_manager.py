#!/usr/bin/env python3
"""
SuperGateway wrapper for CERBERUS-FANGS LANCELOTT
Provides Python interface to SuperGateway MCP stdio server gateway
"""

import asyncio
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil

from core.logger_config import setup_logging

logger = setup_logging()


class SuperGatewayManager:
    def __init__(self, base_path: str = "./SuperGateway"):
        self.base_path = Path(base_path)
        self.active_gateways: Dict[str, subprocess.Popen] = {}
        self.gateway_configs: Dict[str, Dict] = {}

    async def is_available(self) -> bool:
        """Check if SuperGateway is available and built"""
        try:
            dist_path = self.base_path / "dist" / "index.js"
            return dist_path.exists()
        except Exception as e:
            logger.error(f"Error checking SuperGateway availability: {e}")
            return False

    async def start_stdio_to_sse_gateway(
        self,
        gateway_id: str,
        stdio_command: str,
        port: int = 8000,
        base_url: Optional[str] = None,
        sse_path: str = "/sse",
        message_path: str = "/message",
        cors: bool = True,
        headers: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Start a stdio→SSE gateway"""
        try:
            if gateway_id in self.active_gateways:
                raise ValueError(f"Gateway {gateway_id} is already running")

            cmd = [
                "node",
                str(self.base_path / "dist" / "index.js"),
                "--stdio",
                stdio_command,
                "--port",
                str(port),
                "--ssePath",
                sse_path,
                "--messagePath",
                message_path,
            ]

            if base_url:
                cmd.extend(["--baseUrl", base_url])

            if cors:
                cmd.append("--cors")

            if headers:
                for header in headers:
                    cmd.extend(["--header", header])

            # Start the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.base_path,
            )

            # Wait a moment to check if it started successfully
            await asyncio.sleep(2)

            if process.poll() is not None:
                stdout, stderr = process.communicate()
                raise RuntimeError(f"Gateway failed to start: {stderr}")

            self.active_gateways[gateway_id] = process
            self.gateway_configs[gateway_id] = {
                "type": "stdio_to_sse",
                "stdio_command": stdio_command,
                "port": port,
                "base_url": base_url or f"http://localhost:{port}",
                "sse_path": sse_path,
                "message_path": message_path,
                "pid": process.pid,
            }

            logger.info(f"Started SuperGateway {gateway_id} on port {port}")

            return {
                "gateway_id": gateway_id,
                "status": "running",
                "config": self.gateway_configs[gateway_id],
                "endpoints": {
                    "sse_url": f"{self.gateway_configs[gateway_id]['base_url']}{sse_path}",
                    "message_url": f"{self.gateway_configs[gateway_id]['base_url']}{message_path}",
                },
            }

        except Exception as e:
            logger.error(f"Error starting SuperGateway {gateway_id}: {e}")
            raise

    async def start_sse_to_stdio_gateway(
        self, gateway_id: str, sse_url: str, headers: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Start an SSE→stdio gateway"""
        try:
            if gateway_id in self.active_gateways:
                raise ValueError(f"Gateway {gateway_id} is already running")

            cmd = ["node", str(self.base_path / "dist" / "index.js"), "--sse", sse_url]

            if headers:
                for header in headers:
                    cmd.extend(["--header", header])

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.base_path,
            )

            await asyncio.sleep(2)

            if process.poll() is not None:
                stdout, stderr = process.communicate()
                raise RuntimeError(f"Gateway failed to start: {stderr}")

            self.active_gateways[gateway_id] = process
            self.gateway_configs[gateway_id] = {
                "type": "sse_to_stdio",
                "sse_url": sse_url,
                "pid": process.pid,
            }

            logger.info(f"Started SSE→stdio gateway {gateway_id}")

            return {
                "gateway_id": gateway_id,
                "status": "running",
                "config": self.gateway_configs[gateway_id],
            }

        except Exception as e:
            logger.error(f"Error starting SSE→stdio gateway {gateway_id}: {e}")
            raise

    async def stop_gateway(self, gateway_id: str) -> Dict[str, Any]:
        """Stop a running gateway"""
        try:
            if gateway_id not in self.active_gateways:
                raise ValueError(f"Gateway {gateway_id} is not running")

            process = self.active_gateways[gateway_id]

            # Try graceful shutdown first
            try:
                process.terminate()
                await asyncio.sleep(2)

                if process.poll() is None:
                    # Force kill if still running
                    process.kill()
                    await asyncio.sleep(1)
            except ProcessLookupError:
                pass  # Process already terminated

            # Clean up
            del self.active_gateways[gateway_id]
            config = self.gateway_configs.pop(gateway_id, {})

            logger.info(f"Stopped SuperGateway {gateway_id}")

            return {"gateway_id": gateway_id, "status": "stopped", "config": config}

        except Exception as e:
            logger.error(f"Error stopping gateway {gateway_id}: {e}")
            raise

    async def list_gateways(self) -> Dict[str, Any]:
        """List all active gateways"""
        return {
            "active_gateways": len(self.active_gateways),
            "gateways": {
                gateway_id: {
                    **config,
                    "status": (
                        "running"
                        if self.active_gateways.get(gateway_id)
                        and self.active_gateways[gateway_id].poll() is None
                        else "stopped"
                    ),
                }
                for gateway_id, config in self.gateway_configs.items()
            },
        }

    async def get_gateway_status(self, gateway_id: str) -> Dict[str, Any]:
        """Get status of a specific gateway"""
        if gateway_id not in self.gateway_configs:
            raise ValueError(f"Gateway {gateway_id} not found")

        process = self.active_gateways.get(gateway_id)
        is_running = process and process.poll() is None

        config = self.gateway_configs[gateway_id]

        result = {
            "gateway_id": gateway_id,
            "status": "running" if is_running else "stopped",
            "config": config,
        }

        if is_running and process:
            try:
                proc_info = psutil.Process(process.pid)
                result["process_info"] = {
                    "cpu_percent": proc_info.cpu_percent(),
                    "memory_info": proc_info.memory_info()._asdict(),
                    "create_time": proc_info.create_time(),
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return result

    async def cleanup_all(self):
        """Stop all running gateways"""
        for gateway_id in list(self.active_gateways.keys()):
            try:
                await self.stop_gateway(gateway_id)
            except Exception as e:
                logger.error(f"Error stopping gateway {gateway_id} during cleanup: {e}")

    def __del__(self):
        """Cleanup on destruction"""
        try:
            for process in self.active_gateways.values():
                if process.poll() is None:
                    process.terminate()
        except:
            pass
