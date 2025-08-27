#!/usr/bin/env python3
"""
Firebase Authentication Setup Script for LANCELOTT
Sets up Firebase Authentication with admin user configuration

This script configures Firebase Authentication, creates the admin user,
and sets up the necessary security rules and permissions.

Author: LANCELOTT Development Team
Version: 2.1.0
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from integrations.firebase_auth import FirebaseAuth
    from integrations.firebase_integration import get_firebase_manager
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root")
    sys.exit(1)


class FirebaseAuthSetup:
    """
    Firebase Authentication Setup and Configuration
    """

    def __init__(self):
        self.firebase_manager = get_firebase_manager()
        self.firebase_auth = FirebaseAuth()
        self.admin_email = "knightprojeks@gmail.com"
        self.admin_display_name = "LANCELOTT Admin"

    def initialize_firebase(self) -> bool:
        """Initialize Firebase connection"""
        print("🔥 Initializing Firebase connection...")

        if not self.firebase_manager.initialize():
            print("❌ Failed to initialize Firebase")
            return False

        print("✅ Firebase initialized successfully")
        return True

    def create_admin_user_profile(self, uid: str) -> bool:
        """Create admin user profile in Firestore"""
        try:
            print(f"👤 Creating admin user profile for UID: {uid}")

            # Admin permissions
            admin_permissions = [
                "admin:all",
                "read:all_scans",
                "create:scans",
                "delete:scans",
                "read:all_users",
                "manage:users",
                "manage:tools",
                "manage:system",
                "access:dashboard",
                "access:api",
                "access:dataconnect",
                "manage:firebase",
            ]

            # Create comprehensive admin profile
            success = self.firebase_auth.create_user_profile(
                uid=uid,
                email=self.admin_email,
                display_name=self.admin_display_name,
                role="admin",
                permissions=admin_permissions,
            )

            if success:
                print("✅ Admin user profile created successfully")

                # Add additional admin settings
                additional_settings = {
                    "is_super_admin": True,
                    "created_by_system": True,
                    "setup_completed": True,
                    "dashboard_access": True,
                    "api_access": True,
                    "data_connect_access": True,
                    "firebase_console_access": True,
                    "last_profile_update": datetime.now().isoformat(),
                    "profile_version": "2.1.0",
                }

                # Update with additional settings
                self.firebase_auth.update_user_profile(uid, additional_settings)
                print("✅ Admin settings configured")
                return True
            else:
                print("❌ Failed to create admin user profile")
                return False

        except Exception as e:
            print(f"❌ Error creating admin user profile: {e}")
            return False

    def setup_firestore_security_rules(self) -> bool:
        """Update Firestore security rules for proper authentication"""
        try:
            print("🔐 Setting up Firestore security rules...")

            # Read current rules
            rules_path = project_root / "firestore.rules"
            if not rules_path.exists():
                print("❌ firestore.rules file not found")
                return False

            # Enhanced security rules with admin support
            enhanced_rules = """rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    // Admin users have full access
    function isAdmin() {
      return request.auth != null &&
             get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }

    // Check if user is authenticated
    function isAuthenticated() {
      return request.auth != null;
    }

    // Check if user owns the resource
    function isOwner(userId) {
      return request.auth != null && request.auth.uid == userId;
    }

    // Check if user has specific permission
    function hasPermission(permission) {
      return request.auth != null &&
             permission in get(/databases/$(database)/documents/users/$(request.auth.uid)).data.permissions;
    }

    // Users collection - admin can read all, users can read/write own
    match /users/{userId} {
      allow read: if isAdmin() || isOwner(userId);
      allow write: if isAdmin() || (isOwner(userId) &&
                                  !('role' in resource.data || 'permissions' in resource.data));
      allow create: if isAdmin();
    }

    // Scan results - admin can read all, users can read/write own
    match /scan_results/{scanId} {
      allow read: if isAdmin() ||
                     isOwner(resource.data.user_id) ||
                     hasPermission('read:all_scans');
      allow write: if isAdmin() ||
                      isOwner(resource.data.user_id) ||
                      hasPermission('create:scans');
      allow create: if isAuthenticated();
    }

    // System logs - admin only
    match /system_logs/{logId} {
      allow read, write: if isAdmin();
    }

    // Scan webhooks - admin and system access
    match /scan_webhooks/{webhookId} {
      allow read, write: if isAdmin();
    }

    // Health check collection - authenticated users
    match /health_check/{document} {
      allow read, write: if isAuthenticated();
    }

    // API keys - users can manage their own, admin can manage all
    match /api_keys/{keyId} {
      allow read, write: if isAdmin() || isOwner(resource.data.user_id);
    }

    // Tool configurations - admin only
    match /tool_configs/{toolId} {
      allow read: if isAuthenticated();
      allow write: if isAdmin() || hasPermission('manage:tools');
    }

    // Reports - users can read own, admin can read all
    match /reports/{reportId} {
      allow read: if isAdmin() ||
                     isOwner(resource.data.user_id) ||
                     hasPermission('read:all_scans');
      allow write: if isAdmin() || isOwner(resource.data.user_id);
    }
  }
}"""

            # Write enhanced rules
            with open(rules_path, "w") as f:
                f.write(enhanced_rules)

            print("✅ Firestore security rules updated")
            return True

        except Exception as e:
            print(f"❌ Error setting up security rules: {e}")
            return False

    def setup_storage_security_rules(self) -> bool:
        """Update Storage security rules for proper authentication"""
        try:
            print("📁 Setting up Storage security rules...")

            rules_path = project_root / "storage.rules"
            if not rules_path.exists():
                print("❌ storage.rules file not found")
                return False

            # Enhanced storage rules
            enhanced_storage_rules = """rules_version = '2';

