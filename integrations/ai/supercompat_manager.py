#!/usr/bin/env python3
"""
LANCELOTT SuperCompat Integration
AI Compatibility Handler for Multi-Provider Support
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Optional

import aiohttp

from fastapi import HTTPException


class SuperCompatManager:
    """Manager for SuperCompat AI compatibility layer"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.compat_path = self.project_root / "integrations" / "ai" / "supercompat"
        self.package_path = self.compat_path / "packages" / "supercompat"
        self.logger = self._setup_logging()
        self.process: Optional[subprocess.Popen] = None
        self.base_url = "http://localhost:3001"
        self.is_running = False

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for SuperCompat manager"""
        return logging.getLogger(__name__)

    async def start_compat_service(self, port: int = 3001) -> bool:
        """Start the SuperCompat compatibility service"""
        try:
            if self.is_running:
                self.logger.info("SuperCompat is already running")
                return True

            # Check if the package exists
            if not self.package_path.exists():
                raise FileNotFoundError("SuperCompat package not found")

            # Install dependencies if needed
            node_modules = self.package_path / "node_modules"
            if not node_modules.exists():
                self.logger.info("Installing SuperCompat dependencies...")
                await self._install_dependencies()

            # Build the package if needed
            dist_path = self.package_path / "dist"
            if not dist_path.exists():
                self.logger.info("Building SuperCompat package...")
                await self._build_package()

            # Start the SuperCompat service
            self.logger.info(f"Starting SuperCompat on port {port}...")

            cmd = ["npm", "start"]
            env = {"PORT": str(port)}

            self.process = subprocess.Popen(
                cmd,
                cwd=self.package_path,
                env={**dict(subprocess.os.environ), **env},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Wait for startup
            await asyncio.sleep(3)

            # Check if process is still running
            if self.process.poll() is None:
                self.is_running = True
                self.base_url = f"http://localhost:{port}"
                self.logger.info(f"SuperCompat started successfully on {self.base_url}")
                return True
            else:
                stdout, stderr = self.process.communicate()
                self.logger.error(f"SuperCompat failed to start: {stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to start SuperCompat: {e}")
            return False

    async def stop_compat_service(self) -> bool:
        """Stop the SuperCompat service"""
        try:
            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait(timeout=10)
                self.is_running = False
                self.logger.info("SuperCompat stopped successfully")
                return True
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop SuperCompat: {e}")
            if self.process:
                self.process.kill()
            return False

    async def _install_dependencies(self) -> None:
        """Install Node.js dependencies for SuperCompat"""
        try:
            # Install root dependencies
            process = subprocess.run(
                ["npm", "install"],
                cwd=self.compat_path,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if process.returncode != 0:
                raise RuntimeError(f"Root npm install failed: {process.stderr}")

            # Install package dependencies
            process = subprocess.run(
                ["npm", "install"],
                cwd=self.package_path,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if process.returncode != 0:
                raise RuntimeError(f"Package npm install failed: {process.stderr}")

            self.logger.info("SuperCompat dependencies installed successfully")

        except subprocess.TimeoutExpired:
            raise RuntimeError("npm install timed out")
        except Exception as e:
            raise RuntimeError(f"Failed to install dependencies: {e}")

    async def _build_package(self) -> None:
        """Build the SuperCompat package"""
        try:
            process = subprocess.run(
                ["npm", "run", "build"],
                cwd=self.package_path,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if process.returncode != 0:
                raise RuntimeError(f"Build failed: {process.stderr}")

            self.logger.info("SuperCompat package built successfully")

        except subprocess.TimeoutExpired:
            raise RuntimeError("Build timed out")
        except Exception as e:
            raise RuntimeError(f"Failed to build package: {e}")

    async def health_check(self) -> bool:
        """Check if SuperCompat is healthy and responding"""
        try:
            if not self.is_running:
                return False

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/health", timeout=5
                ) as response:
                    return response.status == 200

        except Exception as e:
            self.logger.warning(f"SuperCompat health check failed: {e}")
            return False

    async def translate_request(
        self, source_provider: str, target_provider: str, request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Translate AI request between different providers"""
        try:
            if not self.is_running:
                raise HTTPException(status_code=503, detail="SuperCompat not running")

            payload = {
                "source": source_provider,
                "target": target_provider,
                "data": request_data,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/translate/request", json=payload, timeout=10
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"Request translation failed: {error_text}",
                        )

        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=503, detail=f"SuperCompat connection error: {e}"
            )

    async def translate_response(
        self, source_provider: str, target_provider: str, response_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Translate AI response between different providers"""
        try:
            if not self.is_running:
                raise HTTPException(status_code=503, detail="SuperCompat not running")

            payload = {
                "source": source_provider,
                "target": target_provider,
                "data": response_data,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/translate/response", json=payload, timeout=10
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"Response translation failed: {error_text}",
                        )

        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=503, detail=f"SuperCompat connection error: {e}"
            )

    async def get_supported_providers(self) -> List[str]:
        """Get list of supported AI providers"""
        try:
            if not self.is_running:
                raise HTTPException(status_code=503, detail="SuperCompat not running")

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/providers", timeout=5
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("providers", [])
                    else:
                        error_text = await response.text()
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"Failed to get providers: {error_text}",
                        )

        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=503, detail=f"SuperCompat connection error: {e}"
            )

    async def stream_compatible_request(
        self, provider: str, request_data: Dict[str, Any]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream compatible AI request"""
        try:
            if not self.is_running:
                raise HTTPException(status_code=503, detail="SuperCompat not running")

            payload = {"provider": provider, "data": request_data, "stream": True}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/stream", json=payload, timeout=None
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
                            detail=f"Streaming failed: {error_text}",
                        )

        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=503, detail=f"SuperCompat connection error: {e}"
            )

    async def validate_compatibility(
        self, source_provider: str, target_provider: str, feature: str
    ) -> bool:
        """Check if a feature is compatible between providers"""
        try:
            if not self.is_running:
                raise HTTPException(status_code=503, detail="SuperCompat not running")

            params = {
                "source": source_provider,
                "target": target_provider,
                "feature": feature,
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/compatibility", params=params, timeout=5
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("compatible", False)
                    else:
                        return False

        except Exception as e:
            self.logger.warning(f"Compatibility check failed: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get SuperCompat status information"""
        return {
            "running": self.is_running,
            "base_url": self.base_url,
            "process_id": self.process.pid if self.process else None,
            "compat_path": str(self.compat_path),
            "package_path": str(self.package_path),
        }

    async def get_service_info(self) -> Dict[str, Any]:
        """Get SuperCompat service information"""
        try:
            if not self.is_running:
                return {"status": "stopped", "version": None, "providers": []}

            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/info", timeout=5) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"status": "error", "message": await response.text()}

        except Exception as e:
            return {"status": "error", "message": str(e)}


# Global SuperCompat manager instance
_compat_manager = None


def get_supercompat_manager() -> SuperCompatManager:
    """Get global SuperCompat manager instance"""
    global _compat_manager
    if _compat_manager is None:
        _compat_manager = SuperCompatManager()
    return _compat_manager
