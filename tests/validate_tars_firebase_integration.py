#!/usr/bin/env python3
"""
TARS API and Firebase Integration Validation Test
"""

import asyncio
import sys
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")

    try:
        from core.firebase_config import FirebaseConfig, get_firebase

        print("✅ Firebase config import successful")
    except ImportError as e:
        print(f"❌ Firebase config import failed: {e}")
        return False

    try:
        from api.routes.tars_api import router

        print("✅ TARS API router import successful")
    except ImportError as e:
        print(f"❌ TARS API router import failed: {e}")
        return False

    return True


def test_firebase_config():
    """Test Firebase configuration"""
    print("\n🔧 Testing Firebase configuration...")

    try:
        from core.firebase_config import FirebaseConfig

        config = FirebaseConfig()
        print("✅ Firebase config instance created")

        # Test config loading
        config_data = config._load_config()
        print(f"✅ Config loaded: project_id={config_data.get('project_id')}")

        return True
    except Exception as e:
        print(f"❌ Firebase config test failed: {e}")
        return False


def test_app_integration():
    """Test app integration"""
    print("\n🚀 Testing app integration...")

    try:
        # Check if app.py can be imported
        sys.path.insert(0, str(Path.cwd()))

        # Test that the imports work
        from app import app

        print("✅ FastAPI app import successful")

        # Check if TARS router is included
        routes = [route.path for route in app.routes]
        tars_routes = [r for r in routes if "/tars" in r]

        if tars_routes:
            print(f"✅ TARS routes found: {tars_routes}")
        else:
            print("❌ No TARS routes found in app")
            return False

        return True
    except Exception as e:
        print(f"❌ App integration test failed: {e}")
        return False


async def main():
    """Main validation function"""
    print("🛡️ LANCELOTT - TARS API & Firebase Integration Validation")
    print("=" * 60)

    tests = [
        ("Import Tests", test_imports),
        ("Firebase Config", test_firebase_config),
        ("App Integration", test_app_integration),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")

    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All integration tests PASSED!")
        print("\n📋 Next Steps:")
        print("1. Configure Firebase service account")
        print("2. Set environment variables")
        print("3. Start the application: python app.py")
        print("4. Test TARS endpoints with authentication")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
