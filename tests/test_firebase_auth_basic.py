#!/usr/bin/env python3
"""
Basic Firebase Authentication Test
Simple test to verify Firebase auth configuration
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_environment_variables():
    """Test if required environment variables are set"""
    print("🔍 Testing Environment Variables...")

    required_vars = [
        "FIREBASE_PROJECT_ID",
        "FIREBASE_API_KEY",
        "FIREBASE_AUTH_DOMAIN",
        "FIREBASE_SERVICE_ACCOUNT_PATH",
    ]

    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * min(len(value), 10)}...")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)

    return len(missing_vars) == 0


def test_firebase_files():
    """Test if required Firebase files exist"""
    print("\n📁 Testing Firebase Files...")

    required_files = [
        "firebase.json",
        ".firebaserc",
        "firestore.rules",
        "storage.rules",
        "dataconnect.yaml",
    ]

    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}: Found")
        else:
            print(f"❌ {file_path}: Not found")
            missing_files.append(file_path)

    return len(missing_files) == 0


def test_service_account():
    """Test service account file"""
    print("\n🔑 Testing Service Account...")

    sa_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
    if not sa_path:
        print("❌ Service account path not configured")
        return False

    sa_file = Path(sa_path)
    if not sa_file.exists():
        print(f"❌ Service account file not found: {sa_path}")
        return False

    print(f"✅ Service account file found: {sa_file.name}")

    # Try to read and validate JSON
    try:
        import json

        with open(sa_file, "r") as f:
            sa_data = json.load(f)

        if sa_data.get("type") == "service_account":
            print(f"✅ Valid service account for project: {sa_data.get('project_id')}")
            return True
        else:
            print("❌ Invalid service account type")
            return False

    except Exception as e:
        print(f"❌ Error reading service account: {e}")
        return False


def test_auth_imports():
    """Test if authentication modules can be imported"""
    print("\n📦 Testing Module Imports...")

    try:
        from integrations.firebase_integration import get_firebase_manager

        print("✅ firebase_integration imported")
    except Exception as e:
        print(f"❌ firebase_integration import failed: {e}")
        return False

    try:
        from integrations.firebase_auth import FirebaseAuth

        print("✅ firebase_auth imported")
    except Exception as e:
        print(f"❌ firebase_auth import failed: {e}")
        return False

    try:
        from api.routes.auth_routes import router

        print("✅ auth_routes imported")
    except Exception as e:
        print(f"❌ auth_routes import failed: {e}")
        return False

    return True


def test_firebase_initialization():
    """Test Firebase initialization"""
    print("\n🔥 Testing Firebase Initialization...")

    try:
        from integrations.firebase_integration import get_firebase_manager

        firebase_manager = get_firebase_manager()
        if firebase_manager.initialize():
            print("✅ Firebase initialized successfully")
            return True
        else:
            print("❌ Firebase initialization failed")
            return False

    except Exception as e:
        print(f"❌ Firebase initialization error: {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 LANCELOTT Firebase Authentication Basic Test")
    print("=" * 55)

    tests = [
        ("Environment Variables", test_environment_variables),
        ("Firebase Files", test_firebase_files),
        ("Service Account", test_service_account),
        ("Module Imports", test_auth_imports),
        ("Firebase Initialization", test_firebase_initialization),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ {test_name} test failed")
        except Exception as e:
            print(f"\n💥 {test_name} test error: {e}")

    print(f"\n📊 Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed! Firebase auth setup looks good.")
        print("\n🔧 Next Steps:")
        print("1. Create admin user in Firebase Console")
        print("2. Set password: Ggg123456789ggG!")
        print("3. Deploy with: ./deploy_firebase_auth.sh")
        print("4. Test login at dashboard")
        return 0
    else:
        print("❌ Some tests failed. Check configuration.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
