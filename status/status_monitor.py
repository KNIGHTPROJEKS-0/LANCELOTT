#!/usr/bin/env python3
"""
CERBERUS-FANGS LANCELOTT - Unified Status Monitor
Comprehensive monitoring system for all framework components
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import aiohttp
import psutil
import requests


@dataclass
class ComponentStatus:
    """Status information for a framework component"""

    name: str
    type: str  # 'tool', 'service', 'api', 'integration'
    status: str  # 'healthy', 'degraded', 'failed', 'unknown'
    last_check: datetime
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = None
    port: Optional[int] = None
    pid: Optional[int] = None


@dataclass
class SystemMetrics:
    """System-wide metrics"""

    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_connections: int
    active_processes: int
    uptime: float


class StatusMonitor:
    """Unified status monitoring for LANCELOTT framework"""

    def __init__(self, config_path: str = None):
        self.project_root = Path(__file__).parent.parent.parent
        self.config_path = (
            config_path or self.project_root / "config" / "monitoring.json"
        )
        self.logger = self._setup_logging()
        self.components: Dict[str, ComponentStatus] = {}
        self.monitoring_config = self._load_monitoring_config()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for status monitor"""
        log_path = self.project_root / "logs" / "monitoring.log"
        log_path.parent.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        )
        return logging.getLogger(__name__)

    def _load_monitoring_config(self) -> Dict[str, Any]:
        """Load monitoring configuration"""
        default_config = {
            "check_interval": 30,  # seconds
            "timeout": 10,  # seconds
            "retry_attempts": 3,
            "components": {
                "fastapi": {
                    "type": "api",
                    "url": "http://localhost:7777/health",
                    "port": 7777,
                    "critical": True,
                },
                "n8n": {
                    "type": "service",
                    "url": "http://localhost:5678/healthz",
                    "port": 5678,
                    "critical": False,
                },
                "supergateway": {
                    "type": "integration",
                    "url": "http://localhost:3000/health",
                    "port": 3000,
                    "critical": True,
                },
                "supercompat": {
                    "type": "integration",
                    "url": "http://localhost:3001/health",
                    "port": 3001,
                    "critical": True,
                },
            },
            "tools": {
                "nmap": {"port": 7001, "executable": "nmap/nmap"},
                "argus": {"port": 7002, "executable": "tools/Argus/argus.py"},
                "kraken": {"port": 7003, "executable": "tools/Kraken/kraken.py"},
                "metabigor": {"port": 7004, "executable": "tools/Metabigor/metabigor"},
                "osmedeus": {"port": 7005, "executable": "tools/Osmedeus/osmedeus"},
                "spiderfoot": {"port": 7006, "executable": "tools/Spiderfoot/sf.py"},
                "social_analyzer": {
                    "port": 7007,
                    "executable": "tools/Social-Analyzer/app.py",
                },
                "phonesploit": {
                    "port": 7008,
                    "executable": "tools/PhoneSploit-Pro/phonesploitpro.py",
                },
                "vajra": {"port": 7009, "executable": "tools/Vajra/vajra.py"},
                "storm_breaker": {
                    "port": 7010,
                    "executable": "tools/Storm-Breaker/st.py",
                },
                "dismap": {"port": 7011, "executable": "tools/dismap/dismap"},
                "hydra": {"port": 7012, "executable": "tools/THC-Hydra/hydra"},
                "webstor": {"port": 7013, "executable": "tools/Webstor/webstor.py"},
                "sherlock": {
                    "port": 7014,
                    "executable": "tools/SHERLOCK/sherlock_project/sherlock.py",
                },
                "redteam_toolkit": {
                    "port": 7015,
                    "executable": "tools/RedTeam-ToolKit/manage.py",
                },
                "ui_tars": {
                    "port": 7016,
                    "executable": "tools/UI-TARS/apps/ui-tars/src/main/main.ts",
                },
                "web_check": {"port": 7017, "executable": "tools/Web-Check/server.js"},
            },
        }

        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}, using defaults")

        return default_config

    def save_monitoring_config(self) -> None:
        """Save monitoring configuration to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(self.monitoring_config, f, indent=2)
            self.logger.info(f"Saved monitoring config to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")

    async def check_url_health(self, url: str, timeout: int = 10) -> ComponentStatus:
        """Check health of a URL-based component"""
        start_time = time.time()

        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as session:
                async with session.get(url) as response:
                    response_time = time.time() - start_time

                    if response.status == 200:
                        status = "healthy"
                        error_message = None
                    else:
                        status = "degraded"
                        error_message = f"HTTP {response.status}"

                    return ComponentStatus(
                        name=url.split("/")[2],  # Extract hostname:port
                        type="api",
                        status=status,
                        last_check=datetime.now(),
                        response_time=response_time,
                        error_message=error_message,
                    )

        except asyncio.TimeoutError:
            return ComponentStatus(
                name=url.split("/")[2],
                type="api",
                status="failed",
                last_check=datetime.now(),
                error_message="Timeout",
            )
        except Exception as e:
            return ComponentStatus(
                name=url.split("/")[2],
                type="api",
                status="failed",
                last_check=datetime.now(),
                error_message=str(e),
            )

    def check_port_health(self, port: int, host: str = "localhost") -> bool:
        """Check if a port is open and listening"""
        import socket

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                result = sock.connect_ex((host, port))
                return result == 0
        except Exception:
            return False

    def check_process_health(self, executable_path: str) -> Optional[int]:
        """Check if a process is running by executable path"""
        full_path = self.project_root / executable_path

        try:
            for proc in psutil.process_iter(["pid", "name", "exe", "cmdline"]):
                try:
                    if proc.info["exe"] and str(full_path) in proc.info["exe"]:
                        return proc.info["pid"]
                    if proc.info["cmdline"]:
                        for cmd_part in proc.info["cmdline"]:
                            if str(full_path) in cmd_part:
                                return proc.info["pid"]
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            self.logger.warning(f"Error checking process for {executable_path}: {e}")

        return None

    def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        return SystemMetrics(
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent,
            disk_percent=psutil.disk_usage("/").percent,
            network_connections=len(psutil.net_connections()),
            active_processes=len(psutil.pids()),
            uptime=time.time() - psutil.boot_time(),
        )

    async def check_all_components(self) -> Dict[str, ComponentStatus]:
        """Check health of all monitored components"""
        results = {}

        # Check API and service components
        for name, config in self.monitoring_config.get("components", {}).items():
            if "url" in config:
                status = await self.check_url_health(
                    config["url"], self.monitoring_config["timeout"]
                )
                status.name = name
                status.type = config["type"]
                status.port = config.get("port")
                results[name] = status

        # Check tools
        for name, config in self.monitoring_config.get("tools", {}).items():
            executable = config.get("executable", "")
            port = config.get("port")

            # Check if executable exists
            executable_path = self.project_root / executable
            executable_exists = executable_path.exists()

            # Check if process is running
            pid = self.check_process_health(executable) if executable_exists else None

            # Check if port is listening
            port_open = self.check_port_health(port) if port else False

            # Determine status
            if executable_exists and (pid or port_open):
                status = "healthy"
                error_message = None
            elif executable_exists and not pid and not port_open:
                status = "degraded"
                error_message = "Process not running"
            elif not executable_exists:
                status = "failed"
                error_message = "Executable not found"
            else:
                status = "unknown"
                error_message = "Unable to determine status"

            results[name] = ComponentStatus(
                name=name,
                type="tool",
                status=status,
                last_check=datetime.now(),
                port=port,
                pid=pid,
                error_message=error_message,
            )

        self.components = results
        return results

    async def continuous_monitoring(self, duration: Optional[int] = None) -> None:
        """Run continuous monitoring"""
        self.logger.info("Starting continuous monitoring...")
        start_time = time.time()

        try:
            while True:
                # Check all components
                await self.check_all_components()

                # Log status summary
                healthy = sum(
                    1
                    for status in self.components.values()
                    if status.status == "healthy"
                )
                total = len(self.components)
                self.logger.info(
                    f"Status check completed: {healthy}/{total} components healthy"
                )

                # Break if duration specified and reached
                if duration and (time.time() - start_time) >= duration:
                    break

                # Wait for next check
                await asyncio.sleep(self.monitoring_config["check_interval"])

        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Error in continuous monitoring: {e}")

    def generate_status_report(self, output_format: str = "text") -> Union[str, Dict]:
        """Generate a comprehensive status report"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "system_metrics": asdict(self.get_system_metrics()),
            "components": {
                name: asdict(status) for name, status in self.components.items()
            },
            "summary": {
                "total_components": len(self.components),
                "healthy": sum(
                    1 for s in self.components.values() if s.status == "healthy"
                ),
                "degraded": sum(
                    1 for s in self.components.values() if s.status == "degraded"
                ),
                "failed": sum(
                    1 for s in self.components.values() if s.status == "failed"
                ),
                "unknown": sum(
                    1 for s in self.components.values() if s.status == "unknown"
                ),
            },
        }

        if output_format == "json":
            return report_data
        elif output_format == "text":
            return self._format_text_report(report_data)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    def _format_text_report(self, report_data: Dict) -> str:
        """Format report data as text"""
        lines = []
        lines.append("🐺 CERBERUS-FANGS LANCELOTT - STATUS REPORT 🐺")
        lines.append("=" * 60)
        lines.append(f"Generated: {report_data['timestamp']}")
        lines.append("")

        # System metrics
        metrics = report_data["system_metrics"]
        lines.append("📊 SYSTEM METRICS")
        lines.append("-" * 20)
        lines.append(f"CPU Usage:     {metrics['cpu_percent']:.1f}%")
        lines.append(f"Memory Usage:  {metrics['memory_percent']:.1f}%")
        lines.append(f"Disk Usage:    {metrics['disk_percent']:.1f}%")
        lines.append(f"Connections:   {metrics['network_connections']}")
        lines.append(f"Processes:     {metrics['active_processes']}")
        lines.append(f"Uptime:        {metrics['uptime']:.0f} seconds")
        lines.append("")

        # Summary
        summary = report_data["summary"]
        lines.append("📈 COMPONENT SUMMARY")
        lines.append("-" * 20)
        lines.append(f"Total:    {summary['total_components']}")
        lines.append(f"Healthy:  {summary['healthy']} ✅")
        lines.append(f"Degraded: {summary['degraded']} ⚠️")
        lines.append(f"Failed:   {summary['failed']} ❌")
        lines.append(f"Unknown:  {summary['unknown']} ❓")
        lines.append("")

        # Component details
        lines.append("🔧 COMPONENT DETAILS")
        lines.append("-" * 20)

        for name, component in report_data["components"].items():
            status_icon = {
                "healthy": "✅",
                "degraded": "⚠️",
                "failed": "❌",
                "unknown": "❓",
            }.get(component["status"], "❓")

            port_info = f":{component['port']}" if component["port"] else ""
            response_time = (
                f" ({component['response_time']:.3f}s)"
                if component["response_time"]
                else ""
            )
            error_info = (
                f" - {component['error_message']}" if component["error_message"] else ""
            )

            lines.append(
                f"{status_icon} {name:15} | {component['type']:12} | "
                f"{component['status']:8}{port_info}{response_time}{error_info}"
            )

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

    def save_report(self, filename: str = None, output_format: str = "json") -> str:
        """Save status report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"status_report_{timestamp}.{output_format}"

        report_path = self.project_root / "status" / "reporting" / filename
        report_path.parent.mkdir(parents=True, exist_ok=True)

        report = self.generate_status_report(output_format)

        try:
            if output_format == "json":
                with open(report_path, "w") as f:
                    json.dump(report, f, indent=2, default=str)
            else:
                with open(report_path, "w") as f:
                    f.write(report)

            self.logger.info(f"Status report saved to {report_path}")
            return str(report_path)

        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")
            raise


async def main():
    """CLI interface for status monitor"""
    import argparse

    parser = argparse.ArgumentParser(description="LANCELOTT Status Monitor")
    parser.add_argument(
        "action",
        choices=["check", "monitor", "report", "save"],
        help="Action to perform",
    )
    parser.add_argument(
        "--format", "-f", choices=["text", "json"], default="text", help="Output format"
    )
    parser.add_argument(
        "--duration", "-d", type=int, help="Monitoring duration in seconds"
    )
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--config", "-c", help="Configuration file path")

    args = parser.parse_args()

    try:
        monitor = StatusMonitor(args.config)

        if args.action == "check":
            await monitor.check_all_components()
            report = monitor.generate_status_report(args.format)
            print(report)

        elif args.action == "monitor":
            await monitor.continuous_monitoring(args.duration)

        elif args.action == "report":
            await monitor.check_all_components()
            report = monitor.generate_status_report(args.format)
            print(report)

        elif args.action == "save":
            await monitor.check_all_components()
            filepath = monitor.save_report(args.output, args.format)
            print(f"Report saved to: {filepath}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
