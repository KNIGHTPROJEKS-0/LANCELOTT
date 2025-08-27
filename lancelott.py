#!/usr/bin/env python3
"""
LANCELOTT - Unified CLI Management
Command-line interface for managing the LANCELOTT framework
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def setup_logging():
    """Setup basic logging for CLI"""
    import logging

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="LANCELOTT - Unified Security Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s start                    # Start the API server
  %(prog)s build                    # Build all tools
  %(prog)s build --target argus     # Build specific tool
  %(prog)s status                   # Check system status
  %(prog)s config summary           # Show configuration summary
  %(prog)s monitor                  # Start monitoring
  %(prog)s workflows setup          # Setup n8n workflows
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start the LANCELOTT API server")
    start_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    start_parser.add_argument("--port", type=int, default=7777, help="Port to bind to")
    start_parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload"
    )
    start_parser.add_argument(
        "--workers", type=int, default=1, help="Number of workers"
    )

    # Build command
    build_parser = subparsers.add_parser("build", help="Build tools and components")
    build_parser.add_argument("--target", help="Specific tool to build")
    build_parser.add_argument(
        "--clean", action="store_true", help="Clean before building"
    )
    build_parser.add_argument(
        "--skip-optional", action="store_true", help="Skip optional tools"
    )

    # Status command
    status_parser = subparsers.add_parser("status", help="Check system status")
    status_parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format"
    )
    status_parser.add_argument("--save", help="Save report to file")

    # Config command
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_subparsers = config_parser.add_subparsers(
        dest="config_action", help="Config actions"
    )
    config_subparsers.add_parser("summary", help="Show configuration summary")
    config_subparsers.add_parser("validate", help="Validate configuration")
    config_subparsers.add_parser("save", help="Save current configuration")
    env_parser = config_subparsers.add_parser("env", help="Generate environment file")
    env_parser.add_argument("--output", help="Output file path")

    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Start system monitoring")
    monitor_parser.add_argument(
        "--duration", type=int, help="Monitor duration in seconds"
    )
    monitor_parser.add_argument(
        "--interval", type=int, default=30, help="Check interval in seconds"
    )

    # Workflows command
    workflows_parser = subparsers.add_parser(
        "workflows", help="n8n workflow management"
    )
    workflows_subparsers = workflows_parser.add_subparsers(
        dest="workflows_action", help="Workflow actions"
    )
    workflows_subparsers.add_parser("setup", help="Setup n8n workflows")
    workflows_subparsers.add_parser("health", help="Check n8n health")
    start_n8n = workflows_subparsers.add_parser("start", help="Start n8n instance")
    start_n8n.add_argument("--tunnel", action="store_true", help="Start with tunnel")

    # Integrations command
    integrations_parser = subparsers.add_parser(
        "integrations", help="Tool integration management"
    )
    integrations_subparsers = integrations_parser.add_subparsers(
        dest="integrations_action", help="Integration actions"
    )
    integrations_subparsers.add_parser("init", help="Initialize all integrations")
    integrations_subparsers.add_parser("status", help="Show integration status")
    integrations_subparsers.add_parser("health", help="Check integration health")
    test_parser = integrations_subparsers.add_parser(
        "test", help="Test specific integration"
    )
    test_parser.add_argument("tool", help="Tool name to test")

    # Tools command
    tools_parser = subparsers.add_parser("tools", help="Tool management")
    tools_subparsers = tools_parser.add_subparsers(
        dest="tools_action", help="Tool actions"
    )
    tools_subparsers.add_parser("list", help="List all tools")
    enable_parser = tools_subparsers.add_parser("enable", help="Enable a tool")
    enable_parser.add_argument("tool", help="Tool name to enable")
    disable_parser = tools_subparsers.add_parser("disable", help="Disable a tool")
    disable_parser.add_argument("tool", help="Tool name to disable")

    # Version command
    version_parser = subparsers.add_parser("version", help="Show version information")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    logger = setup_logging()

    try:
        if args.command == "start":
            handle_start_command(args, logger)
        elif args.command == "build":
            handle_build_command(args, logger)
        elif args.command == "status":
            asyncio.run(handle_status_command(args, logger))
        elif args.command == "config":
            handle_config_command(args, logger)
        elif args.command == "monitor":
            asyncio.run(handle_monitor_command(args, logger))
        elif args.command == "workflows":
            asyncio.run(handle_workflows_command(args, logger))
        elif args.command == "integrations":
            asyncio.run(handle_integrations_command(args, logger))
        elif args.command == "tools":
            handle_tools_command(args, logger)
        elif args.command == "version":
            handle_version_command(args, logger)

    except KeyboardInterrupt:
        logger.info("Operation interrupted by user")
    except Exception as e:
        logger.error(f"Command failed: {e}")
        sys.exit(1)


def handle_start_command(args, logger):
    """Handle start command"""
    logger.info("🚀 Starting LANCELOTT API server...")

    try:
        import uvicorn

        from app import app

        uvicorn.run(
            "app:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers,
            log_level="info",
        )

    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        logger.error(
            "Please ensure all dependencies are installed: pip install -r requirements.txt"
        )
        sys.exit(1)


def handle_build_command(args, logger):
    """Handle build command"""
    logger.info("🔨 Building LANCELOTT components...")

    try:
        from build.build_manager import BuildManager

        manager = BuildManager()

        if args.clean:
            logger.info("🧹 Cleaning build artifacts...")
            manager.clean_all()

        if args.target:
            success = manager.build_target(args.target)
            if success:
                logger.info(f"✅ Successfully built {args.target}")
            else:
                logger.error(f"❌ Failed to build {args.target}")
                sys.exit(1)
        else:
            success = manager.build_all(args.skip_optional)
            if success:
                logger.info("✅ All builds completed successfully")
            else:
                logger.error("❌ Some builds failed")
                sys.exit(1)

    except ImportError as e:
        logger.error(f"Failed to import build manager: {e}")
        sys.exit(1)


async def handle_status_command(args, logger):
    """Handle status command"""
    logger.info("📊 Checking system status...")

    try:
        from status.status_monitor import StatusMonitor

        monitor = StatusMonitor()
        await monitor.check_all_components()

        if args.save:
            report_path = monitor.save_report(args.save, args.format)
            logger.info(f"📄 Status report saved to: {report_path}")
        else:
            report = monitor.generate_status_report(args.format)
            print(report)

    except ImportError as e:
        logger.error(f"Failed to import status monitor: {e}")
        sys.exit(1)


def handle_config_command(args, logger):
    """Handle config command"""
    try:
        from config.lancelott_config import LancelottConfig

        config = LancelottConfig()

        if args.config_action == "summary":
            summary = config.get_configuration_summary()
            print("📋 Configuration Summary:")
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

        elif args.config_action == "validate":
            issues = config.validate_configuration()
            if issues:
                print("⚠️  Configuration validation issues:")
                for issue in issues:
                    print(f"  - {issue}")
                sys.exit(1)
            else:
                print("✅ Configuration validation passed")

        elif args.config_action == "save":
            config.save_configuration()
            print("💾 Configuration saved successfully")

        elif args.config_action == "env":
            output_path = config.generate_environment_file(args.output)
            print(f"📄 Environment file generated: {output_path}")

    except ImportError as e:
        logger.error(f"Failed to import configuration manager: {e}")
        sys.exit(1)


async def handle_monitor_command(args, logger):
    """Handle monitor command"""
    logger.info("📈 Starting system monitoring...")

    try:
        from status.status_monitor import StatusMonitor

        monitor = StatusMonitor()
        await monitor.continuous_monitoring(args.duration)

    except ImportError as e:
        logger.error(f"Failed to import status monitor: {e}")
        sys.exit(1)


async def handle_workflows_command(args, logger):
    """Handle workflows command"""
    try:
        from integrations.n8n_integration import N8nIntegration

        integration = N8nIntegration()

        if args.workflows_action == "setup":
            logger.info("🔄 Setting up n8n workflows...")
            results = await integration.setup_complete_integration()
            if results.get("workflows_created"):
                logger.info("✅ n8n workflows setup completed")
            else:
                logger.error("❌ n8n workflows setup failed")

        elif args.workflows_action == "health":
            healthy = await integration.check_n8n_health()
            if healthy:
                logger.info("✅ n8n is healthy")
            else:
                logger.error("❌ n8n is not responding")

        elif args.workflows_action == "start":
            logger.info("🚀 Starting n8n instance...")
            process = integration.start_n8n(args.tunnel)
            logger.info(f"n8n started with PID: {process.pid}")
            logger.info(f"Access n8n at: {integration.n8n_url}")

    except ImportError as e:
        logger.error(f"Failed to import n8n integration: {e}")
        sys.exit(1)


async def handle_integrations_command(args, logger):
    """Handle integrations command"""
    try:
        from integrations.integration_manager import IntegrationManager

        manager = IntegrationManager()

        if args.integrations_action == "init":
            logger.info("🔧 Initializing tool integrations...")
            results = await manager.initialize_all()
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            logger.info(
                f"✅ Integration initialization: {successful}/{total} successful"
            )

        elif args.integrations_action == "status":
            status = manager.get_tool_status()
            print("🔧 Integration Status:")
            print("=" * 80)
            for tool, info in status.items():
                enabled = "✅" if info["enabled"] else "❌"
                executable = "✅" if info["executable_exists"] else "❌"
                initialized = "✅" if info["initialized"] else "❌"
                print(
                    f"{tool:15} | Enabled: {enabled} | Executable: {executable} | Initialized: {initialized}"
                )

        elif args.integrations_action == "health":
            results = await manager.health_check_all()
            print("💓 Integration Health:")
            for tool, healthy in results.items():
                status = "✅ Healthy" if healthy else "❌ Unhealthy"
                print(f"  {tool}: {status}")

        elif args.integrations_action == "test":
            result = await manager.execute_tool_command(args.tool, "--help")
            print(f"🧪 Test result for {args.tool}:")
            if result.get("success"):
                logger.info("✅ Tool test successful")
            else:
                logger.error(f"❌ Tool test failed: {result.get('error')}")

    except ImportError as e:
        logger.error(f"Failed to import integration manager: {e}")
        sys.exit(1)


def handle_tools_command(args, logger):
    """Handle tools command"""
    try:
        from config.lancelott_config import get_config

        config = get_config()

        if args.tools_action == "list":
            print("🛠️  Available Tools:")
            print("=" * 60)
            for name, tool in config.tools.items():
                status = "✅ Enabled" if tool.enabled else "❌ Disabled"
                optional = " (Optional)" if tool.optional else ""
                print(f"{tool.name:20} | {status}{optional} | Port: {tool.port}")

        elif args.tools_action == "enable":
            if config.update_tool_config(args.tool, enabled=True):
                config.save_configuration()
                logger.info(f"✅ Tool {args.tool} enabled")
            else:
                logger.error(f"❌ Tool {args.tool} not found")

        elif args.tools_action == "disable":
            if config.update_tool_config(args.tool, enabled=False):
                config.save_configuration()
                logger.info(f"❌ Tool {args.tool} disabled")
            else:
                logger.error(f"❌ Tool {args.tool} not found")

    except ImportError as e:
        logger.error(f"Failed to import configuration: {e}")
        sys.exit(1)


def handle_version_command(args, logger):
    """Handle version command"""
    print("🛡️  LANCELOTT")
    print("=" * 40)
    print("Version: 2.1.0")
    print("Framework: Enhanced Security Suite")
    print("Components:")
    print("  • Unified Build System")
    print("  • Integration Manager")
    print("  • Status Monitor")
    print("  • n8n Workflow Automation")
    print("  • Advanced API Routes")
    print("  • Unified Configuration")
    print("  • 17+ Security Tools")


if __name__ == "__main__":
    main()
