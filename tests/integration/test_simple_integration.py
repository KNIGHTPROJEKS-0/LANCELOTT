#!/usr/bin/env python3
"""
Simple integration test for SuperGateway and SuperCompat
Tests without loading the full configuration
"""

import asyncio
import os
from pathlib import Path


async def test_simple_integration():
    """Simple test without full config loading"""
    print("\n🛡️ CERBERUS-FANGS LANCELOTT - Simple SuperTools Integration Test")
    print("=" * 60)

    # Check directories exist
    supergateway_path = Path("./SuperGateway")
    supercompat_path = Path("./SuperCompat")

    print("🌉 SuperGateway:")
    print(f"  Directory exists: {'✅' if supergateway_path.exists() else '❌'}")

    if supergateway_path.exists():
        dist_path = supergateway_path / "dist" / "index.js"
        package_path = supergateway_path / "package.json"
        print(f"  Built (dist/index.js): {'✅' if dist_path.exists() else '❌'}")
        print(f"  Package.json: {'✅' if package_path.exists() else '❌'}")

        # Check Node modules
        node_modules = supergateway_path / "node_modules"
        print(f"  Dependencies installed: {'✅' if node_modules.exists() else '❌'}")

    print("\n🤖 SuperCompat:")
    print(f"  Directory exists: {'✅' if supercompat_path.exists() else '❌'}")

    if supercompat_path.exists():
        core_path = supercompat_path / "packages" / "supercompat"
        print(f"  Core package exists: {'✅' if core_path.exists() else '❌'}")

        if core_path.exists():
            dist_path = core_path / "dist" / "index.js"
            package_path = core_path / "package.json"
            print(f"  Built (dist/index.js): {'✅' if dist_path.exists() else '❌'}")
            print(f"  Package.json: {'✅' if package_path.exists() else '❌'}")

            # Check Node modules
            node_modules = core_path / "node_modules"
            print(
                f"  Dependencies installed: {'✅' if node_modules.exists() else '❌'}"
            )

    # Check Node.js availability
    print("\n🟢 Node.js Environment:")
    try:
        import subprocess

        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  Node.js version: ✅ {result.stdout.strip()}")
        else:
            print("  Node.js: ❌ Not available")
    except FileNotFoundError:
        print("  Node.js: ❌ Not found")

    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  npm version: ✅ {result.stdout.strip()}")
        else:
            print("  npm: ❌ Not available")
    except FileNotFoundError:
        print("  npm: ❌ Not found")

    # Test Python modules
    print("\n🐍 Python Dependencies:")
    try:
        import psutil

        print(f"  psutil: ✅ {psutil.__version__}")
    except ImportError:
        print("  psutil: ❌ Not installed")

    try:
        import fastapi

        print(f"  FastAPI: ✅ {fastapi.__version__}")
    except ImportError:
        print("  FastAPI: ❌ Not installed")

    print("\n📊 Integration Status:")

    gateway_ready = (
        supergateway_path.exists()
        and (supergateway_path / "dist" / "index.js").exists()
    )

    compat_ready = (
        supercompat_path.exists()
        and (
            supercompat_path / "packages" / "supercompat" / "dist" / "index.js"
        ).exists()
    )

    print(f"  SuperGateway: {'✅ Ready' if gateway_ready else '❌ Needs setup'}")
    print(f"  SuperCompat: {'✅ Ready' if compat_ready else '❌ Needs setup'}")

    if gateway_ready and compat_ready:
        print("\n🎉 Both SuperTools are ready for integration!")
        print("\n🚀 Next steps:")
        print("  1. Fix the configuration issue in core/config.py")
        print("  2. Run: scripts/quick_setup.sh")
        print("  3. Start: python main.py")
        print("  4. Test: http://localhost:7777/docs")
    else:
        print("\n⚠️  Some tools need building:")
        if not gateway_ready:
            print("  • SuperGateway: cd SuperGateway && npm install && npm run build")
        if not compat_ready:
            print(
                "  • SuperCompat: cd SuperCompat/packages/supercompat && npm install && npm run build"
            )


if __name__ == "__main__":
    asyncio.run(test_simple_integration())