service firebase.storage {
  match /b/{bucket}/o {
    // Admin users have full access
    function isAdmin() {
      return request.auth != null &&
             firestore.get(/databases/(default)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }

    // Check if user is authenticated
    function isAuthenticated() {
      return request.auth != null;
    }

    // User uploads - authenticated users can upload to their own directory
    match /uploads/{userId}/{allPaths=**} {
      allow read, write: if isAdmin() || (isAuthenticated() && request.auth.uid == userId);
    }

    // Scan results - authenticated users can read, admin can write
    match /scan_results/{allPaths=**} {
      allow read: if isAuthenticated();
      allow write: if isAdmin();
    }

    // Reports - similar to scan results
    match /reports/{allPaths=**} {
      allow read: if isAuthenticated();
      allow write: if isAdmin();
    }

    // Public assets - anyone can read
    match /public/{allPaths=**} {
      allow read: if true;
      allow write: if isAdmin();
    }

    // Tool outputs - authenticated users
    match /tool_outputs/{allPaths=**} {
      allow read: if isAuthenticated();
      allow write: if isAdmin();
    }

    // System files - admin only
    match /system/{allPaths=**} {
      allow read, write: if isAdmin();
    }
  }
}"""

            # Write enhanced storage rules
            with open(rules_path, "w") as f:
                f.write(enhanced_storage_rules)

            print("✅ Storage security rules updated")
            return True

        except Exception as e:
            print(f"❌ Error setting up storage rules: {e}")
            return False

    def create_firebase_config_file(self) -> bool:
        """Create Firebase client configuration file"""
        try:
            print("⚙️ Creating Firebase client configuration...")

            # Create config directory if it doesn't exist
            config_dir = project_root / "static" / "js"
            config_dir.mkdir(parents=True, exist_ok=True)

            # Firebase client configuration
            firebase_config = {
                "apiKey": os.getenv("FIREBASE_API_KEY"),
                "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
                "projectId": os.getenv("FIREBASE_PROJECT_ID"),
                "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
                "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
                "appId": os.getenv("FIREBASE_APP_ID"),
            }

            # Create JavaScript config file
            js_config = f"""// Firebase Configuration for LANCELOTT
// Auto-generated by Firebase Auth Setup Script

const firebaseConfig = {json.dumps(firebase_config, indent=2)};

// Initialize Firebase
import {{ initializeApp }} from 'firebase/app';
import {{ getAuth }} from 'firebase/auth';
import {{ getFirestore }} from 'firebase/firestore';
import {{ getStorage }} from 'firebase/storage';

const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);

export default app;
"""

            # Write JavaScript config
            js_config_path = config_dir / "firebase-config.js"
            with open(js_config_path, "w") as f:
                f.write(js_config)

            # Create JSON config for other uses
            json_config_path = config_dir / "firebase-config.json"
            with open(json_config_path, "w") as f:
                json.dump(firebase_config, f, indent=2)

            print("✅ Firebase client configuration created")
            return True

        except Exception as e:
            print(f"❌ Error creating Firebase config: {e}")
            return False

    def setup_authentication_flow(self) -> bool:
        """Set up authentication flow and test endpoints"""
        try:
            print("🔐 Setting up authentication flow...")

            # Create authentication test script
            auth_test_script = '''#!/usr/bin/env python3
"""
Firebase Authentication Test Script
Tests Firebase authentication setup and admin user access
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime

async def test_firebase_auth():
    """Test Firebase authentication endpoints"""

    base_url = "http://localhost:7777"
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }

    async with aiohttp.ClientSession() as session:

        # Test 1: Health check
        try:
            async with session.get(f"{base_url}/health") as response:
                test_results["tests"].append({
                    "name": "Health Check",
                    "status": "PASS" if response.status == 200 else "FAIL",
                    "response_code": response.status
                })
        except Exception as e:
            test_results["tests"].append({
                "name": "Health Check",
                "status": "FAIL",
                "error": str(e)
            })

        # Test 2: Firebase status
        try:
            async with session.get(f"{base_url}/api/v1/firebase/status") as response:
                test_results["tests"].append({
                    "name": "Firebase Status",
                    "status": "PASS" if response.status == 200 else "FAIL",
                    "response_code": response.status
                })
        except Exception as e:
            test_results["tests"].append({
                "name": "Firebase Status",
                "status": "FAIL",
                "error": str(e)
            })

        # Test 3: Auth endpoints
        try:
            async with session.get(f"{base_url}/api/v1/auth/config") as response:
                test_results["tests"].append({
                    "name": "Auth Config",
                    "status": "PASS" if response.status == 200 else "FAIL",
                    "response_code": response.status
                })
        except Exception as e:
            test_results["tests"].append({
                "name": "Auth Config",
                "status": "FAIL",
                "error": str(e)
            })

    # Print results
    print("🧪 Firebase Authentication Test Results")
    print("=" * 50)
    for test in test_results["tests"]:
        status_emoji = "✅" if test["status"] == "PASS" else "❌"
        print(f"{status_emoji} {test['name']}: {test['status']}")
        if "error" in test:
            print(f"   Error: {test['error']}")

    passed_tests = len([t for t in test_results["tests"] if t["status"] == "PASS"])
    total_tests = len(test_results["tests"])
    print(f"\\n📊 Results: {passed_tests}/{total_tests} tests passed")

    return test_results

