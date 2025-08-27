#!/usr/bin/env python3
"""
Simple test script to verify CERBERUS-FANGS LANCELOTT basic functionality
"""

import os
import sys


def test_basic_imports():
    """Test if basic imports work"""
    print("🔍 Testing basic Python imports...")

    try:
        import asyncio
        import datetime
        import json

        print("✅ Basic Python modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import basic modules: {e}")
        return False


def test_fastapi_imports():
    """Test if FastAPI imports work"""
    print("🔍 Testing FastAPI imports...")

    try:
        import uvicorn

        import fastapi

        print("✅ FastAPI modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import FastAPI modules: {e}")
        print("💡 Run: pip install fastapi uvicorn")
        return False


def test_file_structure():
    """Test if required files exist"""
    print("🔍 Testing file structure...")

    required_files = [
        "main.py",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "startup.sh",
        "api/__init__.py",
        "core/__init__.py",
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True


def test_tool_directories():
    """Test if tool directories exist"""
    print("🔍 Testing tool directories...")

    tool_dirs = [
        "Argus",
        "Kraken",
        "Spiderfoot",
        "Social-Analyzer",
        "RedTeam-ToolKit",
        "Storm-Breaker",
        "PhoneSploit-Pro",
    ]

    existing_tools = []
    for tool in tool_dirs:
        if os.path.exists(tool):
            existing_tools.append(tool)

    print(f"✅ Found {len(existing_tools)}/{len(tool_dirs)} security tools")
    for tool in existing_tools:
        print(f"   📁 {tool}")

    return len(existing_tools) > 0


def test_port_config():
    """Test if port configuration is accessible"""
    print("🔍 Testing port configuration...")

    try:
        sys.path.append(".")
        from core.port_config import TOOL_PORTS

        print(f"✅ Port configuration loaded: {len(TOOL_PORTS)} tools configured")
        return True
    except Exception as e:
        print(f"❌ Failed to load port configuration: {e}")
        return False


def main():
    """Run all tests"""
    print("🐺 CERBERUS-FANGS LANCELOTT - System Test 🐺")
    print("=" * 50)

    tests = [
        test_basic_imports,
        test_fastapi_imports,
        test_file_structure,
        test_tool_directories,
        test_port_config,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! System ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Check the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
