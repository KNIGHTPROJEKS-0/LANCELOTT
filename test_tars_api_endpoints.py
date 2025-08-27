#!/usr/bin/env python3
"""
TARS API Endpoint Testing Script
Tests all TARS API endpoints with proper authentication
"""

import json
import subprocess
import time
from datetime import datetime
from typing import Any, Dict, Optional

import requests


class TARSAPITester:
    def __init__(self, base_url: str = "http://localhost:7777"):
        self.base_url = base_url
        self.auth_token: Optional[str] = None
        self.session = requests.Session()

    def wait_for_server(self, max_attempts: int = 30, delay: int = 2) -> bool:
        """Wait for the server to be ready"""
        print(f"🔄 Waiting for LANCELOTT server at {self.base_url}...")

        for attempt in range(max_attempts):
            try:
                response = self.session.get(f"{self.base_url}/", timeout=5)
                if response.status_code == 200:
                    print("✅ Server is ready!")
                    return True
            except requests.exceptions.RequestException:
                pass

            print(f"   Attempt {attempt + 1}/{max_attempts} - waiting {delay}s...")
            time.sleep(delay)

        print("❌ Server failed to start or is not responding")
        return False

    def authenticate(
        self, email: str = "admin@lancelott.com", password: str = "admin123"
    ) -> bool:
        """Authenticate and get JWT token"""
        print("🔐 Authenticating...")

        try:
            auth_data = {"email": email, "password": password}

            response = self.session.post(
                f"{self.base_url}/api/v1/auth/login",
                json=auth_data,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                token_data = response.json()
                self.auth_token = token_data.get("access_token")
                if self.auth_token:
                    self.session.headers.update(
                        {"Authorization": f"Bearer {self.auth_token}"}
                    )
                    print("✅ Authentication successful!")
                    return True

            print(f"❌ Authentication failed: {response.status_code} - {response.text}")
            return False

        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False

    def test_endpoint(
        self,
        method: str,
        endpoint: str,
        data: Dict[Any, Any] = None,
        expected_status: int = 200,
    ) -> Dict[str, Any]:
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            result = {
                "success": response.status_code == expected_status,
                "status_code": response.status_code,
                "response": None,
                "error": None,
            }

            try:
                result["response"] = response.json()
            except:
                result["response"] = response.text

            if not result["success"]:
                result["error"] = (
                    f"Expected {expected_status}, got {response.status_code}"
                )

            return result

        except Exception as e:
            return {
                "success": False,
                "status_code": None,
                "response": None,
                "error": str(e),
            }

    def test_tars_status(self) -> bool:
        """Test TARS status endpoint"""
        print("\n📊 Testing TARS Status endpoint...")

        result = self.test_endpoint("GET", "/api/v1/tars/status")

        if result["success"]:
            print("✅ TARS Status endpoint working!")
            response = result["response"]
            if isinstance(response, dict):
                print(
                    f"   🤖 Agent running: {response.get('agent_running', 'unknown')}"
                )
                print(f"   🖥️  UI running: {response.get('ui_running', 'unknown')}")
                print(
                    f"   🔥 Firebase connected: {response.get('firebase_connected', 'unknown')}"
                )

                if "firebase_status" in response:
                    fb_status = response["firebase_status"]
                    print(f"   📊 Firebase details:")
                    print(f"      - Initialized: {fb_status.get('initialized', False)}")
                    print(f"      - Firestore: {fb_status.get('firestore', False)}")
                    print(f"      - Storage: {fb_status.get('storage', False)}")
                    print(f"      - Auth: {fb_status.get('auth', False)}")
            return True
        else:
            print(f"❌ TARS Status failed: {result['error']}")
            print(f"   Status Code: {result['status_code']}")
            print(f"   Response: {result['response']}")
            return False

    def test_agent_start(self) -> bool:
        """Test starting TARS agent"""
        print("\n🚀 Testing TARS Agent Start...")

        result = self.test_endpoint("POST", "/api/v1/tars/agent/start")

        if result["success"]:
            print("✅ TARS Agent start endpoint working!")
            response = result["response"]
            if isinstance(response, dict):
                print(f"   📝 Message: {response.get('message', 'No message')}")
                print(f"   🆔 Process ID: {response.get('process_id', 'No ID')}")
                if "data" in response and response["data"]:
                    data = response["data"]
                    print(f"   📊 Details:")
                    print(f"      - PID: {data.get('pid', 'unknown')}")
                    print(f"      - Command: {data.get('command', 'unknown')}")
            return True
        else:
            print(f"❌ TARS Agent start failed: {result['error']}")
            print(f"   Status Code: {result['status_code']}")
            print(f"   Response: {result['response']}")
            return False

    def test_ui_start(self) -> bool:
        """Test starting TARS UI"""
        print("\n🖥️  Testing TARS UI Start...")

        result = self.test_endpoint("POST", "/api/v1/tars/ui/start")

        if result["success"]:
            print("✅ TARS UI start endpoint working!")
            response = result["response"]
            if isinstance(response, dict):
                print(f"   📝 Message: {response.get('message', 'No message')}")
                print(f"   🆔 Process ID: {response.get('process_id', 'No ID')}")
            return True
        else:
            print(f"❌ TARS UI start failed: {result['error']}")
            print(f"   Status Code: {result['status_code']}")
            print(f"   Response: {result['response']}")
            return False

    def test_agent_command(self) -> bool:
        """Test sending command to TARS agent"""
        print("\n📤 Testing TARS Agent Command...")

        command_data = {
            "command": "test_scan",
            "parameters": {"target": "127.0.0.1", "type": "quick"},
            "timeout": 60,
        }

        result = self.test_endpoint("POST", "/api/v1/tars/agent/command", command_data)

        if result["success"]:
            print("✅ TARS Agent command endpoint working!")
            response = result["response"]
            if isinstance(response, dict):
                print(f"   📝 Message: {response.get('message', 'No message')}")
                if "data" in response:
                    data = response["data"]
                    print(f"   📊 Command details:")
                    print(f"      - Command: {data.get('command', 'unknown')}")
                    print(f"      - Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ TARS Agent command failed: {result['error']}")
            print(f"   Status Code: {result['status_code']}")
            print(f"   Response: {result['response']}")
            return False

    def test_logs_retrieval(self) -> bool:
        """Test retrieving TARS logs"""
        print("\n📜 Testing TARS Logs Retrieval...")

        result = self.test_endpoint("GET", "/api/v1/tars/logs?limit=5")

        if result["success"]:
            print("✅ TARS Logs endpoint working!")
            response = result["response"]
            if isinstance(response, dict) and "events" in response:
                events = response["events"]
                print(f"   📊 Retrieved {len(events)} events")
                for i, event in enumerate(events[:3]):  # Show first 3 events
                    print(f"   Event {i+1}:")
                    print(f"      - Type: {event.get('event_type', 'unknown')}")
                    print(f"      - Timestamp: {event.get('timestamp', 'unknown')}")
                    print(f"      - User: {event.get('user', 'unknown')}")
            return True
        else:
            print(f"❌ TARS Logs retrieval failed: {result['error']}")
            print(f"   Status Code: {result['status_code']}")
            print(f"   Response: {result['response']}")
            return False

    def test_unauthorized_access(self) -> bool:
        """Test that endpoints require authentication"""
        print("\n🔒 Testing Unauthorized Access Protection...")

        # Temporarily remove auth header
        temp_headers = self.session.headers.copy()
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]

        try:
            result = self.test_endpoint(
                "GET", "/api/v1/tars/status", expected_status=401
            )

            # Restore auth header
            self.session.headers.update(temp_headers)

            if result["success"]:
                print("✅ Unauthorized access properly blocked!")
                return True
            else:
                print(f"❌ Unauthorized access not properly blocked: {result['error']}")
                return False
        except Exception as e:
            # Restore auth header
            self.session.headers.update(temp_headers)
            print(f"❌ Error testing unauthorized access: {e}")
            return False

    def run_all_tests(self) -> Dict[str, bool]:
        """Run all TARS API tests"""
        print("🛡️ LANCELOTT - TARS API Integration Testing")
        print("=" * 60)

        # Wait for server
        if not self.wait_for_server():
            return {"server_ready": False}

        # Authenticate
        if not self.authenticate():
            return {"server_ready": True, "authentication": False}

        # Run tests
        test_results = {
            "server_ready": True,
            "authentication": True,
            "status_endpoint": self.test_tars_status(),
            "agent_start": self.test_agent_start(),
            "ui_start": self.test_ui_start(),
            "agent_command": self.test_agent_command(),
            "logs_retrieval": self.test_logs_retrieval(),
            "unauthorized_protection": self.test_unauthorized_access(),
        }

        # Summary
        print("\n" + "=" * 60)
        print("🎯 TEST RESULTS SUMMARY")
        print("=" * 60)

        passed = sum(1 for result in test_results.values() if result)
        total = len(test_results)

        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name.replace('_', ' ').title()}")

        print(f"\n📊 Overall: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All TARS API tests PASSED!")
            print("\n✅ Backend Integration is fully operational!")
        else:
            print("⚠️  Some tests failed. Check the results above.")

        return test_results


def main():
    """Main test function"""
    tester = TARSAPITester()
    results = tester.run_all_tests()

    # Return exit code based on results
    if all(results.values()):
        print("\n🚀 TARS API integration is ready for production!")
        return 0
    else:
        print("\n⚠️  TARS API integration needs attention.")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
