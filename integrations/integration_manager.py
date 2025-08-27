#!/usr/bin/env python3
"""
CERBERUS-FANGS LANCELOTT - Unified Integration Manager
Manages all tool integrations and provides a unified interface
"""

import asyncio
import importlib.util
import json
import logging
import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class ToolConfig:
    """Configuration for a security tool"""

    name: str
    executable_path: str
    wrapper_module: Optional[str] = None
    config_file: Optional[str] = None
    port: Optional[int] = None
    dependencies: List[str] = None
    enabled: bool = True


class BaseToolWrapper(ABC):
    """Abstract base class for tool wrappers"""

    def __init__(self, config: ToolConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{config.name}")

    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the tool"""
        pass

    @abstractmethod
    async def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute a command with the tool"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the tool is healthy and responsive"""
        pass

    async def cleanup(self) -> None:
        """Clean up resources"""
        pass


class IntegrationManager:
    """Manages all tool integrations for LANCELOTT"""

    def __init__(self, config_path: str = None):
        self.project_root = Path(__file__).parent.parent.parent
        self.config_path = (
            config_path or self.project_root / "config" / "tools" / "integrations.json"
        )
        self.logger = self._setup_logging()
        self.tools: Dict[str, BaseToolWrapper] = {}
        self.tool_configs: Dict[str, ToolConfig] = {}

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for integration manager"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        return logging.getLogger(__name__)

    def _load_default_configs(self) -> Dict[str, ToolConfig]:
        """Load default tool configurations"""
        return {
            "nmap": ToolConfig(
                name="Nmap",
                executable_path=str(self.project_root / "nmap" / "nmap"),
                wrapper_module="integrations.tools.nmap_wrapper",
                port=7001,
            ),
            "argus": ToolConfig(
                name="Argus",
                executable_path=str(self.project_root / "tools" / "Argus" / "argus.py"),
                wrapper_module="integrations.tools.argus_wrapper",
                port=7002,
            ),
            "kraken": ToolConfig(
                name="Kraken",
                executable_path=str(
                    self.project_root / "tools" / "Kraken" / "kraken.py"
                ),
                wrapper_module="integrations.tools.kraken_wrapper",
                port=7003,
            ),
            "metabigor": ToolConfig(
                name="Metabigor",
                executable_path=str(
                    self.project_root / "tools" / "Metabigor" / "metabigor"
                ),
                wrapper_module="integrations.tools.metabigor_wrapper",
                port=7004,
            ),
            "osmedeus": ToolConfig(
                name="Osmedeus",
                executable_path=str(
                    self.project_root / "tools" / "Osmedeus" / "osmedeus"
                ),
                wrapper_module="integrations.tools.osmedeus_wrapper",
                port=7005,
            ),
            "spiderfoot": ToolConfig(
                name="SpiderFoot",
                executable_path=str(
                    self.project_root / "tools" / "Spiderfoot" / "sf.py"
                ),
                wrapper_module="integrations.tools.spiderfoot_wrapper",
                port=7006,
            ),
            "social_analyzer": ToolConfig(
                name="Social-Analyzer",
                executable_path=str(
                    self.project_root / "tools" / "Social-Analyzer" / "app.py"
                ),
                wrapper_module="integrations.tools.social_analyzer_wrapper",
                port=7007,
            ),
            "phonesploit": ToolConfig(
                name="PhoneSploit-Pro",
                executable_path=str(
                    self.project_root
                    / "tools"
                    / "PhoneSploit-Pro"
                    / "phonesploitpro.py"
                ),
                wrapper_module="integrations.tools.phonesploit_wrapper",
                port=7008,
            ),
            "vajra": ToolConfig(
                name="Vajra",
                executable_path=str(self.project_root / "tools" / "Vajra" / "vajra.py"),
                wrapper_module="integrations.tools.vajra_wrapper",
                port=7009,
            ),
            "storm_breaker": ToolConfig(
                name="Storm-Breaker",
                executable_path=str(
                    self.project_root / "tools" / "Storm-Breaker" / "st.py"
                ),
                wrapper_module="integrations.tools.storm_breaker_wrapper",
                port=7010,
            ),
            "dismap": ToolConfig(
                name="Dismap",
                executable_path=str(self.project_root / "tools" / "dismap" / "dismap"),
                wrapper_module="integrations.tools.dismap_wrapper",
                port=7011,
            ),
            "hydra": ToolConfig(
                name="THC-Hydra",
                executable_path=str(
                    self.project_root / "tools" / "THC-Hydra" / "hydra"
                ),
                wrapper_module="integrations.tools.hydra_wrapper",
                port=7012,
            ),
            "webstor": ToolConfig(
                name="Webstor",
                executable_path=str(
                    self.project_root / "tools" / "Webstor" / "webstor.py"
                ),
                wrapper_module="integrations.tools.webstor_wrapper",
                port=7013,
            ),
            "sherlock": ToolConfig(
                name="SHERLOCK",
                executable_path=str(
                    self.project_root
                    / "tools"
                    / "SHERLOCK"
                    / "sherlock_project"
                    / "sherlock.py"
                ),
                wrapper_module="integrations.tools.sherlock_wrapper",
                port=7014,
            ),
            "redteam_toolkit": ToolConfig(
                name="RedTeam-ToolKit",
                executable_path=str(
                    self.project_root / "tools" / "RedTeam-ToolKit" / "manage.py"
                ),
                wrapper_module="integrations.tools.redteam_toolkit_wrapper",
                port=7015,
            ),
            "ui_tars": ToolConfig(
                name="UI-TARS",
                executable_path=str(
                    self.project_root
                    / "tools"
                    / "UI-TARS"
                    / "apps"
                    / "ui-tars"
                    / "src"
                    / "main"
                    / "main.ts"
                ),
                wrapper_module="integrations.tools.ui_tars_wrapper",
                port=7016,
                optional=True,
            ),
            "web_check": ToolConfig(
                name="Web-Check",
                executable_path=str(
                    self.project_root / "tools" / "Web-Check" / "server.js"
                ),
                wrapper_module="integrations.tools.web_check_wrapper",
                port=7017,
                optional=True,
            ),
        }

    def load_config(self) -> None:
        """Load tool configurations from file or use defaults"""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    config_data = json.load(f)

                self.tool_configs = {}
                for name, data in config_data.items():
                    self.tool_configs[name] = ToolConfig(**data)

                self.logger.info(
                    f"Loaded configuration for {len(self.tool_configs)} tools"
                )
            except Exception as e:
                self.logger.warning(f"Failed to load config file: {e}, using defaults")
                self.tool_configs = self._load_default_configs()
        else:
            self.logger.info("No config file found, using default configurations")
            self.tool_configs = self._load_default_configs()

    def save_config(self) -> None:
        """Save current tool configurations to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            config_data = {}
            for name, config in self.tool_configs.items():
                config_data[name] = {
                    "name": config.name,
                    "executable_path": config.executable_path,
                    "wrapper_module": config.wrapper_module,
                    "config_file": config.config_file,
                    "port": config.port,
                    "dependencies": config.dependencies,
                    "enabled": config.enabled,
                }

            with open(self.config_path, "w") as f:
                json.dump(config_data, f, indent=2)

            self.logger.info(f"Saved configuration to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")

    def _load_wrapper_module(self, module_path: str) -> Optional[type]:
        """Dynamically load a wrapper module"""
        try:
            spec = importlib.util.spec_from_file_location("wrapper", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Look for a class that inherits from BaseToolWrapper
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseToolWrapper)
                    and attr != BaseToolWrapper
                ):
                    return attr

            self.logger.warning(f"No wrapper class found in {module_path}")
            return None

        except Exception as e:
            self.logger.error(f"Failed to load wrapper module {module_path}: {e}")
            return None

    async def initialize_tool(self, tool_name: str) -> bool:
        """Initialize a specific tool"""
        if tool_name not in self.tool_configs:
            self.logger.error(f"Unknown tool: {tool_name}")
            return False

        config = self.tool_configs[tool_name]

        if not config.enabled:
            self.logger.info(f"Tool {tool_name} is disabled, skipping")
            return True

        # Check if executable exists
        if not Path(config.executable_path).exists():
            self.logger.warning(
                f"Executable not found for {tool_name}: {config.executable_path}"
            )
            return False

        try:
            # Load wrapper if specified
            if config.wrapper_module:
                wrapper_path = (
                    self.project_root / config.wrapper_module.replace(".", "/") + ".py"
                )
                wrapper_class = self._load_wrapper_module(str(wrapper_path))

                if wrapper_class:
                    tool_instance = wrapper_class(config)
                    if await tool_instance.initialize():
                        self.tools[tool_name] = tool_instance
                        self.logger.info(f"Initialized tool: {tool_name}")
                        return True
                    else:
                        self.logger.error(f"Failed to initialize tool: {tool_name}")
                        return False
                else:
                    self.logger.error(f"Failed to load wrapper for: {tool_name}")
                    return False
            else:
                # Create a generic wrapper for tools without specific wrappers
                tool_instance = GenericToolWrapper(config)
                if await tool_instance.initialize():
                    self.tools[tool_name] = tool_instance
                    self.logger.info(f"Initialized generic wrapper for: {tool_name}")
                    return True
                else:
                    self.logger.error(
                        f"Failed to initialize generic wrapper for: {tool_name}"
                    )
                    return False

        except Exception as e:
            self.logger.error(f"Error initializing tool {tool_name}: {e}")
            return False

    async def initialize_all(self) -> Dict[str, bool]:
        """Initialize all tools"""
        self.load_config()
        results = {}

        self.logger.info("Initializing all tools...")

        for tool_name in self.tool_configs.keys():
            results[tool_name] = await self.initialize_tool(tool_name)

        successful = sum(1 for success in results.values() if success)
        total = len(results)

        self.logger.info(
            f"Tool initialization completed: {successful}/{total} successful"
        )
        return results

    async def execute_tool_command(
        self, tool_name: str, command: str, **kwargs
    ) -> Dict[str, Any]:
        """Execute a command with a specific tool"""
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool {tool_name} not initialized",
                "data": None,
            }

        try:
            return await self.tools[tool_name].execute_command(command, **kwargs)
        except Exception as e:
            self.logger.error(f"Error executing command with {tool_name}: {e}")
            return {"success": False, "error": str(e), "data": None}

    async def health_check_all(self) -> Dict[str, bool]:
        """Perform health check on all tools"""
        results = {}

        for tool_name, tool in self.tools.items():
            try:
                results[tool_name] = await tool.health_check()
            except Exception as e:
                self.logger.error(f"Health check failed for {tool_name}: {e}")
                results[tool_name] = False

        return results

    async def cleanup_all(self) -> None:
        """Cleanup all tools"""
        for tool_name, tool in self.tools.items():
            try:
                await tool.cleanup()
                self.logger.info(f"Cleaned up tool: {tool_name}")
            except Exception as e:
                self.logger.error(f"Error cleaning up {tool_name}: {e}")

        self.tools.clear()

    def get_tool_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all tools"""
        status = {}

        for tool_name, config in self.tool_configs.items():
            tool_status = {
                "name": config.name,
                "enabled": config.enabled,
                "executable_exists": Path(config.executable_path).exists(),
                "initialized": tool_name in self.tools,
                "port": config.port,
            }
            status[tool_name] = tool_status

        return status


class GenericToolWrapper(BaseToolWrapper):
    """Generic wrapper for tools without specific wrappers"""

    async def initialize(self) -> bool:
        """Initialize the generic tool wrapper"""
        executable_path = Path(self.config.executable_path)
        return executable_path.exists() and executable_path.is_file()

    async def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute a command with the tool"""
        try:
            cmd = [self.config.executable_path] + command.split()
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=kwargs.get("timeout", 300)
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "data": {"raw_output": result.stdout},
            }

        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out", "data": None}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}

    async def health_check(self) -> bool:
        """Check if the tool is healthy"""
        executable_path = Path(self.config.executable_path)
        return executable_path.exists()


async def main():
    """CLI interface for integration manager"""
    import argparse

    parser = argparse.ArgumentParser(description="LANCELOTT Integration Manager")
    parser.add_argument(
        "action",
        choices=["init", "status", "health", "test", "cleanup"],
        help="Action to perform",
    )
    parser.add_argument("--tool", "-t", help="Specific tool to operate on")
    parser.add_argument("--config", "-c", help="Configuration file path")

    args = parser.parse_args()

    try:
        manager = IntegrationManager(args.config)

        if args.action == "init":
            if args.tool:
                success = await manager.initialize_tool(args.tool)
                print(
                    f"Tool {args.tool} initialization: {'success' if success else 'failed'}"
                )
            else:
                results = await manager.initialize_all()
                print("Initialization results:")
                for tool, success in results.items():
                    print(f"  {tool}: {'success' if success else 'failed'}")

        elif args.action == "status":
            status = manager.get_tool_status()
            print("Tool Status:")
            print("=" * 80)
            for tool, info in status.items():
                print(
                    f"{tool:15} | {info['name']:20} | "
                    f"Enabled: {info['enabled']} | "
                    f"Executable: {info['executable_exists']} | "
                    f"Initialized: {info['initialized']} | "
                    f"Port: {info['port']}"
                )

        elif args.action == "health":
            results = await manager.health_check_all()
            print("Health Check Results:")
            for tool, healthy in results.items():
                status = "healthy" if healthy else "unhealthy"
                print(f"  {tool}: {status}")

        elif args.action == "cleanup":
            await manager.cleanup_all()
            print("Cleanup completed")

        elif args.action == "test":
            if args.tool:
                result = await manager.execute_tool_command(args.tool, "--help")
                print(f"Test result for {args.tool}:")
                print(json.dumps(result, indent=2))
            else:
                print("Please specify a tool to test with --tool")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
