#!/usr/bin/env python3
"""
LANCELOTT Admin User Setup Script
Creates admin user account with specific credentials for knightprojeks@gmail.com

This script handles the complete setup of the admin user account
including Firebase Authentication and Firestore profile creation.

Author: LANCELOTT Development Team
Version: 2.1.0
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import firebase_admin
    from firebase_admin import auth as firebase_auth
    from firebase_admin import credentials

    from integrations.firebase_auth import FirebaseAuth
    from integrations.firebase_integration import get_firebase_manager
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install Firebase dependencies: pip install firebase-admin")
    sys.exit(1)


class AdminUserSetup:
    """
    Admin user setup and configuration
    """

    def __init__(self):
        self.admin_email = "knightprojeks@gmail.com"
        self.admin_display_name = "LANCELOTT Admin"
        self.firebase_manager = get_firebase_manager()
        self.firebase_auth = FirebaseAuth()

    def initialize_firebase(self) -> bool:
        """Initialize Firebase with admin privileges"""
        try:
            print("🔥 Initializing Firebase Admin SDK...")

            if not self.firebase_manager.initialize():
                print("❌ Failed to initialize Firebase")
                return False

            print("✅ Firebase initialized successfully")
            return True

        except Exception as e:
            print(f"❌ Firebase initialization error: {e}")
            return False

    def create_admin_user(self) -> str:
        """Create admin user in Firebase Authentication"""
        try:
            print(f"👤 Creating admin user: {self.admin_email}")

            # Check if user already exists
            try:
                existing_user = firebase_auth.get_user_by_email(self.admin_email)
                print(f"✅ Admin user already exists with UID: {existing_user.uid}")
                return existing_user.uid
            except firebase_auth.UserNotFoundError:
                print("👤 Admin user not found, creating new user...")

            # Create new user
            user_record = firebase_auth.create_user(
                email=self.admin_email,
                email_verified=True,
                display_name=self.admin_display_name,
                disabled=False,
            )

            print(f"✅ Admin user created successfully!")
            print(f"📧 Email: {user_record.email}")
            print(f"🆔 UID: {user_record.uid}")
            print(f"👤 Display Name: {user_record.display_name}")

            return user_record.uid

        except Exception as e:
            print(f"❌ Failed to create admin user: {e}")
            return None

    def create_admin_profile(self, uid: str) -> bool:
        """Create comprehensive admin profile in Firestore"""
        try:
            print(f"📋 Creating admin profile for UID: {uid}")

            # Comprehensive admin permissions
            admin_permissions = [
                # System permissions
                "admin:all",
                "system:manage",
                "system:monitor",
                "system:configure",
                # User management
                "users:read_all",
                "users:create",
                "users:update",
                "users:delete",
                "users:manage_roles",
                # Scan permissions
                "scans:read_all",
                "scans:create",
                "scans:update",
                "scans:delete",
                "scans:manage",
                # Tool permissions
                "tools:read_all",
                "tools:execute",
                "tools:configure",
                "tools:manage",
                # Dashboard access
                "dashboard:access",
                "dashboard:admin",
                "dashboard:manage",
                # API access
                "api:full_access",
                "api:admin",
                # Firebase permissions
                "firebase:admin",
                "firebase:dataconnect",
                "firebase:manage",
                # Reports and data
                "reports:read_all",
                "reports:create",
                "reports:manage",
                "data:export",
                "data:import",
            ]

            # Create admin profile
            success = self.firebase_auth.create_user_profile(
                uid=uid,
                email=self.admin_email,
                display_name=self.admin_display_name,
                role="admin",
                permissions=admin_permissions,
            )

            if not success:
                print("❌ Failed to create admin profile")
                return False

            # Add additional admin settings
            additional_settings = {
                "is_super_admin": True,
                "is_owner": True,
                "account_type": "admin",
                "created_by_system": True,
                "setup_completed": True,
                "profile_complete": True,
                # Access controls
                "dashboard_access": True,
                "api_access": True,
                "firebase_console_access": True,
                "data_connect_access": True,
                "admin_panel_access": True,
                # Security settings
                "two_factor_enabled": False,
                "password_reset_required": False,
                "account_locked": False,
                # Preferences
                "theme": "dark",
                "language": "en",
                "timezone": "UTC",
                "notifications_enabled": True,
                # Metadata
                "last_profile_update": datetime.now().isoformat(),
                "profile_version": "2.1.0",
                "setup_timestamp": datetime.now().isoformat(),
                "created_by": "system_setup_script",
            }

            # Update profile with additional settings
            self.firebase_auth.update_user_profile(uid, additional_settings)

            print("✅ Admin profile created successfully")
            print(f"🔑 Permissions granted: {len(admin_permissions)}")

            return True

        except Exception as e:
            print(f"❌ Failed to create admin profile: {e}")
            return False

    def verify_setup(self, uid: str) -> bool:
        """Verify the admin setup is complete"""
        try:
            print("🔍 Verifying admin setup...")

            # Get user from Firebase Auth
            user_record = firebase_auth.get_user(uid)
            print(f"✅ Firebase Auth user verified: {user_record.email}")

            # Get user profile from Firestore
            profile = self.firebase_auth.get_user_profile(uid)
            if not profile:
                print("❌ Admin profile not found in Firestore")
                return False

            print(f"✅ Firestore profile verified: {profile.get('role')}")

            # Verify permissions
            permissions = profile.get("permissions", [])
            if "admin:all" not in permissions:
                print("❌ Admin permissions not properly set")
                return False

            print(f"✅ Admin permissions verified: {len(permissions)} permissions")

            # Test token verification
            custom_token = self.firebase_manager.create_custom_token(uid)
            if not custom_token:
                print("❌ Custom token creation failed")
                return False

            print("✅ Custom token creation verified")

            return True

        except Exception as e:
            print(f"❌ Setup verification failed: {e}")
            return False

    def run_setup(self) -> bool:
        """Run complete admin user setup"""
        print("🚀 LANCELOTT Admin User Setup")
        print("=" * 50)
        print(f"📧 Admin Email: {self.admin_email}")
        print(f"👤 Display Name: {self.admin_display_name}")
        print(f"🔥 Firebase Project: {os.getenv('FIREBASE_PROJECT_ID')}")
        print()

        # Step 1: Initialize Firebase
        if not self.initialize_firebase():
            return False

        # Step 2: Create admin user
        admin_uid = self.create_admin_user()
        if not admin_uid:
            return False

        # Step 3: Create admin profile
        if not self.create_admin_profile(admin_uid):
            return False

        # Step 4: Verify setup
        if not self.verify_setup(admin_uid):
            print("⚠️ Warning: Setup verification failed")

        print()
        print("🎉 Admin User Setup Completed Successfully!")
        print()
        print("📋 Setup Summary:")
        print(f"   📧 Email: {self.admin_email}")
        print(f"   🆔 UID: {admin_uid}")
        print(f"   👤 Display Name: {self.admin_display_name}")
        print(f"   👑 Role: Admin")
        print("   🔑 Permissions: Full admin access")
        print()
        print("🔐 Authentication Details:")
        print("   • Firebase Authentication: ✅ Configured")
        print("   • Firestore Profile: ✅ Created")
        print("   • Admin Permissions: ✅ Granted")
        print("   • Custom Tokens: ✅ Enabled")
        print()
        print("🌐 Access Information:")
        print(f"   • Dashboard: https://{os.getenv('FIREBASE_PROJECT_ID')}.web.app")
        print(f"   • API Docs: https://{os.getenv('FIREBASE_PROJECT_ID')}.web.app/docs")
        print(
            f"   • Firebase Console: https://console.firebase.google.com/project/{os.getenv('FIREBASE_PROJECT_ID')}"
        )
        print()
        print("⚠️ IMPORTANT SECURITY NOTES:")
        print("   1. Set a strong password in Firebase Console")
        print("   2. Enable 2FA for additional security")
        print("   3. The password 'Ggg123456789ggG!' should be set manually")
        print("   4. Consider changing default permissions as needed")
        print()
        print("🔧 Next Steps:")
        print("   1. Go to Firebase Console > Authentication > Users")
        print(f"   2. Find user: {self.admin_email}")
        print("   3. Set password: Ggg123456789ggG!")
        print("   4. Enable the user account")
        print("   5. Test login at the dashboard")
        print()

        return True


def print_manual_instructions():
    """Print manual setup instructions"""
    print()
    print("🔧 MANUAL FIREBASE CONSOLE SETUP REQUIRED:")
    print("=" * 60)
    print()
    print("1. 🌐 Open Firebase Console:")
    print("   https://console.firebase.google.com")
    print()
    print(f"2. 📁 Select Project: {os.getenv('FIREBASE_PROJECT_ID')}")
    print()
    print("3. 🔐 Go to Authentication > Users")
    print()
    print("4. 👤 Find or Add User:")
    print("   📧 Email: knightprojeks@gmail.com")
    print("   🔑 Password: Ggg123456789ggG!")
    print("   ✅ Email verified: Yes")
    print()
    print("5. 💾 Save the user account")
    print()
    print("6. 🧪 Test Login:")
    print("   • Use the dashboard or API endpoints")
    print("   • Verify admin permissions work")
    print()
    print("🔒 SECURITY RECOMMENDATIONS:")
    print("   • Use 2FA when available")
    print("   • Regular password rotation")
    print("   • Monitor admin access logs")
    print("   • Restrict admin access to trusted IPs")
    print()


async def main():
    """Main async function"""
    try:
        setup = AdminUserSetup()
        success = setup.run_setup()

        if success:
            print_manual_instructions()
            print(
                "✅ Setup completed! Please complete manual steps in Firebase Console."
            )
            return 0
        else:
            print("❌ Setup failed! Check error messages above.")
            return 1

    except KeyboardInterrupt:
        print("\n⚠️ Setup interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    # Run the async main function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
