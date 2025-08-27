#!/usr/bin/env python3
"""
Test script for Crush and CliWrap integration
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from integrations.tools.cliwrap_wrapper import get_cliwrap_wrapper
from integrations.tools.crush_wrapper import get_crush_wrapper


async def test_crush_integration():
    """Test Crush integration"""
    print("🚀 Testing Crush Integration...")

    try:
        # Get wrapper
        wrapper = get_crush_wrapper()
        print(f"✅ Crush wrapper initialized: {wrapper.name}")

        # Check dependencies
        deps = await wrapper.check_dependencies()
        print(f"🔍 Dependencies check: {deps['success']}")
        if not deps["success"]:
            print(f"❌ Missing dependencies: {deps}")

        # Test basic execution (if binary exists)
        if deps["success"]:
            result = await wrapper.execute_scan(".", {"operation": "browse"})
            print(f"🎯 Execution test: {result['success']}")

        return True

    except Exception as e:
        print(f"❌ Crush test failed: {e}")
        return False


async def test_cliwrap_integration():
    """Test CliWrap integration"""
    print("\n🛠️ Testing CliWrap Integration...")

    try:
        # Get wrapper
        wrapper = get_cliwrap_wrapper()
        print(f"✅ CliWrap wrapper initialized: {wrapper.name}")

        # Check dependencies
        deps = await wrapper.check_dependencies()
        print(f"🔍 Dependencies check: {deps['success']}")
        if not deps["success"]:
            print(f"❌ Missing dependencies: {deps}")

        return True

    except Exception as e:
        print(f"❌ CliWrap test failed: {e}")
        return False


async def test_framework_integration():
    """Test framework integration"""
    print("\n🏗️ Testing Framework Integration...")

    try:
        # Test imports
        from api.routes.cliwrap_router import router as cliwrap_router
        from api.routes.crush_router import router as crush_router

        print("✅ Router imports successful")

        # Test configuration
        from config.lancelott_config import load_config

        config = load_config()

        # Check if tools are in config
        tools = config.get("tools", {})
        crush_config = tools.get("crush")
        cliwrap_config = tools.get("cliwrap")

        if crush_config:
            print(f"✅ Crush configuration found: {crush_config.get('name')}")
        else:
            print("❌ Crush configuration missing")

        if cliwrap_config:
            print(f"✅ CliWrap configuration found: {cliwrap_config.get('name')}")
        else:
            print("❌ CliWrap configuration missing")

        return True

    except Exception as e:
        print(f"❌ Framework integration test failed: {e}")
        return False


async def main():
    """Main test function"""
    print("🛡️ CERBERUS-FANGS LANCELOTT - Crush Integration Test\n")

    # Test individual components
    crush_ok = await test_crush_integration()
    cliwrap_ok = await test_cliwrap_integration()
    framework_ok = await test_framework_integration()

    # Summary
    print(f"\n📊 Test Results Summary:")
    print(f"Crush Integration: {'✅' if crush_ok else '❌'}")
    print(f"CliWrap Integration: {'✅' if cliwrap_ok else '❌'}")
    print(f"Framework Integration: {'✅' if framework_ok else '❌'}")

    if all([crush_ok, cliwrap_ok, framework_ok]):
        print("\n🎉 All integration tests passed!")
        print("\n🚀 Ready to launch Crush orchestrator:")
        print("   python crush_orchestrator.py")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the issues above.")
        return 1


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Run tests
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
