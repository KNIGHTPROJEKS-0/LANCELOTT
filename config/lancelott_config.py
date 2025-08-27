#!/usr/bin/env python3
"""
LANCELOTT - Unified Configuration System
Centralized configuration management for all framework components
"""

import json
import logging
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml


@dataclass
class ToolConfiguration:
    """Configuration for individual security tools"""

    name: str
    executable_path: str
    wrapper_module: Optional[str] = None
    config_file: Optional[str] = None
    port: Optional[int] = None
    dependencies: Optional[List[str]] = None
    enabled: bool = True
    optional: bool = False
    build_type: Optional[str] = None  # 'python', 'go', 'node', 'shell'
    build_command: Optional[List[str]] = None
    environment_vars: Optional[Dict[str, str]] = None


@dataclass
class APIConfiguration:
    """Configuration for API components"""

    host: str = "0.0.0.0"
    port: int = 7777
    debug: bool = False
    workers: int = 4
    cors_origins: Optional[List[str]] = None
    auth_enabled: bool = True
    rate_limiting: bool = True
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None


@dataclass
class DatabaseConfiguration:
    """Database configuration"""

    type: str = "sqlite"  # 'sqlite', 'postgresql', 'mysql'
    host: str = "localhost"
    port: int = 5432
    database: str = "lancelott"
    username: str = "lancelott_user"
    password: str = "lancelott_pass"
    url: Optional[str] = None


@dataclass
class SecurityConfiguration:
    """Security configuration"""

    jwt_secret: str = "your-secret-key-change-in-production"
    jwt_expiration: int = 3600  # seconds
    api_key_length: int = 32
    password_min_length: int = 8
    max_login_attempts: int = 5
    lockout_duration: int = 300  # seconds


@dataclass
class IntegrationConfiguration:
    """Configuration for external integrations"""

    n8n_url: str = "http://localhost:5678"
    n8n_auth_user: str = "admin"
    n8n_auth_password: str = "lancelott"
    supergateway_url: str = "http://localhost:3000"
    supercompat_url: str = "http://localhost:3001"
    webhook_base_url: str = "http://localhost:7777/webhooks"


@dataclass
class LoggingConfiguration:
    """Logging configuration"""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "logs/lancelott.log"
    max_file_size: int = 10  # MB
    backup_count: int = 5
    console_output: bool = True


@dataclass
class MonitoringConfiguration:
    """Monitoring configuration"""

    enabled: bool = True
    check_interval: int = 30  # seconds
    timeout: int = 10  # seconds
    retry_attempts: int = 3
    alert_email: Optional[str] = None
    alert_webhook: Optional[str] = None


