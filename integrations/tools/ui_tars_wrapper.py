#!/usr/bin/env python3
"""
UI-TARS Integration Wrapper
CERBERUS-FANGS LANCELOTT Framework Integration

Provides programmatic access to UI-TARS Desktop and Agent-TARS CLI
with async/await patterns, process management, and health checking.
"""

import asyncio
import json
import logging
import os
import signal
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class UITARSMode(Enum):
    """UI-TARS operation modes"""

    DESKTOP = "desktop"
    AGENT_CLI = "agent_cli"
    WEB_INTERFACE = "web_interface"
    BATCH = "batch"


class UITARSStatus(Enum):
    """UI-TARS process status"""

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


@dataclass
class UITARSConfig:
    """UI-TARS configuration data class"""

    # General settings
    enabled: bool = True
    binary_path: str = "tools/UI-TARS"
    config_path: str = "tools/UI-TARS/ui-tars.conf"
    preset_path: str = "tools/UI-TARS/cerberus-gpt5-nano-preset.yaml"

    # Network settings
    port: int = 8765
    web_port: int = 5173
    host: str = "localhost"

    # Mode settings
    desktop_mode: bool = True
    web_interface: bool = True

    # AI Configuration
    ai_model: str = "gpt-5-nano"
    ai_provider: str = "azure"
    ai_deployment: str = "GPT-5-Navo-Cerberus"
    ai_endpoint: str = ""
    ai_api_key: str = ""
    ai_max_tokens: int = 16384
    ai_max_completion_tokens: int = 16384
    ai_temperature: float = 0.1
    ai_top_p: float = 0.9

    # Authentication
    auth_enabled: bool = True
    firebase_api_key: str = ""
    firebase_project_id: str = "lancelott-z9dko"
    framework_api_url: str = "http://localhost:7777"

    # Paths and directories
    output_dir: str = "reports/ui_tars_automation"
    screenshot_dir: str = "reports/screenshots"
    recording_dir: str = "reports/recordings"
    log_dir: str = "logs"
    cache_dir: str = "cache/ui_tars"

    # Performance settings
    timeout: int = 300
    max_concurrent_tasks: int = 2
    screenshot_scale: float = 1.0
    max_loop_count: int = 50
    loop_interval_ms: int = 2000
    action_timeout: int = 30000


@dataclass
class ProcessInfo:
    """Process information data class"""

    pid: int
    mode: UITARSMode
    status: UITARSStatus
    started_at: datetime
    command: List[str]
    log_file: Optional[str] = None
    web_url: Optional[str] = None


