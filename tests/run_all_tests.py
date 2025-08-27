#!/usr/bin/env python3
"""
LANCELOTT Test Runner
Comprehensive test runner for all framework components
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class LANCELOTTTestRunner:
    """Comprehensive test runner for LANCELOTT framework"""

    def __init__(self):
        self.test_results: Dict[str, Dict] = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def run_sync_test(self, test_name: str, test_func) -> bool:
        """Run a synchronous test function"""
        try:
            print(f"\n🔍 Running {test_name}...")
            result = test_func()
            self.total_tests += 1

            if result is None or result is True:
                self.passed_tests += 1
                print(f"✅ {test_name}: PASSED")
                return True
            else:
                self.failed_tests += 1
                print(f"❌ {test_name}: FAILED")
                return False

        except Exception as e:
            self.failed_tests += 1
            print(f"❌ {test_name}: FAILED with error: {e}")
            return False

    async def run_async_test(self, test_name: str, test_func) -> bool:
        """Run an asynchronous test function"""
        try:
            print(f"\n🔍 Running {test_name}...")
            result = await test_func()
            self.total_tests += 1

            if result is None or result is True:
                self.passed_tests += 1
                print(f"✅ {test_name}: PASSED")
                return True
            else:
                self.failed_tests += 1
                print(f"❌ {test_name}: FAILED")
                return False

        except Exception as e:
            self.failed_tests += 1
            print(f"❌ {test_name}: FAILED with error: {e}")
            return False

    def run_framework_tests(self):
        """Run framework structure tests"""
        print("🏗️ Running Framework Tests...")

        try:
            # Import and run framework tests
            sys.path.append(str(project_root / "tests" / "framework"))
            from test_framework import (
                test_build_system,
                test_configuration,
                test_documentation,
                test_framework_structure,
                test_integration_system,
                test_python_imports,
            )

            # Run each test
            self.run_sync_test("Framework Structure", test_framework_structure)
            self.run_sync_test("Python Imports", test_python_imports)
            self.run_sync_test("Configuration System", test_configuration)
            self.run_sync_test("Build System", test_build_system)
            self.run_sync_test("Integration System", test_integration_system)
            self.run_sync_test("Documentation", test_documentation)

        except Exception as e:
            print(f"❌ Framework tests failed to load: {e}")

    async def run_tool_tests(self):
        """Run tool integration tests"""
        print("\n🛠️ Running Tool Integration Tests...")

        try:
            # Import and run tool tests
            sys.path.append(str(project_root / "tests" / "tools"))
            from test_crush_integration import (
                test_cliwrap_integration,
                test_crush_integration,
                test_framework_integration,
            )

            # Run each test
            await self.run_async_test("Crush Integration", test_crush_integration)
            await self.run_async_test("CliWrap Integration", test_cliwrap_integration)
            await self.run_async_test(
                "Framework Integration", test_framework_integration
            )

        except Exception as e:
            print(f"❌ Tool tests failed to load: {e}")

    async def run_integration_tests(self):
        """Run comprehensive integration tests"""
        print("\n🔗 Running Integration Tests...")

        try:
            # Import and run integration tests
            sys.path.append(str(project_root / "tests" / "integration"))
            from test_integration import LancelottIntegrationTest

            # Run comprehensive integration test
            integration_test = LancelottIntegrationTest()
            result = await integration_test.run_all_tests()

            self.total_tests += 1
            if result:
                self.passed_tests += 1
                print("✅ Comprehensive Integration Test: PASSED")
            else:
                self.failed_tests += 1
                print("❌ Comprehensive Integration Test: FAILED")

        except Exception as e:
            print(f"❌ Integration tests failed to load: {e}")
            self.failed_tests += 1
            self.total_tests += 1

    def run_unit_tests(self):
        """Run unit tests using pytest if available"""
        print("\n🧪 Running Unit Tests...")

        try:
            import subprocess

            import pytest

            # Run pytest on unit tests
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    str(project_root / "tests" / "unit"),
                    "-v",
                ],
                capture_output=True,
                text=True,
            )

            self.total_tests += 1
            if result.returncode == 0:
                self.passed_tests += 1
                print("✅ Unit Tests: PASSED")
            else:
                self.failed_tests += 1
                print("❌ Unit Tests: FAILED")
                print(result.stdout)
                print(result.stderr)

        except ImportError:
            print("⚠️ pytest not available, skipping unit tests")
        except Exception as e:
            print(f"❌ Unit tests failed: {e}")

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("🎯 LANCELOTT Test Results Summary")
        print("=" * 60)
        print(f"📊 Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")

        if self.total_tests > 0:
            success_rate = (self.passed_tests / self.total_tests) * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")

        if self.failed_tests == 0:
            print("\n🎉 All tests PASSED! Framework is ready!")
            print("\n🚀 Next steps:")
            print("  • Start the framework: python app.py")
            print("  • Run Crush orchestrator: python crush_orchestrator.py")
            print("  • Access API docs: http://localhost:7777/docs")
        else:
            print(f"\n💥 {self.failed_tests} tests FAILED!")
            print("🔧 Please check the issues above before proceeding.")

        return self.failed_tests == 0


async def main():
    """Main test execution"""
    print("🛡️ CERBERUS-FANGS LANCELOTT - Comprehensive Test Suite")
    print("=" * 60)

    runner = LANCELOTTTestRunner()

    # Run all test suites
    runner.run_framework_tests()
    await runner.run_tool_tests()
    await runner.run_integration_tests()
    runner.run_unit_tests()

    # Print summary and exit
    success = runner.print_summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