class LancelottConfig:
    """Unified configuration manager for LANCELOTT framework"""

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or Path(__file__).parent)
        self.project_root = self.config_dir.parent
        self.config_file = self.config_dir / "lancelott.yaml"

        # Initialize configuration components
        self.api = APIConfiguration()
        self.database = DatabaseConfiguration()
        self.security = SecurityConfiguration()
        self.integrations = IntegrationConfiguration()
        self.logging = LoggingConfiguration()
        self.monitoring = MonitoringConfiguration()
        self.tools: Dict[str, ToolConfiguration] = {}

        # Setup logging
        self.logger = self._setup_logging()

        # Load configuration
        self.load_configuration()

    def _setup_logging(self) -> logging.Logger:
        """Setup basic logging"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        return logging.getLogger(__name__)

    def _load_default_tool_configs(self) -> Dict[str, ToolConfiguration]:
        """Load default tool configurations with new paths"""
        return {
            # Go-based tools
            "metabigor": ToolConfiguration(
                name="Metabigor",
                executable_path="tools/Metabigor/metabigor",
                wrapper_module="integrations.tools.metabigor_wrapper",
                port=7004,
                dependencies=["go"],
                build_type="go",
                build_command=["go", "build", "-o", "metabigor", "."],
            ),
            "osmedeus": ToolConfiguration(
                name="Osmedeus",
                executable_path="tools/Osmedeus/osmedeus",
                wrapper_module="integrations.tools.osmedeus_wrapper",
                port=7005,
                dependencies=["go"],
                build_type="go",
                build_command=["go", "build", "-o", "osmedeus", "."],
            ),
            "dismap": ToolConfiguration(
                name="Dismap",
                executable_path="tools/dismap/dismap",
                wrapper_module="integrations.tools.dismap_wrapper",
                port=7011,
                dependencies=["go"],
                build_type="go",
                build_command=["go", "build", "-o", "dismap", "."],
            ),
            # Python-based tools
            "argus": ToolConfiguration(
                name="Argus",
                executable_path="tools/Argus/argus.py",
                wrapper_module="integrations.tools.argus_wrapper",
                port=7002,
                dependencies=["python3", "pip"],
                build_type="python",
                build_command=["pip", "install", "-r", "requirements.txt"],
            ),
            "kraken": ToolConfiguration(
                name="Kraken",
                executable_path="tools/Kraken/kraken.py",
                wrapper_module="integrations.tools.kraken_wrapper",
                port=7003,
                dependencies=["python3", "pip"],
                build_type="python",
                build_command=["pip", "install", "-r", "requirements.txt"],
            ),
            "spiderfoot": ToolConfiguration(
                name="SpiderFoot",
                executable_path="tools/Spiderfoot/sf.py",
                wrapper_module="integrations.tools.spiderfoot_wrapper",
                port=7006,
                dependencies=["python3", "pip"],
                build_type="python",
                build_command=["pip", "install", "-r", "requirements.txt"],
            ),
            "social_analyzer": ToolConfiguration(
                name="Social-Analyzer",
                executable_path="tools/Social-Analyzer/app.py",
                wrapper_module="integrations.tools.social_analyzer_wrapper",
                port=7007,
                dependencies=["python3", "pip"],
                build_type="python",
                build_command=["pip", "install", "-r", "requirements.txt"],
            ),
            "phonesploit": ToolConfiguration(
                name="PhoneSploit-Pro",
                executable_path="tools/PhoneSploit-Pro/phonesploitpro.py",
                wrapper_module="integrations.tools.phonesploit_wrapper",
                port=7008,
                dependencies=["python3", "pip"],
                build_type="python",
                build_command=["pip", "install", "-r", "requirements.txt"],
                optional=True,
            ),
            "vajra": ToolConfiguration(
                name="Vajra",
                executable_path="tools/Vajra/vajra.py",
                wrapper_module="integrations.tools.vajra_wrapper",
                port=7009,
                dependencies=["python3", "pip"],
                build_type="python",
                build_command=["pip", "install", "-r", "requirements.txt"],
            ),
            "storm_breaker": ToolConfiguration(
                name="Storm-Breaker",
                executable_path="tools/Storm-Breaker/st.py",
                wrapper_module="integrations.tools.storm_breaker_wrapper",
                port=7010,
                dependencies=["python3", "pip"],
                build_type="python",
                build_command=["pip", "install", "-r", "requirements.txt"],
                optional=True,
            ),
            "webstor": ToolConfiguration(
                name="Webstor",
                executable_path="tools/Webstor/webstor.py",
                wrapper_module="integrations.tools.webstor_wrapper",
                port=7013,
                dependencies=["python3", "pip"],
                build_type="python",
                build_command=["pip", "install", "-r", "requirements.txt"],
                optional=True,
            ),
            "sherlock": ToolConfiguration(
                name="SHERLOCK",
                executable_path="tools/SHERLOCK/sherlock_project/sherlock.py",
                wrapper_module="integrations.tools.sherlock_wrapper",
                port=7014,
                dependencies=["python3", "pip"],
                build_type="python",
                build_command=["pip", "install", "-r", "requirements.txt"],
            ),
            "redteam_toolkit": ToolConfiguration(
                name="RedTeam-ToolKit",
                executable_path="tools/RedTeam-ToolKit/manage.py",
                wrapper_module="integrations.tools.redteam_toolkit_wrapper",
                port=7015,
                dependencies=["python3", "pip"],
                build_type="python",
                build_command=["pip", "install", "-r", "requirements.txt"],
            ),
            # Node.js/TypeScript tools
            "ui_tars": ToolConfiguration(
                name="UI-TARS",
                executable_path="tools/UI-TARS/apps/ui-tars/src/main/main.ts",
                wrapper_module="integrations.tools.ui_tars_wrapper",
                port=7016,
                dependencies=["node", "npm"],
                build_type="node",
                build_command=["npm", "install", "&&", "npm", "run", "build"],
                optional=True,
            ),
            "web_check": ToolConfiguration(
                name="Web-Check",
                executable_path="tools/Web-Check/server.js",
                wrapper_module="integrations.tools.web_check_wrapper",
                port=7017,
                dependencies=["node", "npm"],
                build_type="node",
                build_command=["npm", "install", "&&", "npm", "run", "build"],
                optional=True,
            ),
            # C-based tools
            "thc_hydra": ToolConfiguration(
                name="THC-Hydra",
                executable_path="tools/THC-Hydra/hydra",
                wrapper_module="integrations.tools.hydra_wrapper",
                port=7012,
                dependencies=["gcc", "make"],
                build_type="shell",
                build_command=["./configure", "&&", "make"],
            ),
            # Core tools (outside tools directory)
            "nmap": ToolConfiguration(
                name="Nmap",
                executable_path="nmap/nmap",
                wrapper_module="integrations.tools.nmap_wrapper",
                port=7001,
                dependencies=["gcc", "make"],
                build_type="shell",
                build_command=["./configure", "&&", "make"],
                optional=True,
            ),
        }

    def load_configuration(self) -> None:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    config_data = yaml.safe_load(f)

                # Load each configuration section
                if "api" in config_data:
                    self.api = APIConfiguration(**config_data["api"])

                if "database" in config_data:
                    self.database = DatabaseConfiguration(**config_data["database"])

                if "security" in config_data:
                    self.security = SecurityConfiguration(**config_data["security"])

                if "integrations" in config_data:
                    self.integrations = IntegrationConfiguration(
                        **config_data["integrations"]
                    )

                if "logging" in config_data:
                    self.logging = LoggingConfiguration(**config_data["logging"])

                if "monitoring" in config_data:
                    self.monitoring = MonitoringConfiguration(
                        **config_data["monitoring"]
                    )

                # Load tool configurations
                if "tools" in config_data:
                    self.tools = {}
                    for name, tool_data in config_data["tools"].items():
                        self.tools[name] = ToolConfiguration(**tool_data)
                else:
                    self.tools = self._load_default_tool_configs()

                self.logger.info("Configuration loaded successfully")

            except Exception as e:
                self.logger.warning(
                    f"Failed to load configuration: {e}, using defaults"
                )
                self.tools = self._load_default_tool_configs()
        else:
            self.logger.info("No configuration file found, using defaults")
            self.tools = self._load_default_tool_configs()

    def save_configuration(self) -> None:
        """Save current configuration to file"""
        try:
            config_data = {
                "api": asdict(self.api),
                "database": asdict(self.database),
                "security": asdict(self.security),
                "integrations": asdict(self.integrations),
                "logging": asdict(self.logging),
                "monitoring": asdict(self.monitoring),
                "tools": {name: asdict(tool) for name, tool in self.tools.items()},
            }

            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, "w") as f:
                yaml.dump(config_data, f, default_flow_style=False, indent=2)

            self.logger.info(f"Configuration saved to {self.config_file}")

        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")

    def get_tool_config(self, tool_name: str) -> Optional[ToolConfiguration]:
        """Get configuration for a specific tool"""
        return self.tools.get(tool_name)

    def get_enabled_tools(self) -> Dict[str, ToolConfiguration]:
        """Get all enabled tools"""
        return {name: config for name, config in self.tools.items() if config.enabled}

    def get_tools_by_type(self, build_type: str) -> Dict[str, ToolConfiguration]:
        """Get tools by build type"""
        return {
            name: config
            for name, config in self.tools.items()
            if config.build_type == build_type
        }

    def validate_configuration(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []

        # Validate tool paths
        for name, tool in self.tools.items():
            if tool.enabled:
                tool_path = self.project_root / tool.executable_path
                if not tool_path.exists() and not tool.optional:
                    issues.append(f"Required tool {name} not found at {tool_path}")

        # Validate ports for conflicts
        used_ports: Dict[int, str] = {}
        for name, tool in self.tools.items():
            if tool.port and tool.enabled:
                if tool.port in used_ports:
                    issues.append(
                        f"Port conflict: {name} and {used_ports[tool.port]} both use port {tool.port}"
                    )
                else:
                    used_ports[tool.port] = name

        # Add API port to check
        if self.api.port in used_ports:
            issues.append(
                f"Port conflict: API and {used_ports[self.api.port]} both use port {self.api.port}"
            )

        return issues

    def generate_environment_file(self, output_path: Optional[str] = None) -> str:
        """Generate .env file with configuration"""
        if output_path is None:
            output_path = self.project_root / ".env.generated"

        env_vars = [
            "# LANCELOTT - Generated Configuration",
            f"# Generated at: {datetime.now()}",
            "",
            "# API Configuration",
            f"LANCELOTT_HOST={self.api.host}",
            f"LANCELOTT_PORT={self.api.port}",
            f"LANCELOTT_DEBUG={self.api.debug}",
            f"LANCELOTT_WORKERS={self.api.workers}",
            "",
            "# Database Configuration",
            f"DATABASE_TYPE={self.database.type}",
            f"DATABASE_HOST={self.database.host}",
            f"DATABASE_PORT={self.database.port}",
            f"DATABASE_NAME={self.database.database}",
            f"DATABASE_USER={self.database.username}",
            f"DATABASE_PASSWORD={self.database.password}",
            "",
            "# Security Configuration",
            f"JWT_SECRET={self.security.jwt_secret}",
            f"JWT_EXPIRATION={self.security.jwt_expiration}",
            "",
            "# Integration Configuration",
            f"N8N_URL={self.integrations.n8n_url}",
            f"N8N_AUTH_USER={self.integrations.n8n_auth_user}",
            f"N8N_AUTH_PASSWORD={self.integrations.n8n_auth_password}",
            f"SUPERGATEWAY_URL={self.integrations.supergateway_url}",
            f"SUPERCOMPAT_URL={self.integrations.supercompat_url}",
            "",
            "# Tool Ports",
        ]

        for name, tool in self.tools.items():
            if tool.enabled and tool.port:
                env_vars.append(f"{name.upper()}_PORT={tool.port}")

        env_content = "\n".join(env_vars)

        with open(output_path, "w") as f:
            f.write(env_content)

        self.logger.info(f"Environment file generated at {output_path}")
        return str(output_path)

    def update_tool_config(self, tool_name: str, **kwargs) -> bool:
        """Update configuration for a specific tool"""
        if tool_name not in self.tools:
            self.logger.error(f"Tool {tool_name} not found")
            return False

        tool_config = self.tools[tool_name]

        for key, value in kwargs.items():
            if hasattr(tool_config, key):
                setattr(tool_config, key, value)
            else:
                self.logger.warning(f"Unknown configuration key: {key}")

        self.logger.info(f"Updated configuration for tool: {tool_name}")
        return True

    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration"""
        return {
            "api": {
                "host": self.api.host,
                "port": self.api.port,
                "debug": self.api.debug,
            },
            "database": {
                "type": self.database.type,
                "host": self.database.host,
                "port": self.database.port,
            },
            "tools": {
                "total": len(self.tools),
                "enabled": len(self.get_enabled_tools()),
                "by_type": {
                    build_type: len(self.get_tools_by_type(build_type))
                    for build_type in ["python", "go", "node", "shell"]
                },
            },
            "validation_issues": len(self.validate_configuration()),
        }


