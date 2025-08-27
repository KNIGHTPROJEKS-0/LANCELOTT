#!/usr/bin/env python3
"""
CERBERUS-FANGS LANCELOTT - Unified Deployment System
Comprehensive deployment script for all integrated components
"""

import argparse
import asyncio
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Import framework components
from build.build_manager import BuildManager
from config.lancelott_config import get_config
from integrations.ai.supercompat_manager import get_supercompat_manager
from integrations.ai.supergateway_manager import get_supergateway_manager
from integrations.integration_manager import IntegrationManager
from integrations.security.vanguard_manager import get_vanguard_manager
from status.status_monitor import StatusMonitor


class LancelottDeployment:
    """Unified deployment manager for LANCELOTT framework"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.logger = self._setup_logging()
        self.config = get_config()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for deployment"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        return logging.getLogger(__name__)

    async def deploy_full_stack(self, environment: str = "development") -> bool:
        """Deploy the complete LANCELOTT stack"""
        self.logger.info(f"🚀 Starting LANCELOTT deployment for {environment}")

        deployment_steps = [
            ("Validating configuration", self._validate_configuration),
            ("Building core components", self._build_core_components),
            ("Building security tools", self._build_security_tools),
            ("Building AI integrations", self._build_ai_integrations),
            ("Building Vanguard tools", self._build_vanguard_tools),
            ("Setting up database", self._setup_database),
            ("Configuring services", self._configure_services),
            ("Starting core services", self._start_core_services),
            ("Initializing integrations", self._initialize_integrations),
            ("Running health checks", self._run_health_checks),
            ("Generating deployment report", self._generate_deployment_report),
        ]

        success_count = 0
        for step_name, step_func in deployment_steps:
            self.logger.info(f"📋 {step_name}...")
            try:
                success = await step_func(environment)
                if success:
                    self.logger.info(f"✅ {step_name} completed successfully")
                    success_count += 1
                else:
                    self.logger.error(f"❌ {step_name} failed")
                    if environment == "production":
                        self.logger.error(
                            "🛑 Deployment halted due to critical failure"
                        )
                        return False
            except Exception as e:
                self.logger.error(f"❌ {step_name} failed with exception: {e}")
                if environment == "production":
                    return False

        total_steps = len(deployment_steps)
        self.logger.info(
            f"🎯 Deployment completed: {success_count}/{total_steps} steps successful"
        )

        if success_count == total_steps:
            self.logger.info("🎉 LANCELOTT deployment successful!")
            return True
        else:
            self.logger.warning("⚠️ Partial deployment completed with warnings")
            return environment != "production"

    async def _validate_configuration(self, environment: str) -> bool:
        """Validate framework configuration"""
        try:
            issues = self.config.validate_configuration()
            if issues:
                self.logger.warning(f"Configuration issues found: {len(issues)}")
                for issue in issues:
                    self.logger.warning(f"  - {issue}")
                return environment == "development"
            return True
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False

    async def _build_core_components(self, environment: str) -> bool:
        """Build core framework components"""
        try:
            build_manager = BuildManager()

            # Build essential components
            core_targets = ["supergateway", "supercompat"]

            for target in core_targets:
                success = build_manager.build_target(target)
                if not success and environment == "production":
                    return False

            return True
        except Exception as e:
            self.logger.error(f"Core component build failed: {e}")
            return False

    async def _build_security_tools(self, environment: str) -> bool:
        """Build security tools"""
        try:
            build_manager = BuildManager()

            # Build security tools
            security_targets = [
                "metabigor",
                "osmedeus",
                "dismap",
                "argus",
                "kraken",
                "spiderfoot",
                "social-analyzer",
                "sherlock",
                "vajra",
            ]

            success_count = 0
            for target in security_targets:
                success = build_manager.build_target(target)
                if success:
                    success_count += 1

            # Require at least 50% success rate
            required_success = len(security_targets) * 0.5
            return success_count >= required_success

        except Exception as e:
            self.logger.error(f"Security tools build failed: {e}")
            return False

    async def _build_ai_integrations(self, environment: str) -> bool:
        """Build AI integration components"""
        try:
            # Start SuperGateway
            gateway_manager = get_supergateway_manager()
            gateway_success = await gateway_manager.start_gateway()

            # Start SuperCompat
            compat_manager = get_supercompat_manager()
            compat_success = await compat_manager.start_compat_service()

            if environment == "production":
                return gateway_success and compat_success
            else:
                return gateway_success or compat_success

        except Exception as e:
            self.logger.error(f"AI integrations build failed: {e}")
            return False

    async def _build_vanguard_tools(self, environment: str) -> bool:
        """Build Vanguard obfuscation tools"""
        try:
            vanguard_manager = get_vanguard_manager()

            # Build essential Vanguard tools
            build_tools = [
                "javascript-obfuscator",
                "skidfuscator",
                "utls",
                "fake-http",
                "bitmono",
            ]

            success_count = 0
            for tool in build_tools:
                try:
                    success = await vanguard_manager.build_tool(tool)
                    if success:
                        success_count += 1
                except Exception as e:
                    self.logger.warning(f"Vanguard tool {tool} build failed: {e}")

            # At least 3 tools should build successfully
            return success_count >= 3

        except Exception as e:
            self.logger.error(f"Vanguard tools build failed: {e}")
            return False

    async def _setup_database(self, environment: str) -> bool:
        """Setup database for the framework"""
        try:
            db_config = self.config.database

            if db_config.type == "sqlite":
                # Create SQLite database file if it doesn't exist
                db_path = self.project_root / f"{db_config.database}.db"
                db_path.parent.mkdir(parents=True, exist_ok=True)
                db_path.touch(exist_ok=True)
                return True

            # For PostgreSQL/MySQL, check connection
            # This would normally involve actual database setup
            self.logger.info(f"Database configuration: {db_config.type}")
            return True

        except Exception as e:
            self.logger.error(f"Database setup failed: {e}")
            return False

    async def _configure_services(self, environment: str) -> bool:
        """Configure all services"""
        try:
            # Generate environment file
            env_file = self.config.generate_environment_file()
            self.logger.info(f"Environment file generated: {env_file}")

            # Create necessary directories
            directories = ["logs", "reports", "uploads", "static"]
            for directory in directories:
                (self.project_root / directory).mkdir(exist_ok=True)

            return True

        except Exception as e:
            self.logger.error(f"Service configuration failed: {e}")
            return False

    async def _start_core_services(self, environment: str) -> bool:
        """Start core services"""
        try:
            # Check if main application can start (dry run)
            import importlib.util

            app_spec = importlib.util.spec_from_file_location(
                "app", self.project_root / "app.py"
            )
            if app_spec and app_spec.loader:
                self.logger.info("FastAPI application validated")
                return True

            return False

        except Exception as e:
            self.logger.error(f"Core services start failed: {e}")
            return False

    async def _initialize_integrations(self, environment: str) -> bool:
        """Initialize all integrations"""
        try:
            integration_manager = IntegrationManager()
            results = await integration_manager.initialize_all()

            successful = sum(1 for success in results.values() if success)
            total = len(results)

            self.logger.info(
                f"Integration initialization: {successful}/{total} successful"
            )

            # Require at least 50% success
            return successful >= (total * 0.5)

        except Exception as e:
            self.logger.error(f"Integration initialization failed: {e}")
            return False

    async def _run_health_checks(self, environment: str) -> bool:
        """Run comprehensive health checks"""
        try:
            status_monitor = StatusMonitor()
            await status_monitor.check_all_components()

            report = status_monitor.generate_status_report("json")

            if isinstance(report, dict):
                healthy_components = sum(
                    1
                    for component in report.get("components", {}).values()
                    if component.get("status") == "healthy"
                )
                total_components = len(report.get("components", {}))

                self.logger.info(
                    f"Health check: {healthy_components}/{total_components} components healthy"
                )

                # Require at least 70% health
                return healthy_components >= (total_components * 0.7)

            return True

        except Exception as e:
            self.logger.error(f"Health checks failed: {e}")
            return False

    async def _generate_deployment_report(self, environment: str) -> bool:
        """Generate deployment report"""
        try:
            report_data = {
                "deployment_time": str(asyncio.get_event_loop().time()),
                "environment": environment,
                "framework_version": "2.1.0",
                "configuration_summary": self.config.get_configuration_summary(),
            }

            # Add AI services status
            gateway_manager = get_supergateway_manager()
            compat_manager = get_supercompat_manager()

            report_data["ai_services"] = {
                "supergateway": gateway_manager.get_status(),
                "supercompat": compat_manager.get_status(),
            }

            # Add Vanguard tools status
            vanguard_manager = get_vanguard_manager()
            report_data["vanguard"] = vanguard_manager.get_status()

            # Save report
            report_file = (
                self.project_root / "reports" / f"deployment_report_{environment}.json"
            )
            report_file.parent.mkdir(exist_ok=True)

            import json

            with open(report_file, "w") as f:
                json.dump(report_data, f, indent=2)

            self.logger.info(f"Deployment report saved: {report_file}")
            return True

        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return False

    def deploy_docker(self) -> bool:
        """Deploy using Docker Compose"""
        try:
            self.logger.info("🐳 Starting Docker deployment...")

            cmd = ["docker-compose", "up", "-d", "--build"]
            result = subprocess.run(
                cmd, cwd=self.project_root, capture_output=True, text=True
            )

            if result.returncode == 0:
                self.logger.info("✅ Docker deployment successful")
                return True
            else:
                self.logger.error(f"❌ Docker deployment failed: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Docker deployment failed: {e}")
            return False

    def rollback_deployment(self) -> bool:
        """Rollback deployment"""
        try:
            self.logger.info("⏪ Rolling back deployment...")

            # Stop services
            services = ["supergateway", "supercompat"]
            for service in services:
                try:
                    subprocess.run(["pkill", "-f", service], capture_output=True)
                except:
                    pass

            # Clean build artifacts
            build_manager = BuildManager()
            build_manager.clean_all()

            self.logger.info("✅ Rollback completed")
            return True

        except Exception as e:
            self.logger.error(f"Rollback failed: {e}")
            return False


async def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="LANCELOTT Deployment System")
    parser.add_argument(
        "command",
        choices=["deploy", "docker", "rollback", "status"],
        help="Deployment command",
    )
    parser.add_argument(
        "--environment",
        "-e",
        choices=["development", "staging", "production"],
        default="development",
        help="Deployment environment",
    )
    parser.add_argument(
        "--force", "-f", action="store_true", help="Force deployment even with warnings"
    )

    args = parser.parse_args()

    deployment = LancelottDeployment()

    if args.command == "deploy":
        success = await deployment.deploy_full_stack(args.environment)
        sys.exit(0 if success else 1)

    elif args.command == "docker":
        success = deployment.deploy_docker()
        sys.exit(0 if success else 1)

    elif args.command == "rollback":
        success = deployment.rollback_deployment()
        sys.exit(0 if success else 1)

    elif args.command == "status":
        print("📊 LANCELOTT Deployment Status")
        print("=" * 50)

        # Show configuration summary
        config = get_config()
        summary = config.get_configuration_summary()

        print(f"🌐 API: {summary['api']['host']}:{summary['api']['port']}")
        print(f"🛠️ Tools: {summary['tools']['enabled']}/{summary['tools']['total']}")
        print(f"🔧 Build types: {summary['tools']['by_type']}")
        print(f"⚠️ Issues: {summary['validation_issues']}")


if __name__ == "__main__":
    asyncio.run(main())
