#!/usr/bin/env python3
"""
CERBERUS-FANGS LANCELOTT - Comprehensive Integration Test
Tests all integrated components including AI and Vanguard tools
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from build.build_manager import BuildManager

# Framework imports
from config.lancelott_config import get_config
from integrations.ai.supercompat_manager import get_supercompat_manager
from integrations.ai.supergateway_manager import get_supergateway_manager
from integrations.integration_manager import IntegrationManager
from integrations.security.vanguard_manager import get_vanguard_manager
from status.status_monitor import StatusMonitor


class LancelottIntegrationTest:
    """Comprehensive integration test suite"""

    def __init__(self):
        self.logger = self._setup_logging()
        self.test_results: Dict[str, Any] = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "test_details": [],
        }

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for integration tests"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        return logging.getLogger(__name__)

    async def run_all_tests(self) -> bool:
        """Run all integration tests"""
        self.logger.info("🧪 Starting LANCELOTT Integration Tests")
        self.logger.info("=" * 60)

        test_suites = [
            ("Configuration System", self._test_configuration),
            ("Build System", self._test_build_system),
            ("Security Tools Integration", self._test_security_tools),
            ("AI Integrations", self._test_ai_integrations),
            ("Vanguard Security Tools", self._test_vanguard_tools),
            ("Status Monitoring", self._test_status_monitoring),
            ("API Structure", self._test_api_structure),
            ("Documentation Completeness", self._test_documentation),
        ]

        for suite_name, test_func in test_suites:
            self.logger.info(f"\n📋 Testing: {suite_name}")
            try:
                result = await test_func()
                self._record_test_result(suite_name, result)
            except Exception as e:
                self.logger.error(f"❌ {suite_name} failed with exception: {e}")
                self._record_test_result(suite_name, False, str(e))

        self._generate_test_report()
        return self.test_results["failed"] == 0

    def _record_test_result(self, test_name: str, passed: bool, error: str = None):
        """Record test result"""
        self.test_results["total_tests"] += 1

        if passed:
            self.test_results["passed"] += 1
            self.logger.info(f"✅ {test_name}: PASSED")
        else:
            self.test_results["failed"] += 1
            self.logger.error(f"❌ {test_name}: FAILED")
            if error:
                self.logger.error(f"   Error: {error}")

        self.test_results["test_details"].append(
            {
                "test": test_name,
                "status": "PASSED" if passed else "FAILED",
                "error": error,
            }
        )

    async def _test_configuration(self) -> bool:
        """Test configuration system"""
        try:
            config = get_config()

            # Test configuration loading
            if not config.tools:
                return False

            # Test configuration validation
            issues = config.validate_configuration()
            if issues:
                self.logger.warning(f"Configuration issues: {len(issues)}")
                self.test_results["warnings"] += 1

            # Test configuration summary
            summary = config.get_configuration_summary()
            if not summary or "tools" not in summary:
                return False

            return True

        except Exception as e:
            self.logger.error(f"Configuration test failed: {e}")
            return False

    async def _test_build_system(self) -> bool:
        """Test build system"""
        try:
            build_manager = BuildManager()

            # Test build target definition
            targets = build_manager.build_targets
            if not targets:
                return False

            # Check for key targets
            required_targets = ["supergateway", "supercompat"]
            for target in required_targets:
                if target not in targets:
                    self.logger.error(f"Missing build target: {target}")
                    return False

            # Check Vanguard targets
            vanguard_targets = [t for t in targets.keys() if "vanguard" in t]
            if len(vanguard_targets) < 3:
                self.logger.warning("Limited Vanguard build targets")
                self.test_results["warnings"] += 1

            return True

        except Exception as e:
            self.logger.error(f"Build system test failed: {e}")
            return False

    async def _test_security_tools(self) -> bool:
        """Test security tools integration"""
        try:
            integration_manager = IntegrationManager()

            # Test tool configurations
            configs = integration_manager._load_default_configs()
            if len(configs) < 10:  # Should have at least 10 security tools
                return False

            # Test path updates
            for name, config in configs.items():
                if not config.executable_path.startswith("tools/") and name != "nmap":
                    self.logger.error(
                        f"Tool {name} path not updated: {config.executable_path}"
                    )
                    return False

            return True

        except Exception as e:
            self.logger.error(f"Security tools test failed: {e}")
            return False

    async def _test_ai_integrations(self) -> bool:
        """Test AI integration components"""
        try:
            # Test SuperGateway manager
            gateway_manager = get_supergateway_manager()
            gateway_status = gateway_manager.get_status()

            if not gateway_status or "gateway_path" not in gateway_status:
                return False

            # Test SuperCompat manager
            compat_manager = get_supercompat_manager()
            compat_status = compat_manager.get_status()

            if not compat_status or "compat_path" not in compat_status:
                return False

            # Verify paths are updated
            expected_gateway_path = "integrations/ai/supergateway"
            expected_compat_path = "integrations/ai/supercompat"

            if expected_gateway_path not in str(gateway_status["gateway_path"]):
                self.logger.error(
                    f"SuperGateway path not updated: {gateway_status['gateway_path']}"
                )
                return False

            if expected_compat_path not in str(compat_status["compat_path"]):
                self.logger.error(
                    f"SuperCompat path not updated: {compat_status['compat_path']}"
                )
                return False

            return True

        except Exception as e:
            self.logger.error(f"AI integrations test failed: {e}")
            return False

    async def _test_vanguard_tools(self) -> bool:
        """Test Vanguard obfuscation tools"""
        try:
            vanguard_manager = get_vanguard_manager()

            # Test tool listing
            tools = await vanguard_manager.list_available_tools()
            if len(tools) < 5:  # Should have at least 5 Vanguard tools
                return False

            # Test tool configuration
            status = vanguard_manager.get_status()
            if not status or "total_tools" not in status:
                return False

            # Verify tool types
            expected_types = [
                "python",
                "javascript",
                "java",
                "binary",
                "network",
                "shellcode",
            ]
            found_types = set()

            for tool in tools:
                tool_type = tool.get("type")
                if tool_type:
                    found_types.add(tool_type)

            if len(found_types) < 3:  # Should support at least 3 different types
                self.logger.warning("Limited Vanguard tool type coverage")
                self.test_results["warnings"] += 1

            return True

        except Exception as e:
            self.logger.error(f"Vanguard tools test failed: {e}")
            return False

    async def _test_status_monitoring(self) -> bool:
        """Test status monitoring system"""
        try:
            status_monitor = StatusMonitor()

            # Test status checking
            await status_monitor.check_all_components()

            # Test report generation
            report = status_monitor.generate_status_report("json")
            if not report:
                return False

            return True

        except Exception as e:
            self.logger.error(f"Status monitoring test failed: {e}")
            return False

    async def _test_api_structure(self) -> bool:
        """Test API structure and routing"""
        try:
            # Test router imports
            from api.routes.supercompat_router import router as supercompat_router
            from api.routes.supergateway_router import router as supergateway_router
            from api.routes.vanguard_router import router as vanguard_router

            # Test that routers have endpoints
            if (
                not hasattr(supergateway_router, "routes")
                or len(supergateway_router.routes) == 0
            ):
                return False

            if (
                not hasattr(supercompat_router, "routes")
                or len(supercompat_router.routes) == 0
            ):
                return False

            if (
                not hasattr(vanguard_router, "routes")
                or len(vanguard_router.routes) == 0
            ):
                return False

            return True

        except Exception as e:
            self.logger.error(f"API structure test failed: {e}")
            return False

    async def _test_documentation(self) -> bool:
        """Test documentation completeness"""
        try:
            project_root = Path(__file__).parent

            # Check key documentation files
            required_docs = [
                "README.md",
                "docs/api/API_REFERENCE.md",
                "docs/tools/TOOLS_REFERENCE.md",
                "docs/CONFIGURATION_GUIDE.md",
                "FRAMEWORK_VALIDATION_REPORT.md",
            ]

            missing_docs = []
            for doc in required_docs:
                doc_path = project_root / doc
                if not doc_path.exists():
                    missing_docs.append(doc)

            if missing_docs:
                self.logger.error(f"Missing documentation files: {missing_docs}")
                return False

            # Check README content for new components
            readme_path = project_root / "README.md"
            readme_content = readme_path.read_text()

            required_sections = [
                "SuperGateway",
                "SuperCompat",
                "Vanguard",
                "AI Integration",
            ]
            missing_sections = []

            for section in required_sections:
                if section not in readme_content:
                    missing_sections.append(section)

            if missing_sections:
                self.logger.warning(f"Missing README sections: {missing_sections}")
                self.test_results["warnings"] += 1

            return True

        except Exception as e:
            self.logger.error(f"Documentation test failed: {e}")
            return False

    def _generate_test_report(self):
        """Generate comprehensive test report"""
        self.logger.info("\n" + "=" * 60)
        self.logger.info("🎯 LANCELOTT Integration Test Results")
        self.logger.info("=" * 60)

        total = self.test_results["total_tests"]
        passed = self.test_results["passed"]
        failed = self.test_results["failed"]
        warnings = self.test_results["warnings"]

        self.logger.info(f"📊 Total Tests: {total}")
        self.logger.info(f"✅ Passed: {passed}")
        self.logger.info(f"❌ Failed: {failed}")
        self.logger.info(f"⚠️ Warnings: {warnings}")

        success_rate = (passed / total * 100) if total > 0 else 0
        self.logger.info(f"📈 Success Rate: {success_rate:.1f}%")

        if failed == 0:
            self.logger.info("🎉 All integration tests PASSED!")
        else:
            self.logger.error("💥 Some integration tests FAILED!")

        # Save detailed report
        try:
            project_root = Path(__file__).parent
            report_file = project_root / "reports" / "integration_test_report.json"
            report_file.parent.mkdir(exist_ok=True)

            with open(report_file, "w") as f:
                json.dump(self.test_results, f, indent=2)

            self.logger.info(f"📋 Detailed report saved: {report_file}")

        except Exception as e:
            self.logger.warning(f"Failed to save test report: {e}")


async def main():
    """Main test execution"""
    test_runner = LancelottIntegrationTest()
    success = await test_runner.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
