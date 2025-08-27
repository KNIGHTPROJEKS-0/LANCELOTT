#!/usr/bin/env python3
"""
Integration test for SuperGateway and SuperCompat
Tests the new tools within the CERBERUS-FANGS LANCELOTT framework
"""

import asyncio
import sys
from pathlib import Path

import pytest

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from core.supercompat_manager import SuperCompatManager
from core.supergateway_manager import SuperGatewayManager


@pytest.mark.asyncio
async def test_supergateway():
    """Test SuperGateway functionality"""
    print("🌉 Testing SuperGateway...")

    gateway_manager = SuperGatewayManager()

    # Check availability
    is_available = await gateway_manager.is_available()
    print(f"  SuperGateway available: {'✅' if is_available else '❌'}")

    if not is_available:
        print(
            "  ⚠️  SuperGateway not built. Run 'npm run build' in SuperGateway directory."
        )
        return False

    # Test listing gateways (should be empty initially)
    gateways = await gateway_manager.list_gateways()
    print(f"  Active gateways: {gateways['active_gateways']}")

    print("  ✅ SuperGateway basic functionality working")
    return True


@pytest.mark.asyncio
async def test_supercompat():
    """Test SuperCompat functionality"""
    print("🤖 Testing SuperCompat...")

    compat_manager = SuperCompatManager()

    # Check availability
    is_available = await compat_manager.is_available()
    print(f"  SuperCompat available: {'✅' if is_available else '❌'}")

    if not is_available:
        # Try to build
        print("  🔧 Attempting to build SuperCompat...")
        build_success = await compat_manager.build_if_needed()
        print(f"  Build result: {'✅' if build_success else '❌'}")

        if not build_success:
            print(
                "  ⚠️  SuperCompat build failed. Check npm installation in SuperCompat/packages/supercompat/"
            )
            return False

    # Test listing sessions (should be empty initially)
    sessions = await compat_manager.list_sessions()
    print(f"  Active sessions: {sessions['active_sessions']}")

    # Test supported providers
    providers = await compat_manager.get_supported_providers()
    print(f"  Supported providers: {', '.join(providers)}")

    print("  ✅ SuperCompat basic functionality working")
    return True


@pytest.mark.asyncio
async def test_integration():
    """Test overall integration"""
    print("\n🛡️ CERBERUS-FANGS LANCELOTT - SuperTools Integration Test")
    print("=" * 60)

    results = []

    # Test SuperGateway
    gateway_result = await test_supergateway()
    results.append(("SuperGateway", gateway_result))

    print()

    # Test SuperCompat
    compat_result = await test_supercompat()
    results.append(("SuperCompat", compat_result))

    # Summary
    print("\n📊 Test Results:")
    print("-" * 30)

    for tool, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {tool}: {status}")

    success_count = sum(1 for _, result in results if result)
    total_count = len(results)

    print(f"\n🎯 Overall: {success_count}/{total_count} tools working")

    if success_count == total_count:
        print("🎉 All SuperTools integrated successfully!")
        print("\n🚀 Next steps:")
        print("  1. Run: scripts/quick_setup.sh")
        print("  2. Start: python main.py")
        print("  3. Visit: http://localhost:7777/docs")
        print("  4. Test the new /supergateway and /supercompat endpoints")
    else:
        print("⚠️  Some tools need attention. Check the error messages above.")

    return success_count == total_count


if __name__ == "__main__":
    asyncio.run(test_integration())
