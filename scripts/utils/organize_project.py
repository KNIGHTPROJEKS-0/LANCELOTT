#!/usr/bin/env python3
"""
LANCELOTT Project Organization and Validation Script
Ensures proper project structure and validates all components
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# Setup
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
logging.basicConfig(level=logging.INFO)


class LANCELOTTOrganizer:
    """Organizes and validates LANCELOTT project structure"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.issues = []
        self.fixed = []

    def organize_project_structure(self):
        """Organize the project structure"""
        print("🏗️ Organizing LANCELOTT Project Structure...")

        # Required directories
        required_dirs = [
            "api/routes",
            "build",
            "config",
            "core",
            "docs/api",
            "docs/tools",
            "integrations/ai",
            "integrations/security",
            "integrations/tools",
            "integrations/workflows",
            "logs",
            "reports",
            "status",
            "static",
            "tests/api",
            "tests/framework",
            "tests/integration",
            "tests/tools",
            "tests/unit",
            "tools",
            "uploads",
            "workflows",
        ]

        # Create directories
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                self.fixed.append(f"Created directory: {dir_path}")
                print(f"✅ Created: {dir_path}/")
            else:
                print(f"📁 Exists: {dir_path}/")

    def validate_core_files(self):
        """Validate core project files exist"""
        print("\n📄 Validating Core Files...")

        core_files = {
            "app.py": "Main FastAPI application",
            "main.py": "Alternative entry point",
            "lancelott.py": "CLI interface",
            "requirements.txt": "Python dependencies",
            "README.md": "Project documentation",
            "config/lancelott.yaml": "Main configuration",
            "config/lancelott_config.py": "Configuration manager",
            ".env.example": "Environment template",
        }

        for file_path, description in core_files.items():
            full_path = self.project_root / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                print(f"✅ {file_path} ({size} bytes) - {description}")
            else:
                self.issues.append(f"Missing: {file_path}")
                print(f"❌ Missing: {file_path} - {description}")

    def validate_test_organization(self):
        """Validate test file organization"""
        print("\n🧪 Validating Test Organization...")

        expected_tests = {
            "tests/run_all_tests.py": "Main test runner",
            "tests/framework/test_framework.py": "Framework structure tests",
            "tests/tools/test_crush_integration.py": "Crush integration tests",
            "tests/integration/test_integration.py": "Comprehensive integration tests",
            "tests/conftest.py": "Pytest configuration",
            "tests/README.md": "Test documentation",
        }

        for test_file, description in expected_tests.items():
            full_path = self.project_root / test_file
            if full_path.exists():
                print(f"✅ {test_file} - {description}")
            else:
                self.issues.append(f"Missing test: {test_file}")
                print(f"❌ Missing: {test_file} - {description}")

    def validate_integrations(self):
        """Validate integration components"""
        print("\n🔗 Validating Integrations...")

        try:
            # Test imports
            from integrations.integration_manager import IntegrationManager
            from integrations.tools.cliwrap_wrapper import get_cliwrap_wrapper
            from integrations.tools.crush_wrapper import get_crush_wrapper

            print("✅ Core integration imports successful")

            # Test wrapper creation
            crush = get_crush_wrapper()
            cliwrap = get_cliwrap_wrapper()

            print(f"✅ Wrappers created: {crush.name}, {cliwrap.name}")

            # Test integration manager
            manager = IntegrationManager()
            configs = manager._load_default_configs()

            print(f"✅ Integration manager loaded {len(configs)} tool configs")

        except Exception as e:
            self.issues.append(f"Integration validation failed: {e}")
            print(f"❌ Integration validation failed: {e}")

    def validate_tools_directory(self):
        """Validate tools directory structure"""
        print("\n🛠️ Validating Tools Directory...")

        tools_dir = self.project_root / "tools"
        if not tools_dir.exists():
            self.issues.append("Tools directory missing")
            print("❌ Tools directory missing")
            return

        # Count tools
        tool_dirs = [d for d in tools_dir.iterdir() if d.is_dir()]
        print(f"📊 Found {len(tool_dirs)} security tools:")

        # Check key tools
        key_tools = ["crush", "CliWrap", "nmap", "Argus"]
        for tool in key_tools:
            tool_path = tools_dir / tool
            if tool_path.exists():
                print(f"  ✅ {tool}")
            else:
                print(f"  ❌ {tool} - Missing")
                self.issues.append(f"Missing key tool: {tool}")

        # Show other tools
        other_tools = [d.name for d in tool_dirs if d.name not in key_tools]
        if other_tools:
            print(
                f"  📦 Other tools: {', '.join(other_tools[:5])}{'...' if len(other_tools) > 5 else ''}"
            )

    def validate_configuration(self):
        """Validate configuration system"""
        print("\n⚙️ Validating Configuration...")

        try:
            from config.lancelott_config import get_config

            config = get_config()
            print(f"✅ Configuration loaded successfully")
            print(f"📊 Configured tools: {len(config.tools)}")
            print(f"🌐 API port: {config.api.port}")

            # Validate configuration
            issues = config.validate_configuration()
            if issues:
                print(f"⚠️ Configuration issues: {len(issues)}")
                for issue in issues[:3]:  # Show first 3
                    print(f"  - {issue}")
            else:
                print("✅ Configuration validation passed")

        except Exception as e:
            self.issues.append(f"Configuration validation failed: {e}")
            print(f"❌ Configuration validation failed: {e}")

    async def run_quick_integration_test(self):
        """Run a quick integration test"""
        print("\n🧪 Running Quick Integration Test...")

        try:
            from integrations.tools.cliwrap_wrapper import get_cliwrap_wrapper
            from integrations.tools.crush_wrapper import get_crush_wrapper

            # Test Crush
            crush = get_crush_wrapper()
            crush_health = await crush.health_check()
            print(f"🔨 Crush health check: {'✅' if crush_health else '⚠️'}")

            # Test CliWrap
            cliwrap = get_cliwrap_wrapper()
            cliwrap_health = await cliwrap.health_check()
            print(f"🛠️ CliWrap health check: {'✅' if cliwrap_health else '⚠️'}")

            # Test basic functionality
            if crush_health:
                result = await crush.execute_command(".", target=".", options={})
                success = result.get("success", False)
                print(f"🎯 Crush execution test: {'✅' if success else '⚠️'}")

            print("✅ Quick integration test completed")

        except Exception as e:
            self.issues.append(f"Integration test failed: {e}")
            print(f"❌ Integration test failed: {e}")

    def generate_report(self):
        """Generate organization report"""
        print("\n" + "=" * 60)
        print("📋 LANCELOTT Project Organization Report")
        print("=" * 60)

        print(f"🔧 Fixed: {len(self.fixed)} items")
        for fix in self.fixed:
            print(f"  ✅ {fix}")

        print(f"\n⚠️ Issues: {len(self.issues)} items")
        for issue in self.issues:
            print(f"  ❌ {issue}")

        if not self.issues:
            print("\n🎉 Project organization is PERFECT!")
            print("\n🚀 Ready to:")
            print("  • Run tests: python tests/run_all_tests.py")
            print("  • Start framework: python app.py")
            print("  • Use Crush orchestrator: python crush_orchestrator.py")
        else:
            print(f"\n🔧 Please address {len(self.issues)} issues above")

        # Save report
        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "fixed": self.fixed,
            "issues": self.issues,
            "status": "clean" if not self.issues else "issues_found",
        }

        report_file = self.project_root / "reports" / "organization_report.json"
        report_file.parent.mkdir(exist_ok=True)

        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Report saved: {report_file}")


async def main():
    """Main organization and validation"""
    print("🛡️ CERBERUS-FANGS LANCELOTT - Project Organization")
    print("=" * 60)

    organizer = LANCELOTTOrganizer()

    # Run all validations
    organizer.organize_project_structure()
    organizer.validate_core_files()
    organizer.validate_test_organization()
    organizer.validate_tools_directory()
    organizer.validate_configuration()
    organizer.validate_integrations()
    await organizer.run_quick_integration_test()

    # Generate report
    organizer.generate_report()


if __name__ == "__main__":
    asyncio.run(main())
