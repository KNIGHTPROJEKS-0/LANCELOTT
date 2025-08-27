#!/usr/bin/env python3
"""
CERBERUS-FANGS Tool Integration Test Suite
Tests all integrations including N8N workflows
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Test configurations
TEST_TARGET = "httpbin.org"  # Safe test target
LOCALHOST_API = "http://localhost:8000"
N8N_URL = "http://localhost:5678"


class IntegrationTester:
    """Test suite for CERBERUS-FANGS integrations"""

    def __init__(self):
        self.test_results = []
        self.project_root = Path(__file__).parent

    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")

        self.test_results.append(
            {"test": test_name, "success": success, "details": details}
        )

    def test_metabigor_integration(self):
        """Test Metabigor integration"""
        print("\n🔍 Testing Metabigor Integration...")

        try:
            from metabigor_integration import MetabigorWrapper

            # Initialize wrapper
            metabigor = MetabigorWrapper()
            self.log_test(
                "Metabigor wrapper initialization",
                True,
                f"Path: {metabigor.metabigor_path}",
            )

            # Check if binary exists
            if metabigor.metabigor_path.exists():
                self.log_test("Metabigor binary exists", True)

                # Test IP intelligence (safe test)
                print("    Testing IP intelligence with Google DNS (8.8.8.8)...")
                result = metabigor.ip_intelligence("8.8.8.8")

                if result["success"]:
                    self.log_test("IP intelligence test", True)
                else:
                    self.log_test(
                        "IP intelligence test",
                        False,
                        result.get("stderr", "Unknown error"),
                    )
            else:
                self.log_test(
                    "Metabigor binary exists", False, "Run ./build_metabigor.sh"
                )

        except ImportError as e:
            self.log_test("Metabigor import", False, str(e))
        except Exception as e:
            self.log_test("Metabigor integration", False, str(e))

    def test_metasploit_integration(self):
        """Test Metasploit integration"""
        print("\n🛡️ Testing Metasploit Integration...")

        try:
            from metasploit_integration import MetasploitWrapper

            # Initialize wrapper
            metasploit = MetasploitWrapper()
            self.log_test(
                "Metasploit wrapper initialization",
                True,
                f"Path: {metasploit.msf_path}",
            )

            # Check if Metasploit directory exists
            if metasploit.msf_path.exists():
                self.log_test("Metasploit directory exists", True)

                # Check for msfconsole
                if metasploit.msfconsole_path.exists():
                    self.log_test("msfconsole binary exists", True)
                else:
                    self.log_test("msfconsole binary exists", False)

                # Test database status
                db_result = metasploit.check_database_status()
                if db_result["success"]:
                    self.log_test("Database status check", True)
                else:
                    self.log_test(
                        "Database status check",
                        False,
                        "Database may need initialization",
                    )
            else:
                self.log_test("Metasploit directory exists", False)

        except ImportError as e:
            self.log_test("Metasploit import", False, str(e))
        except Exception as e:
            self.log_test("Metasploit integration", False, str(e))


def test_cerberus_manager():
    """Test CERBERUS-FANGS Manager"""
    print("\n[*] Testing CERBERUS-FANGS Manager...")

    try:
        from cerberus_manager import CerbeusFangsManager, TargetInfo

        # Initialize manager
        manager = CerbeusFangsManager("test_workspace")
        print("[+] Manager initialized successfully")

        # Test target info creation
        target_info = TargetInfo(ip="127.0.0.1", domain="localhost")
        print(f"[+] Target info created: {target_info}")

        # Test IP detection
        is_ip = manager._is_ip("8.8.8.8")
        is_domain = manager._is_ip("google.com")
        print(f"[+] IP detection test: 8.8.8.8 -> {is_ip}, google.com -> {is_domain}")

        print("[+] Manager tests successful")

    except ImportError as e:
        print(f"[-] Import error: {e}")
    except Exception as e:
        print(f"[-] Error testing Manager: {e}")


def test_dependencies():
    """Test required dependencies"""
    print("\n[*] Testing Dependencies...")

    required_modules = [
        "pathlib",
        "subprocess",
        "json",
        "typing",
        "dataclasses",
        "datetime",
    ]

    optional_modules = ["pexpect", "pandas", "requests"]

    for module in required_modules:
        try:
            __import__(module)
            print(f"[+] {module} - OK")
        except ImportError:
            print(f"[-] {module} - MISSING")

    for module in optional_modules:
        try:
            __import__(module)
            print(f"[+] {module} - OK (optional)")
        except ImportError:
            print(f"[!] {module} - MISSING (optional)")

    def test_cerberus_manager(self):
        """Test CERBERUS core manager functionality"""
        print("\n⚡ Testing CERBERUS Manager...")

        try:
            from core.supercompat_manager import SuperCompatManager
            from core.supergateway_manager import SuperGatewayManager

            # Test SuperCompat Manager
            compat_manager = SuperCompatManager()
            self.log_test("SuperCompat Manager import", True)

            # Test SuperGateway Manager
            gateway_manager = SuperGatewayManager()
            self.log_test("SuperGateway Manager import", True)

            # Test core configuration
            from core.config import Config

            config = Config()
            self.log_test("Core configuration", True)

            return True

        except Exception as e:
            self.log_test("CERBERUS manager test", False, str(e))
            return False

    def test_n8n_integration(self):
        """Test N8N integration"""
        print("\n🔄 Testing N8N Integration...")

        try:
            # Test N8N API routes import
            from api.routes.n8n_workflows import n8n_router

            self.log_test("N8N router import", True)

            # Check N8N directory structure
            n8n_dir = self.project_root / "n8n"
            if n8n_dir.exists():
                self.log_test("N8N directory exists", True)

                # Check for key files
                package_json = n8n_dir / "package.json"
                if package_json.exists():
                    self.log_test("N8N package.json exists", True)
                else:
                    self.log_test("N8N package.json missing", False)
                    return False
            else:
                self.log_test("N8N directory missing", False)
                print("    Run ./build_n8n.sh to set up N8N")
                return False

            # Test N8N build script
            build_script = self.project_root / "build_n8n.sh"
            if build_script.exists():
                self.log_test("N8N build script exists", True)
            else:
                self.log_test("N8N build script missing", False)

            return True

        except Exception as e:
            self.log_test("N8N integration test", False, str(e))
            return False


def main():
    """Run integration tests"""
    print("🚀 CERBERUS-FANGS Integration Test Suite")
    print("=" * 50)

    tester = IntegrationTester()

    # Run all tests
    tester.test_metabigor_integration()
    tester.test_metasploit_integration()
    tester.test_cerberus_manager()
    tester.test_n8n_integration()

    # Generate final report
    print("\n" + "=" * 60)
    print("📊 INTEGRATION TEST REPORT")
    print("=" * 60)

    total_tests = len(tester.test_results)
    passed_tests = sum(1 for r in tester.test_results if r["success"])
    failed_tests = total_tests - passed_tests

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    if failed_tests > 0:
        print("\n❌ Failed Tests:")
        for result in tester.test_results:
            if not result["success"]:
                print(f"  - {result['test']}: {result['details']}")

    if failed_tests == 0:
        print("\n🎉 All integrations ready!")
        print("You can now:")
        print("1. Run: ./deploy_integrations.sh")
        print("2. Build N8N: ./build_n8n.sh")
        print("3. Start services: ./start_cerberus.sh")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed. Check the report above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
