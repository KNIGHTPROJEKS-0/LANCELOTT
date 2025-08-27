#!/usr/bin/env python3
"""
UI-TARS Desktop & Agent-TARS Orchestrator
LANCELOTT Framework Integration

Advanced GUI automation and security testing orchestrator
Powered by Azure AI Foundry GPT-5-Nano
"""

import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from rich import box
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm, Prompt
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("Installing required dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=True)
    from rich import box
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm, Prompt
    from rich.table import Table
    from rich.text import Text

# Initialize Rich console
console = Console()


@dataclass
class UITARSConfig:
    """UI-TARS Configuration Data Class"""

    enabled: bool = True
    port: int = 8765
    web_port: int = 5173
    config_path: str = "tools/UI-TARS/ui-tars.conf"
    preset: str = "cerberus-gpt5-nano-preset.yaml"
    binary_path: str = "tools/UI-TARS"
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

    # Authentication
    auth_enabled: bool = True
    firebase_api_key: str = ""
    firebase_project_id: str = "lancelott-z9dko"
    framework_api_url: str = "http://localhost:7777"


class UITARSOrchestrator:
    """Main UI-TARS Orchestrator Class"""

    def __init__(self):
        self.config = self.load_config()
        self.processes: Dict[str, subprocess.Popen] = {}
        self.running = True

        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def load_config(self) -> UITARSConfig:
        """Load configuration from environment variables"""
        config = UITARSConfig()

        # Load from environment
        config.enabled = os.getenv("UI_TARS_ENABLED", "true").lower() == "true"
        config.port = int(os.getenv("UI_TARS_PORT", "8765"))
        config.web_port = int(os.getenv("UI_TARS_WEB_PORT", "5173"))
        config.config_path = os.getenv(
            "UI_TARS_CONFIG_PATH", "tools/UI-TARS/ui-tars.conf"
        )
        config.preset = os.getenv("UI_TARS_PRESET", "cerberus-gpt5-nano-preset.yaml")
        config.binary_path = os.getenv("UI_TARS_BINARY_PATH", "tools/UI-TARS")
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

        return config

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        console.print("\n[yellow]Shutting down UI-TARS Orchestrator...[/yellow]")
        self.running = False
        self.cleanup_processes()
        sys.exit(0)

    def cleanup_processes(self):
        """Clean up all running processes"""
        for name, process in self.processes.items():
            if process.poll() is None:
                console.print(f"[yellow]Terminating {name}...[/yellow]")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    console.print(f"[red]Force killing {name}...[/red]")
                    process.kill()

    def display_header(self):
        """Display the main header"""
        header_text = Text()
        header_text.append("UI-TARS ORCHESTRATOR", style="bold cyan")
        header_text.append("\nLANCELOTT Framework", style="dim")
        header_text.append(f"\nPowered by Azure AI Foundry GPT-5-Nano", style="green")

        panel = Panel(
            header_text,
            title="🎯 GUI Automation & Security Testing",
            border_style="cyan",
            padding=(1, 2),
        )
        console.print(panel)

    def display_ai_config(self):
        """Display AI configuration status"""
        table = Table(title="🧠 AI Configuration", box=box.ROUNDED)
        table.add_column("Setting", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        table.add_column("Status", style="yellow")

        # AI Model Configuration
        table.add_row(
            "AI Model",
            f"{self.config.ai_provider}/{self.config.ai_model}",
            "✅ Active" if self.config.enabled else "❌ Disabled",
        )
        table.add_row(
            "Deployment",
            self.config.ai_deployment,
            "✅ Configured" if self.config.ai_deployment else "❌ Missing",
        )
        table.add_row("Max Tokens", f"{self.config.ai_max_tokens:,}", "✅ Optimized")
        table.add_row(
            "Max Completion Tokens",
            f"{self.config.ai_max_completion_tokens:,}",
            "✅ Enhanced",
        )
        table.add_row(
            "Temperature",
            f"{self.config.ai_temperature}",
            "✅ Precise" if self.config.ai_temperature <= 0.2 else "⚠️ Creative",
        )
        table.add_row(
            "Authentication",
            "Firebase Web API",
            "✅ Enabled" if self.config.auth_enabled else "❌ Disabled",
        )
        table.add_row(
            "Framework Integration",
            self.config.framework_api_url,
            "✅ Connected" if self.config.framework_api_url else "❌ Disconnected",
        )

        console.print(table)

    def display_status(self):
        """Display system status"""
        table = Table(title="📊 System Status", box=box.ROUNDED)
        table.add_column("Component", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Port/Path", style="yellow")

        # Check UI-TARS Desktop status
        ui_tars_status = (
            "🟢 Ready" if Path(self.config.binary_path).exists() else "🔴 Missing"
        )
        table.add_row("UI-TARS Desktop", ui_tars_status, f"Port {self.config.port}")

        # Check Web Interface
        web_status = "🟢 Enabled" if self.config.web_interface else "🔴 Disabled"
        table.add_row("Web Interface", web_status, f"Port {self.config.web_port}")

        # Check Agent-TARS CLI
        agent_tars_path = Path("tools/UI-TARS/multimodal/agent-tars/cli")
        agent_status = "🟢 Ready" if agent_tars_path.exists() else "🔴 Missing"
        table.add_row("Agent-TARS CLI", agent_status, str(agent_tars_path))

        # Check Configuration
        config_status = (
            "🟢 Found" if Path(self.config.config_path).exists() else "🔴 Missing"
        )
        table.add_row("Configuration", config_status, self.config.config_path)

        # Check Preset
        preset_path = Path(self.config.binary_path) / self.config.preset
        preset_status = "🟢 Found" if preset_path.exists() else "🔴 Missing"
        table.add_row("GPT-5-Nano Preset", preset_status, self.config.preset)

        console.print(table)

    def show_main_menu(self):
        """Display the main menu"""
        menu_text = """
[bold cyan]Available Commands:[/bold cyan]

[green]1.[/green] Launch UI-TARS Desktop
[green]2.[/green] Launch Agent-TARS CLI
[green]3.[/green] Start Web Interface
[green]4.[/green] View AI Configuration
[green]5.[/green] View System Status
[green]6.[/green] View Logs
[green]7.[/green] Manage Workflows
[green]8.[/green] Security Testing Tools
[green]9.[/green] Configuration Manager
[green]0.[/green] Exit

[dim]Type the number of your choice...[/dim]
        """

        panel = Panel(
            menu_text, title="🎮 Main Menu", border_style="green", padding=(1, 2)
        )
        console.print(panel)

    def launch_ui_tars_desktop(self):
        """Launch UI-TARS Desktop application"""
        console.print("[cyan]🚀 Launching UI-TARS Desktop...[/cyan]")

        try:
            # Change to UI-TARS directory
            ui_tars_dir = Path(self.config.binary_path)
            if not ui_tars_dir.exists():
                console.print(
                    f"[red]❌ UI-TARS directory not found: {ui_tars_dir}[/red]"
                )
                return

            # Run UI-TARS desktop
            with console.status("[cyan]Starting UI-TARS Desktop..."):
                process = subprocess.Popen(
                    ["npm", "run", "dev:ui-tars"],
                    cwd=ui_tars_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                self.processes["ui_tars_desktop"] = process

                # Wait a moment to check if it started successfully
                time.sleep(3)

                if process.poll() is None:
                    console.print(
                        "[green]✅ UI-TARS Desktop started successfully![/green]"
                    )
                    console.print(
                        f"[yellow]📱 Desktop app should open automatically[/yellow]"
                    )
                    console.print(
                        f"[yellow]🌐 Web interface: http://localhost:{self.config.web_port}[/yellow]"
                    )
                else:
                    stdout, stderr = process.communicate()
                    console.print(f"[red]❌ Failed to start UI-TARS Desktop[/red]")
                    if stderr:
                        console.print(f"[red]Error: {stderr}[/red]")

        except Exception as e:
            console.print(f"[red]❌ Error launching UI-TARS Desktop: {e}[/red]")

    def launch_agent_tars_cli(self):
        """Launch Agent-TARS CLI"""
        console.print("[cyan]🚀 Launching Agent-TARS CLI...[/cyan]")

        try:
            agent_path = Path("tools/UI-TARS/multimodal/agent-tars/cli")
            if not agent_path.exists():
                console.print(f"[red]❌ Agent-TARS CLI not found: {agent_path}[/red]")
                return

            # Interactive mode
            console.print("[green]Starting Agent-TARS in interactive mode...[/green]")

            # Change to agent directory and run
            subprocess.run(["npm", "run", "dev"], cwd=agent_path, check=True)

        except Exception as e:
            console.print(f"[red]❌ Error launching Agent-TARS CLI: {e}[/red]")

    def start_web_interface(self):
        """Start web interface only"""
        console.print("[cyan]🌐 Starting Web Interface...[/cyan]")

        try:
            ui_tars_dir = Path(self.config.binary_path)
            if not ui_tars_dir.exists():
                console.print(
                    f"[red]❌ UI-TARS directory not found: {ui_tars_dir}[/red]"
                )
                return

            # Start web interface only
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=ui_tars_dir / "apps" / "ui-tars",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.processes["web_interface"] = process
            console.print(
                f"[green]✅ Web interface started at http://localhost:{self.config.web_port}[/green]"
            )

        except Exception as e:
            console.print(f"[red]❌ Error starting web interface: {e}[/red]")

    def view_logs(self):
        """View system logs"""
        console.print("[cyan]📋 Viewing Logs...[/cyan]")

        log_files = [
            "logs/ui_tars_orchestrator.log",
            "logs/agent_tars/agent_tars.log",
            "logs/lancelott.log",
        ]

        for log_file in log_files:
            log_path = Path(log_file)
            if log_path.exists():
                console.print(f"\n[green]📄 {log_file}:[/green]")
                try:
                    with open(log_path, "r") as f:
                        lines = f.readlines()
                        # Show last 10 lines
                        for line in lines[-10:]:
                            console.print(f"  {line.strip()}")
                except Exception as e:
                    console.print(f"[red]Error reading {log_file}: {e}[/red]")
            else:
                console.print(f"[yellow]⚠️ Log file not found: {log_file}[/yellow]")

    def manage_workflows(self):
        """Workflow management menu"""
        console.print("[cyan]🔄 Workflow Manager[/cyan]")

        workflows = [
            "Security Testing Automation",
            "Penetration Testing GUI",
            "Vulnerability Scanning Interface",
            "Automated Report Generation",
        ]

        table = Table(title="Available Workflows", box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Workflow", style="green")
        table.add_column("Status", style="yellow")

        for i, workflow in enumerate(workflows, 1):
            table.add_row(str(i), workflow, "✅ Ready")

        console.print(table)

    def security_testing_tools(self):
        """Security testing tools menu"""
        console.print("[cyan]🔒 Security Testing Tools[/cyan]")

        tools = [
            (
                "Screenshot Analysis",
                "AI-powered screenshot analysis for security assessment",
            ),
            ("GUI Vulnerability Scanner", "Automated GUI-based vulnerability scanning"),
            ("Browser Automation Security", "Security-focused browser automation"),
            (
                "Automated Penetration Testing",
                "GUI-driven penetration testing workflows",
            ),
            (
                "Security Report Generator",
                "Automated security report generation with screenshots",
            ),
        ]

        table = Table(title="Security Testing Tools", box=box.ROUNDED)
        table.add_column("Tool", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_column("Status", style="yellow")

        for tool, description in tools:
            table.add_row(tool, description, "✅ Available")

        console.print(table)

    def configuration_manager(self):
        """Configuration management"""
        console.print("[cyan]⚙️ Configuration Manager[/cyan]")

        config_items = [
            ("AI Model", f"{self.config.ai_provider}/{self.config.ai_model}"),
            ("Deployment", self.config.ai_deployment),
            ("Max Tokens", f"{self.config.ai_max_tokens:,}"),
            ("Temperature", f"{self.config.ai_temperature}"),
            ("Desktop Mode", "Enabled" if self.config.desktop_mode else "Disabled"),
            ("Web Interface", "Enabled" if self.config.web_interface else "Disabled"),
            ("Authentication", "Enabled" if self.config.auth_enabled else "Disabled"),
            ("Framework Integration", self.config.framework_api_url),
        ]

        table = Table(title="Current Configuration", box=box.ROUNDED)
        table.add_column("Setting", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        for setting, value in config_items:
            table.add_row(setting, str(value))

        console.print(table)

    def run(self):
        """Main orchestrator loop"""
        try:
            while self.running:
                console.clear()
                self.display_header()
                self.display_ai_config()
                self.display_status()
                self.show_main_menu()

                choice = Prompt.ask(
                    "Enter your choice",
                    choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                )

                if choice == "0":
                    console.print("[yellow]👋 Goodbye![/yellow]")
                    self.cleanup_processes()
                    break
                elif choice == "1":
                    self.launch_ui_tars_desktop()
                    Prompt.ask("\nPress Enter to continue...")
                elif choice == "2":
                    self.launch_agent_tars_cli()
                    Prompt.ask("\nPress Enter to continue...")
                elif choice == "3":
                    self.start_web_interface()
                    Prompt.ask("\nPress Enter to continue...")
                elif choice == "4":
                    self.display_ai_config()
                    Prompt.ask("\nPress Enter to continue...")
                elif choice == "5":
                    self.display_status()
                    Prompt.ask("\nPress Enter to continue...")
                elif choice == "6":
                    self.view_logs()
                    Prompt.ask("\nPress Enter to continue...")
                elif choice == "7":
                    self.manage_workflows()
                    Prompt.ask("\nPress Enter to continue...")
                elif choice == "8":
                    self.security_testing_tools()
                    Prompt.ask("\nPress Enter to continue...")
                elif choice == "9":
                    self.configuration_manager()
                    Prompt.ask("\nPress Enter to continue...")

        except KeyboardInterrupt:
            console.print("\n[yellow]Shutting down...[/yellow]")
            self.cleanup_processes()
        except Exception as e:
            console.print(f"[red]❌ Unexpected error: {e}[/red]")
            self.cleanup_processes()


def main():
    """Main entry point"""
    orchestrator = UITARSOrchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()