class UITARSWrapper:
    """
    Comprehensive UI-TARS wrapper for LANCELOTT framework integration

    Provides async/await patterns, process management, health checking,
    and seamless integration with the CERBERUS-FANGS security framework.
    """

    def __init__(self, config: Optional[UITARSConfig] = None):
        """Initialize UI-TARS wrapper"""
        self.config = config or self._load_config_from_env()
        self.processes: Dict[UITARSMode, ProcessInfo] = {}
        self.is_running = False
        self._setup_directories()
        self._setup_logging()

        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _load_config_from_env(self) -> UITARSConfig:
        """Load configuration from environment variables"""
        config = UITARSConfig()

        # General settings
        config.enabled = os.getenv("UI_TARS_ENABLED", "true").lower() == "true"
        config.binary_path = os.getenv("UI_TARS_BINARY_PATH", "tools/UI-TARS")
        config.config_path = os.getenv(
            "UI_TARS_CONFIG_PATH", "tools/UI-TARS/ui-tars.conf"
        )
        config.preset_path = os.getenv(
            "UI_TARS_PRESET", "cerberus-gpt5-nano-preset.yaml"
        )

        # Network settings
        config.port = int(os.getenv("UI_TARS_PORT", "8765"))
        config.web_port = int(os.getenv("UI_TARS_WEB_PORT", "5173"))
        config.host = os.getenv("UI_TARS_HOST", "localhost")

        # Mode settings
        config.desktop_mode = (
            os.getenv("UI_TARS_DESKTOP_MODE", "true").lower() == "true"
        )
        config.web_interface = (
            os.getenv("UI_TARS_WEB_INTERFACE", "true").lower() == "true"
        )

        # AI Configuration
        config.ai_model = os.getenv("UI_TARS_AI_MODEL", "gpt-5-nano")
        config.ai_provider = os.getenv("UI_TARS_AI_PROVIDER", "azure")
        config.ai_deployment = os.getenv("UI_TARS_AI_DEPLOYMENT", "GPT-5-Navo-Cerberus")
        config.ai_endpoint = os.getenv("UI_TARS_AI_ENDPOINT", "")
        config.ai_api_key = os.getenv("UI_TARS_AI_API_KEY", "")
        config.ai_max_tokens = int(os.getenv("UI_TARS_AI_MAX_TOKENS", "16384"))
        config.ai_max_completion_tokens = int(
            os.getenv("UI_TARS_AI_MAX_COMPLETION_TOKENS", "16384")
        )
        config.ai_temperature = float(os.getenv("UI_TARS_AI_TEMPERATURE", "0.1"))
        config.ai_top_p = float(os.getenv("UI_TARS_AI_TOP_P", "0.9"))

        # Authentication
        config.auth_enabled = (
            os.getenv("UI_TARS_AUTH_ENABLED", "true").lower() == "true"
        )
        config.firebase_api_key = os.getenv("UI_TARS_API_KEY", "")
        config.firebase_project_id = os.getenv(
            "UI_TARS_FIREBASE_PROJECT_ID", "lancelott-z9dko"
        )
        config.framework_api_url = os.getenv(
            "UI_TARS_FRAMEWORK_API_URL", "http://localhost:7777"
        )

        # Directories
        config.output_dir = os.getenv(
            "UI_TARS_OUTPUT_DIR", "reports/ui_tars_automation"
        )
        config.screenshot_dir = os.getenv(
            "UI_TARS_SCREENSHOT_DIR", "reports/screenshots"
        )
        config.recording_dir = os.getenv("UI_TARS_RECORDING_DIR", "reports/recordings")
        config.log_dir = os.getenv("UI_TARS_LOG_DIR", "logs")
        config.cache_dir = os.getenv("UI_TARS_CACHE_DIR", "cache/ui_tars")

        # Performance
        config.timeout = int(os.getenv("UI_TARS_DEFAULT_TIMEOUT", "300"))
        config.max_concurrent_tasks = int(os.getenv("UI_TARS_PARALLEL_TASKS", "2"))
        config.screenshot_scale = float(os.getenv("UI_TARS_SCREENSHOT_SCALE", "1.0"))
        config.max_loop_count = int(os.getenv("UI_TARS_MAX_LOOP_COUNT", "50"))
        config.loop_interval_ms = int(os.getenv("UI_TARS_LOOP_INTERVAL_MS", "2000"))
        config.action_timeout = int(os.getenv("UI_TARS_ACTION_TIMEOUT", "30000"))

        return config

    def _setup_directories(self):
        """Create necessary directories"""
        directories = [
            self.config.output_dir,
            self.config.screenshot_dir,
            self.config.recording_dir,
            self.config.log_dir,
            self.config.cache_dir,
            "config/ui_tars",
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

    def _setup_logging(self):
        """Set up logging configuration"""
        log_file = Path(self.config.log_dir) / "ui_tars_wrapper.log"

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.info("UI-TARS wrapper initialized")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop_all())

    async def start_desktop(self) -> bool:
        """Start UI-TARS Desktop application"""
        if not self.config.enabled or not self.config.desktop_mode:
            logger.warning("UI-TARS Desktop is disabled")
            return False

        if UITARSMode.DESKTOP in self.processes:
            logger.info("UI-TARS Desktop is already running")
            return True

        try:
            logger.info("Starting UI-TARS Desktop...")

            # Prepare command
            ui_tars_dir = Path(self.config.binary_path)
            if not ui_tars_dir.exists():
                logger.error(f"UI-TARS directory not found: {ui_tars_dir}")
                return False

            command = ["pnpm", "run", "dev:ui-tars"]
            log_file = Path(self.config.log_dir) / "ui_tars_desktop.log"

            # Start process
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=ui_tars_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env=self._get_env_vars(),
            )

            # Create process info
            process_info = ProcessInfo(
                pid=process.pid,
                mode=UITARSMode.DESKTOP,
                status=UITARSStatus.STARTING,
                started_at=datetime.now(),
                command=command,
                log_file=str(log_file),
                web_url=f"http://{self.config.host}:{self.config.web_port}",
            )

            self.processes[UITARSMode.DESKTOP] = process_info

            # Monitor startup
            await self._monitor_startup(process, process_info)

            if process_info.status == UITARSStatus.RUNNING:
                logger.info(
                    f"UI-TARS Desktop started successfully (PID: {process.pid})"
                )
                logger.info(f"Web interface available at: {process_info.web_url}")
                return True
            else:
                logger.error("Failed to start UI-TARS Desktop")
                return False

        except Exception as e:
            logger.error(f"Error starting UI-TARS Desktop: {e}")
            return False

    async def start_agent_cli(
        self, task: Optional[str] = None, interactive: bool = True
    ) -> bool:
        """Start Agent-TARS CLI"""
        if UITARSMode.AGENT_CLI in self.processes:
            logger.info("Agent-TARS CLI is already running")
            return True

        try:
            logger.info("Starting Agent-TARS CLI...")

            # Prepare command
            agent_cli_dir = (
                Path(self.config.binary_path) / "multimodal" / "agent-tars" / "cli"
            )
            if not agent_cli_dir.exists():
                logger.error(f"Agent-TARS CLI directory not found: {agent_cli_dir}")
                return False

            command = ["pnpm", "run", "dev"]
            if not interactive:
                command.extend(["--batch"])
                if task:
                    command.extend(["--task", task])
            else:
                command.append("--interactive")

            log_file = Path(self.config.log_dir) / "agent_tars_cli.log"

            # Start process
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=agent_cli_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env=self._get_env_vars(),
            )

            # Create process info
            process_info = ProcessInfo(
                pid=process.pid,
                mode=UITARSMode.AGENT_CLI,
                status=UITARSStatus.STARTING,
                started_at=datetime.now(),
                command=command,
                log_file=str(log_file),
            )

            self.processes[UITARSMode.AGENT_CLI] = process_info

            # Monitor startup
            await self._monitor_startup(process, process_info)

            if process_info.status == UITARSStatus.RUNNING:
                logger.info(f"Agent-TARS CLI started successfully (PID: {process.pid})")
                return True
            else:
                logger.error("Failed to start Agent-TARS CLI")
                return False

        except Exception as e:
            logger.error(f"Error starting Agent-TARS CLI: {e}")
            return False

    async def start_web_interface(self) -> bool:
        """Start web interface only"""
        if not self.config.web_interface:
            logger.warning("Web interface is disabled")
            return False

        if UITARSMode.WEB_INTERFACE in self.processes:
            logger.info("Web interface is already running")
            return True

        try:
            logger.info("Starting UI-TARS web interface...")

            # Prepare command
            web_dir = Path(self.config.binary_path) / "apps" / "ui-tars"
            if not web_dir.exists():
                logger.error(f"Web interface directory not found: {web_dir}")
                return False

            command = ["npm", "run", "dev"]
            log_file = Path(self.config.log_dir) / "ui_tars_web.log"

            # Start process
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=web_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env=self._get_env_vars(),
            )

            # Create process info
            process_info = ProcessInfo(
                pid=process.pid,
                mode=UITARSMode.WEB_INTERFACE,
                status=UITARSStatus.STARTING,
                started_at=datetime.now(),
                command=command,
                log_file=str(log_file),
                web_url=f"http://{self.config.host}:{self.config.web_port}",
            )

            self.processes[UITARSMode.WEB_INTERFACE] = process_info

            # Monitor startup
            await self._monitor_startup(process, process_info)

            if process_info.status == UITARSStatus.RUNNING:
                logger.info(f"Web interface started successfully (PID: {process.pid})")
                logger.info(f"Available at: {process_info.web_url}")
                return True
            else:
                logger.error("Failed to start web interface")
                return False

        except Exception as e:
            logger.error(f"Error starting web interface: {e}")
            return False

    async def stop_process(self, mode: UITARSMode) -> bool:
        """Stop a specific UI-TARS process"""
        if mode not in self.processes:
            logger.info(f"No {mode.value} process to stop")
            return True

        process_info = self.processes[mode]

        try:
            logger.info(f"Stopping {mode.value} (PID: {process_info.pid})...")
            process_info.status = UITARSStatus.STOPPING

            # Send SIGTERM
            os.kill(process_info.pid, signal.SIGTERM)

            # Wait for graceful shutdown
            for _ in range(10):
                try:
                    os.kill(process_info.pid, 0)  # Check if process exists
                    await asyncio.sleep(1)
                except ProcessLookupError:
                    # Process has terminated
                    break
            else:
                # Force kill if still running
                logger.warning(f"Force killing {mode.value} (PID: {process_info.pid})")
                os.kill(process_info.pid, signal.SIGKILL)

            del self.processes[mode]
            logger.info(f"{mode.value} stopped successfully")
            return True

        except ProcessLookupError:
            # Process already dead
            del self.processes[mode]
            return True
        except Exception as e:
            logger.error(f"Error stopping {mode.value}: {e}")
            return False

    async def stop_all(self) -> bool:
        """Stop all UI-TARS processes"""
        logger.info("Stopping all UI-TARS processes...")

        success = True
        for mode in list(self.processes.keys()):
            if not await self.stop_process(mode):
                success = False

        self.is_running = False
        return success

    async def restart_process(self, mode: UITARSMode) -> bool:
        """Restart a specific UI-TARS process"""
        logger.info(f"Restarting {mode.value}...")

        await self.stop_process(mode)
        await asyncio.sleep(2)  # Wait a bit between stop and start

        if mode == UITARSMode.DESKTOP:
            return await self.start_desktop()
        elif mode == UITARSMode.AGENT_CLI:
            return await self.start_agent_cli()
        elif mode == UITARSMode.WEB_INTERFACE:
            return await self.start_web_interface()

        return False

    def get_status(self) -> Dict[str, Any]:
        """Get current status of all UI-TARS processes"""
        status = {
            "enabled": self.config.enabled,
            "processes": {},
            "config": {
                "ai_model": f"{self.config.ai_provider}/{self.config.ai_model}",
                "deployment": self.config.ai_deployment,
                "max_tokens": self.config.ai_max_tokens,
                "temperature": self.config.ai_temperature,
                "desktop_mode": self.config.desktop_mode,
                "web_interface": self.config.web_interface,
                "ports": {"desktop": self.config.port, "web": self.config.web_port},
            },
        }

        for mode, process_info in self.processes.items():
            status["processes"][mode.value] = {
                "pid": process_info.pid,
                "status": process_info.status.value,
                "started_at": process_info.started_at.isoformat(),
                "command": " ".join(process_info.command),
                "log_file": process_info.log_file,
                "web_url": process_info.web_url,
            }

        return status

    def is_healthy(self) -> bool:
        """Check if UI-TARS is healthy"""
        if not self.config.enabled:
            return False

        # Check if any processes are running
        running_processes = [
            p for p in self.processes.values() if p.status == UITARSStatus.RUNNING
        ]

        return len(running_processes) > 0

    async def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        health_status = {
            "healthy": False,
            "timestamp": datetime.now().isoformat(),
            "processes": {},
            "config_files": {},
            "directories": {},
        }

        # Check processes
        for mode, process_info in self.processes.items():
            try:
                os.kill(process_info.pid, 0)  # Check if process exists
                health_status["processes"][mode.value] = "running"
            except ProcessLookupError:
                health_status["processes"][mode.value] = "dead"
            except Exception as e:
                health_status["processes"][mode.value] = f"error: {e}"

        # Check config files
        config_files = [
            self.config.config_path,
            self.config.preset_path,
            Path(self.config.binary_path) / "package.json",
        ]

        for config_file in config_files:
            path = Path(config_file)
            health_status["config_files"][str(path)] = path.exists()

        # Check directories
        directories = [
            self.config.binary_path,
            self.config.output_dir,
            self.config.log_dir,
            self.config.cache_dir,
        ]

        for directory in directories:
            path = Path(directory)
            health_status["directories"][str(path)] = path.exists()

        # Overall health
        health_status["healthy"] = (
            len([s for s in health_status["processes"].values() if s == "running"]) > 0
            and all(health_status["config_files"].values())
            and all(health_status["directories"].values())
        )

        return health_status

    def _get_env_vars(self) -> Dict[str, str]:
        """Get environment variables for UI-TARS processes"""
        env = os.environ.copy()

        # UI-TARS specific environment variables
        env.update(
            {
                "UI_TARS_AI_MODEL": self.config.ai_model,
                "UI_TARS_AI_PROVIDER": self.config.ai_provider,
                "UI_TARS_AI_DEPLOYMENT": self.config.ai_deployment,
                "UI_TARS_AI_ENDPOINT": self.config.ai_endpoint,
                "UI_TARS_AI_API_KEY": self.config.ai_api_key,
                "UI_TARS_AI_MAX_TOKENS": str(self.config.ai_max_tokens),
                "UI_TARS_AI_TEMPERATURE": str(self.config.ai_temperature),
                "UI_TARS_PORT": str(self.config.port),
                "UI_TARS_WEB_PORT": str(self.config.web_port),
                "UI_TARS_API_KEY": self.config.firebase_api_key,
                "UI_TARS_FIREBASE_PROJECT_ID": self.config.firebase_project_id,
                "UI_TARS_FRAMEWORK_API_URL": self.config.framework_api_url,
                "UI_TARS_OUTPUT_DIR": self.config.output_dir,
                "UI_TARS_LOG_DIR": self.config.log_dir,
                "UI_TARS_CACHE_DIR": self.config.cache_dir,
            }
        )

        return env

    async def _monitor_startup(
        self, process: asyncio.subprocess.Process, process_info: ProcessInfo
    ):
        """Monitor process startup"""
        try:
            # Wait for process to start or fail
            for i in range(30):  # 30 second timeout
                if process.returncode is not None:
                    # Process has exited
                    process_info.status = UITARSStatus.ERROR
                    return

                # Check if process is responding (for web services)
                if process_info.web_url:
                    import aiohttp

                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(
                                process_info.web_url, timeout=2
                            ) as response:
                                if response.status < 500:
                                    process_info.status = UITARSStatus.RUNNING
                                    return
                    except:
                        pass  # Not ready yet
                else:
                    # For non-web processes, assume running if still alive after 5 seconds
                    if i >= 5:
                        process_info.status = UITARSStatus.RUNNING
                        return

                await asyncio.sleep(1)

            # Timeout reached
            if process_info.status == UITARSStatus.STARTING:
                process_info.status = UITARSStatus.RUNNING  # Assume it's working

        except Exception as e:
            logger.error(f"Error monitoring startup: {e}")
            process_info.status = UITARSStatus.ERROR


# Example usage and integration functions
async def main():
    """Example usage of UI-TARS wrapper"""
    wrapper = UITARSWrapper()

    try:
        # Start UI-TARS Desktop
        if await wrapper.start_desktop():
            print("✅ UI-TARS Desktop started successfully")

        # Start Agent-TARS CLI in interactive mode
        if await wrapper.start_agent_cli(interactive=True):
            print("✅ Agent-TARS CLI started successfully")

        # Monitor for a while
        for _ in range(10):
            status = wrapper.get_status()
            print(f"Status: {status}")

            health = await wrapper.health_check()
            print(f"Health: {'✅' if health['healthy'] else '❌'}")

            await asyncio.sleep(5)

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await wrapper.stop_all()


if __name__ == "__main__":
    asyncio.run(main())
