#!/usr/bin/env python3
"""
Firebase Configuration Verification Script
Tests that Firebase service account is properly configured and accessible
"""

import json
import os
import sys
from pathlib import Path


def verify_firebase_config():
    """Verify Firebase configuration and service account setup"""

    print("🔥 Firebase Configuration Verification")
    print("=" * 50)

    # Check environment variables
    env_vars = [
        "FIREBASE_PROJECT_ID",
        "FIREBASE_API_KEY",
        "FIREBASE_AUTH_DOMAIN",
        "FIREBASE_STORAGE_BUCKET",
        "FIREBASE_SERVICE_ACCOUNT_PATH",
    ]

    print("\n📋 Environment Variables:")
    missing_vars = []

    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "API_KEY" in var:
                display_value = f"{value[:10]}..." if len(value) > 10 else value
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: NOT SET")
            missing_vars.append(var)

    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        return False

    # Check service account file
    service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
    print(f"\n🔑 Service Account File:")
    print(f"  Path: {service_account_path}")

    if not service_account_path:
        print("  ❌ Service account path not configured")
        return False

    # Convert relative path to absolute
    if service_account_path.startswith("./"):
        service_account_path = os.path.join(os.getcwd(), service_account_path[2:])

    service_account_file = Path(service_account_path)

    if not service_account_file.exists():
        print(f"  ❌ Service account file not found: {service_account_path}")
        return False

    print(f"  ✅ File exists: {service_account_file}")
    print(f"  📊 File size: {service_account_file.stat().st_size} bytes")

    # Validate JSON structure
    try:
        with open(service_account_file, "r") as f:
            service_account_data = json.load(f)

        required_fields = [
            "type",
            "project_id",
            "private_key_id",
            "private_key",
            "client_email",
            "client_id",
            "auth_uri",
            "token_uri",
        ]

        print("\n🔍 Service Account JSON Structure:")
        missing_fields = []

        for field in required_fields:
            if field in service_account_data:
                print(f"  ✅ {field}: Present")
            else:
                print(f"  ❌ {field}: Missing")
                missing_fields.append(field)

        if missing_fields:
            print(f"\n⚠️  Missing required fields: {', '.join(missing_fields)}")
            return False

        # Verify project ID matches
        env_project_id = os.getenv("FIREBASE_PROJECT_ID")
        json_project_id = service_account_data.get("project_id")

        print(f"\n🎯 Project ID Verification:")
        print(f"  Environment: {env_project_id}")
        print(f"  Service Account: {json_project_id}")

        if env_project_id != json_project_id:
            print("  ❌ Project ID mismatch!")
            return False
        else:
            print("  ✅ Project IDs match")

        print(f"\n📧 Service Account Email: {service_account_data.get('client_email')}")

    except json.JSONDecodeError as e:
        print(f"  ❌ Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        return False

    # Check directory structure
    print(f"\n📁 Directory Structure:")
    config_dir = Path("config")
    firebase_dir = config_dir / "firebase"

    print(f"  config/: {'✅ Exists' if config_dir.exists() else '❌ Missing'}")
    print(
        f"  config/firebase/: {'✅ Exists' if firebase_dir.exists() else '❌ Missing'}"
    )

    if firebase_dir.exists():
        firebase_files = list(firebase_dir.glob("*"))
        print(f"  Firebase files: {len(firebase_files)} found")
        for file in firebase_files:
            print(f"    - {file.name}")

    print(f"\n🎉 Firebase Configuration Status: ✅ VALID")
    print("\n🚀 Ready to initialize Firebase services!")
    return True


if __name__ == "__main__":
    # Load environment variables from .env file
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed, skipping .env file loading")

    success = verify_firebase_config()
    sys.exit(0 if success else 1)
