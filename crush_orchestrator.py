#!/usr/bin/env python3
"""
Crush Orchestrator - Main Tool Initiator and Controller with CliWrap Integration
Terminal-based security framework controller using Crush CLI and CliWrap
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests  # type: ignore
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table
from rich.text import Text

# Add project imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from integrations.tools.cliwrap_wrapper import get_cliwrap_wrapper
    from integrations.tools.crush_wrapper import get_crush_wrapper

    WRAPPERS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Wrapper imports failed: {e}")
    WRAPPERS_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

console = Console()


class CrushOrchestrator:
    """Main orchestrator using Crush CLI and CliWrap for enhanced tool management"""

    def __init__(self):
        self.framework_url = "http://localhost:7777"
        self.crush_path = Path("tools/crush/crush")
        self.available_tools = []
        self.workflows = []
        self.crush_wrapper = None
        self.cliwrap_wrapper = None

        # AI Configuration for GPT-5-Nano
        self.ai_config = {
            "model": os.getenv("CRUSH_AI_MODEL", "gpt-5-nano"),
            "provider": os.getenv("CRUSH_AI_PROVIDER", "azure"),
            "deployment": os.getenv("CRUSH_AI_DEPLOYMENT", "GPT-5-Navo-Cerberus"),
            "endpoint": os.getenv(
                "CRUSH_AI_ENDPOINT",
                "https://gujil-mensn3og-eastus2.cognitiveservices.azure.com/openai/responses?api-version=2025-04-01-preview",
            ),
            "api_key": os.getenv(
                "CRUSH_AI_API_KEY", os.getenv("FOUNDRY_GPT5_NANO_API_KEY", "")
            ),
            "api_version": os.getenv("CRUSH_AI_API_VERSION", "2025-04-01-preview"),
        }

        # Initialize wrappers if available
        if WRAPPERS_AVAILABLE:
            try:
                # Import functions are available due to successful import
                self.crush_wrapper = get_crush_wrapper()  # type: ignore
                self.cliwrap_wrapper = get_cliwrap_wrapper()  # type: ignore
                console.print(
                    "[green]✅ Crush and CliWrap wrappers initialized[/green]"
                )
            except Exception as e:
                console.print(f"[yellow]⚠️ Wrapper initialization failed: {e}[/yellow]")

    async def initialize(self):
        """Initialize the orchestrator"""
        console.print(
            Panel.fit(
                "[bold cyan]🛡️ LANCELOTT Crush Orchestrator[/bold cyan]\n"
                "[yellow]Terminal-based Security Framework Controller[/yellow]",
                title="🚀 Starting",
            )
        )

        # Check if Crush is available
        if not self.crush_path.exists():
            console.print("[red]❌ Crush binary not found. Building...[/red]")
            await self.build_crush()

        # Check framework status
        await self.check_framework_status()

        # Load available tools
        await self.load_available_tools()

        # Load workflows
        await self.load_workflows()

    async def build_crush(self):
        """Build Crush from source"""
        try:
            console.print("[yellow]🔨 Building Crush CLI...[/yellow]")
            result = subprocess.run(
                ["go", "build", "-o", "crush", "."],
                cwd="tools/crush",
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                console.print(f"[red]❌ Crush build failed: {result.stderr}[/red]")
                sys.exit(1)

            console.print("[green]✅ Crush built successfully[/green]")

        except Exception as e:
            console.print(f"[red]❌ Failed to build Crush: {e}[/red]")
            sys.exit(1)

    async def check_framework_status(self):
        """Check if the main framework is running"""
        try:
            response = requests.get(f"{self.framework_url}/api/v1/health", timeout=5)
            if response.status_code == 200:
                console.print("[green]✅ LANCELOTT Framework is running[/green]")
                return True
            else:
                console.print("[yellow]⚠️ Framework is not healthy[/yellow]")
                return False
        except Exception as e:
            console.print(f"[red]❌ Framework is not running: {e}[/red]")
            console.print(
                "[yellow]💡 Start the framework first: python app.py[/yellow]"
            )
            return False

    async def load_available_tools(self):
        """Load available tools from the framework"""
        try:
            response = requests.get(
                f"{self.framework_url}/api/v1/tools/crush/tools/available", timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.available_tools = data.get("tools", [])
                console.print(
                    f"[green]✅ Loaded {len(self.available_tools)} available tools[/green]"
                )
            else:
                console.print("[yellow]⚠️ Could not load tools list[/yellow]")
        except Exception as e:
            console.print(f"[yellow]⚠️ Could not connect to framework API: {e}[/yellow]")

    async def load_workflows(self):
        """Load available workflows"""
        try:
            response = requests.get(
                f"{self.framework_url}/api/v1/tools/crush/workflows/list", timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.workflows = data.get("workflows", [])
                console.print(
                    f"[green]✅ Loaded {len(self.workflows)} workflows[/green]"
                )
        except Exception as e:
            console.print(f"[yellow]⚠️ Could not load workflows: {e}[/yellow]")

    def display_main_menu(self):
        """Display the main orchestrator menu"""
        console.clear()

        # Title panel
        console.print(
            Panel.fit(
                "[bold cyan]🛡️ LANCELOTT[/bold cyan]\n"
                "[yellow]Crush Orchestrator - Security Framework Controller[/yellow]\n"
                f"[green]🤖 AI Model: {self.ai_config['model']} ({self.ai_config['deployment']})[/green]",
                title="🚀 Main Menu",
            )
        )

        # Tools table
        tools_table = Table(title="📊 Available Security Tools", show_header=True)
        tools_table.add_column("Name", style="cyan")
        tools_table.add_column("Description", style="yellow")
        tools_table.add_column("Category", style="green")

        for tool in self.available_tools[:10]:  # Show first 10
            tools_table.add_row(
                tool.get("name", ""),
                tool.get("description", ""),
                tool.get("category", ""),
            )

        console.print(tools_table)

        # Menu options
        menu_panel = Panel(
            "[bold]🎮 Available Actions:[/bold]\n\n"
            "[cyan]1.[/cyan] 🚀 Launch Individual Tool\n"
            "[cyan]2.[/cyan] 🎯 Execute Multi-Tool Orchestration\n"
            "[cyan]3.[/cyan] 📋 Create Security Workflow\n"
            "[cyan]4.[/cyan] ▶️ Execute Existing Workflow\n"
            "[cyan]5.[/cyan] 📂 Browse Framework Files (Crush)\n"
            "[cyan]6.[/cyan] 📊 Framework Status Dashboard\n"
            "[cyan]7.[/cyan] 🔧 Tool Configuration\n"
            "[cyan]8.[/cyan] 📝 View Logs and Reports\n"
            "[cyan]9.[/cyan] 🏗️ Build and Manage Tools\n"
            "[cyan]0.[/cyan] 🚪 Exit\n",
            title="🎮 Control Panel",
        )
        console.print(menu_panel)

    async def launch_individual_tool(self):
        """Launch a single security tool"""
        console.print("[bold]🚀 Launch Individual Tool[/bold]")

        # Display tools
        for i, tool in enumerate(self.available_tools, 1):
            console.print(f"[cyan]{i}.[/cyan] {tool['name']} - {tool['description']}")

        try:
            choice = int(input("Select tool number: ")) - 1
            if 0 <= choice < len(self.available_tools):
                tool = self.available_tools[choice]
                target = input(f"Enter target for {tool['name']}: ")

                await self.execute_tool(tool["name"], target)
            else:
                console.print("[red]❌ Invalid selection[/red]")
        except (ValueError, KeyboardInterrupt):
            console.print("[yellow]⚠️ Operation cancelled[/yellow]")

    async def execute_tool(
        self, tool_name: str, target: str, options: Optional[Dict[str, Any]] = None
    ):
        """Execute a specific tool"""
        if options is None:
            options = {}

        console.print(f"[yellow]🔄 Executing {tool_name} on {target}...[/yellow]")

        try:
            # Use Crush API to orchestrate the tool
            payload = {"tools": [tool_name], "target": target, "options": options}

            response = requests.post(
                f"{self.framework_url}/api/v1/tools/crush/orchestrate",
                json=payload,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                console.print(f"[green]✅ {tool_name} execution completed[/green]")

                # Display results
                tool_result = result.get("results", {}).get(tool_name, {})
                if tool_result.get("success"):
                    console.print(f"[green]🎯 {tool_name} scan successful[/green]")
                else:
                    console.print(
                        f"[red]❌ {tool_name} scan failed: {tool_result.get('error')}[/red]"
                    )
            else:
                console.print(f"[red]❌ Tool execution failed: {response.text}[/red]")

        except Exception as e:
            console.print(f"[red]❌ Execution failed: {e}[/red]")

    async def execute_multi_tool_orchestration(self):
        """Execute multiple tools in orchestrated fashion"""
        console.print("[bold]🎯 Multi-Tool Orchestration[/bold]")

        # Let user select multiple tools
        console.print("Available tools:")
        for i, tool in enumerate(self.available_tools, 1):
            console.print(f"[cyan]{i}.[/cyan] {tool['name']}")

        tool_selections = input("Enter tool numbers (comma-separated): ")
        target = input("Enter target: ")

        try:
            selected_indices = [int(x.strip()) - 1 for x in tool_selections.split(",")]
            selected_tools = [
                self.available_tools[i]["name"]
                for i in selected_indices
                if 0 <= i < len(self.available_tools)
            ]

            if selected_tools:
                console.print(
                    f"[yellow]🔄 Orchestrating {len(selected_tools)} tools...[/yellow]"
                )

                payload = {
                    "tools": selected_tools,
                    "target": target,
                    "options": {"background": True},
                }

                response = requests.post(
                    f"{self.framework_url}/api/v1/tools/crush/orchestrate",
                    json=payload,
                    timeout=30,
                )

                if response.status_code == 200:
                    console.print(
                        "[green]✅ Orchestration started in background[/green]"
                    )
                else:
                    console.print(
                        f"[red]❌ Orchestration failed: {response.text}[/red]"
                    )
            else:
                console.print("[red]❌ No valid tools selected[/red]")

        except (ValueError, KeyboardInterrupt):
            console.print("[yellow]⚠️ Operation cancelled[/yellow]")

    async def browse_files_with_crush(self):
        """Launch Crush file manager for framework browsing"""
        console.print("[bold]📂 Launching Crush File Manager[/bold]")

        try:
            # Launch Crush in the current directory
            subprocess.run([str(self.crush_path)], cwd=".")
        except Exception as e:
            console.print(f"[red]❌ Failed to launch Crush: {e}[/red]")

    async def show_framework_status(self):
        """Display comprehensive framework status"""
        console.print("[bold]📊 Framework Status Dashboard[/bold]")

        try:
            # Get comprehensive status
            response = requests.get(
                f"{self.framework_url}/api/v1/integrations/status", timeout=10
            )

            if response.status_code == 200:
                status_data = response.json()

                # Create status table
                status_table = Table(title="🏥 Component Health Status")
                status_table.add_column("Component", style="cyan")
                status_table.add_column("Status", style="green")
                status_table.add_column("Details", style="yellow")

                for component, details in status_data.items():
                    if isinstance(details, dict):
                        status = (
                            "✅ Healthy"
                            if details.get("status") == "healthy"
                            else "❌ Unhealthy"
                        )
                        info = details.get("message", "No details")
                    else:
                        status = "✅ Active" if details else "❌ Inactive"
                        info = str(details)

                    status_table.add_row(component, status, info)

                console.print(status_table)
            else:
                console.print(f"[red]❌ Could not fetch status: {response.text}[/red]")

        except Exception as e:
            console.print(f"[red]❌ Status check failed: {e}[/red]")

    async def run_interactive_mode(self):
        """Run the orchestrator in interactive mode"""
        await self.initialize()

        while True:
            try:
                self.display_main_menu()
                choice = input("\n🎮 Select an option (0-9): ").strip()

                if choice == "1":
                    await self.launch_individual_tool()
                elif choice == "2":
                    await self.execute_multi_tool_orchestration()
                elif choice == "3":
                    console.print(
                        "[yellow]🚧 Workflow creation coming soon...[/yellow]"
                    )
                elif choice == "4":
                    console.print(
                        "[yellow]🚧 Workflow execution coming soon...[/yellow]"
                    )
                elif choice == "5":
                    await self.browse_files_with_crush()
                elif choice == "6":
                    await self.show_framework_status()
                elif choice == "7":
                    console.print(
                        "[yellow]🚧 Tool configuration coming soon...[/yellow]"
                    )
                elif choice == "8":
                    console.print("[yellow]🚧 Logs and reports coming soon...[/yellow]")
                elif choice == "9":
                    console.print("[yellow]🚧 Build management coming soon...[/yellow]")
                elif choice == "0":
                    console.print("[green]👋 Goodbye![/green]")
                    break
                else:
                    console.print("[red]❌ Invalid option[/red]")

                input("\n⏸️ Press Enter to continue...")

            except KeyboardInterrupt:
                console.print("\n[yellow]👋 Exiting...[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")
                input("⏸️ Press Enter to continue...")


async def main():
    """Main entry point"""
    orchestrator = CrushOrchestrator()
    await orchestrator.run_interactive_mode()


if __name__ == "__main__":
    # Check dependencies
    try:
        import requests
        import rich
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install rich requests")
        sys.exit(1)

    asyncio.run(main())