if __name__ == "__main__":
    asyncio.run(test_firebase_auth())
'''

            # Write test script
            test_script_path = project_root / "scripts" / "test_firebase_auth.py"
            with open(test_script_path, "w") as f:
                f.write(auth_test_script)

            # Make it executable
            os.chmod(test_script_path, 0o755)

            print("✅ Authentication flow setup completed")
            return True

        except Exception as e:
            print(f"❌ Error setting up auth flow: {e}")
            return False

    def run_setup(self) -> bool:
        """Run complete Firebase Auth setup"""
        print("🚀 Starting Firebase Authentication Setup for LANCELOTT")
        print("=" * 60)
        print(f"📧 Admin Email: {self.admin_email}")
        print(f"👤 Admin Display Name: {self.admin_display_name}")
        print(f"🔥 Firebase Project: {os.getenv('FIREBASE_PROJECT_ID')}")
        print()

        # Step 1: Initialize Firebase
        if not self.initialize_firebase():
            return False

        # Step 2: Check if admin user exists in Firebase Auth
        print("🔍 Checking for existing admin user...")
        try:
            # Try to get user by email (this will fail if user doesn't exist)
            from firebase_admin import auth as firebase_auth

            try:
                existing_user = firebase_auth.get_user_by_email(self.admin_email)
                print(f"✅ Admin user already exists with UID: {existing_user.uid}")
                admin_uid = existing_user.uid

                # Update the existing user profile
                self.create_admin_user_profile(admin_uid)

            except firebase_auth.UserNotFoundError:
                print("❌ Admin user not found in Firebase Auth")
                print("📝 You need to create the admin user account first")
                print()
                print("🔧 MANUAL SETUP REQUIRED:")
                print("1. Go to Firebase Console: https://console.firebase.google.com")
                print(f"2. Open your project: {os.getenv('FIREBASE_PROJECT_ID')}")
                print("3. Go to Authentication > Users")
                print("4. Click 'Add user'")
                print(f"5. Email: {self.admin_email}")
                print("6. Password: [Your chosen password]")
                print("7. Save the user")
                print("8. Run this script again")
                print()

                # Create the user in Firebase Auth (if we have admin privileges)
                try:
                    print("🔄 Attempting to create admin user...")
                    user_record = firebase_auth.create_user(
                        email=self.admin_email,
                        email_verified=True,
                        display_name=self.admin_display_name,
                    )
                    print(f"✅ Admin user created with UID: {user_record.uid}")
                    admin_uid = user_record.uid

                    # Create user profile
                    self.create_admin_user_profile(admin_uid)

                except Exception as create_error:
                    print(f"❌ Failed to create user: {create_error}")
                    print("Please create the user manually in Firebase Console")
                    return False

        except Exception as e:
            print(f"❌ Error checking admin user: {e}")
            return False

        # Step 3: Setup security rules
        if not self.setup_firestore_security_rules():
            print("⚠️ Warning: Failed to setup Firestore rules")

        if not self.setup_storage_security_rules():
            print("⚠️ Warning: Failed to setup Storage rules")

        # Step 4: Create client configuration
        if not self.create_firebase_config_file():
            print("⚠️ Warning: Failed to create client config")

        # Step 5: Setup authentication flow
        if not self.setup_authentication_flow():
            print("⚠️ Warning: Failed to setup auth flow")

        print()
        print("✅ Firebase Authentication Setup Completed!")
        print()
        print("🔗 Next Steps:")
        print("1. Deploy Firestore rules: firebase deploy --only firestore:rules")
        print("2. Deploy Storage rules: firebase deploy --only storage")
        print("3. Test authentication: python scripts/test_firebase_auth.py")
        print("4. Access dashboard: https://lancelott-z9dko.web.app")
        print()
        print("🔐 Login Details:")
        print(f"📧 Email: {self.admin_email}")
        print("🔑 Password: [Set in Firebase Console]")
        print("👑 Role: Admin")
        print()

        return True


def main():
    """Main function"""
    try:
        setup = FirebaseAuthSetup()
        success = setup.run_setup()

        if success:
            print("🎉 Setup completed successfully!")
            return 0
        else:
            print("❌ Setup failed!")
            return 1

    except KeyboardInterrupt:
        print("\n⚠️ Setup interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