# Global configuration instance
_config_instance = None


def get_config() -> LancelottConfig:
    """Get global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = LancelottConfig()
    return _config_instance


def reload_config() -> None:
    """Reload configuration"""
    global _config_instance
    _config_instance = None


if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="LANCELOTT Configuration Manager")
    parser.add_argument(
        "action",
        choices=["save", "validate", "summary", "env"],
        help="Action to perform",
    )
    parser.add_argument("--config-dir", help="Configuration directory path")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    config = LancelottConfig(args.config_dir)

    if args.action == "save":
        config.save_configuration()
        print("Configuration saved successfully")

    elif args.action == "validate":
        issues = config.validate_configuration()
        if issues:
            print("Configuration validation issues:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("Configuration validation passed")

    elif args.action == "summary":
        summary = config.get_configuration_summary()
        print("Configuration Summary:")
        print(
            f"  API: {summary['api']['host']}:{summary['api']['port']} (debug: {summary['api']['debug']})"
        )
        print(
            f"  Database: {summary['database']['type']} at {summary['database']['host']}:{summary['database']['port']}"
        )
        print(
            f"  Tools: {summary['tools']['enabled']}/{summary['tools']['total']} enabled"
        )
        print(f"  Build types: {summary['tools']['by_type']}")
        print(f"  Validation issues: {summary['validation_issues']}")

    elif args.action == "env":
        output_path = config.generate_environment_file(args.output)
        print(f"Environment file generated: {output_path}")
