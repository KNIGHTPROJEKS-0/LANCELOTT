#!/usr/bin/env python3
"""
Deployment Verification Script
Verifies that all backend integration components are properly deployed
"""

import os
import sys
from pathlib import Path
from typing import Dict, List


def check_file_exists(file_path: str) -> bool:
    """Check if a file exists"""
    return Path(file_path).exists()


def verify_backend_integration() -> Dict[str, bool]:
    """
    Verify all backend integration files are present

    Returns:
        Dictionary with verification results
    """
    required_files = {
        "Firebase Configuration": "core/firebase_config.py",
        "TARS API Routes": "api/routes/tars_api.py",
        "Main Application": "app.py",
        "Environment Config": ".env",
        "Git Ignore": ".gitignore",
        "GitHub Actions": ".github/workflows/ci-cd.yml",
        "Firebase Setup Guide": "docs/setup/FIREBASE_SERVICE_ACCOUNT_SETUP.md",
        "TARS API Documentation": "docs/integration/TARS_API_INTEGRATION_COMPLETE.md",
        "Test Suite": "test_tars_api_endpoints.py",
        "Requirements": "requirements.txt",
    }

    results = {}
    for name, file_path in required_files.items():
        results[name] = check_file_exists(file_path)

    return results


def verify_git_configuration() -> Dict[str, str]:
    """
    Verify Git configuration

    Returns:
        Dictionary with Git configuration status
    """
    try:
        import subprocess

        # Check Git user configuration
        email_result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )

        name_result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )

        remote_result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )

        return {
            "email": (
                email_result.stdout.strip()
                if email_result.returncode == 0
                else "Not configured"
            ),
            "name": (
                name_result.stdout.strip()
                if name_result.returncode == 0
                else "Not configured"
            ),
            "remote": (
                remote_result.stdout.strip()
                if remote_result.returncode == 0
                else "Not configured"
            ),
        }
    except Exception as e:
        return {"error": str(e)}


def print_results(file_results: Dict[str, bool], git_config: Dict[str, str]):
    """Print verification results"""
    print("🔍 Backend Integration Deployment Verification")
    print("=" * 50)

    print("\n📁 Required Files:")
    all_present = True
    for name, exists in file_results.items():
        status = "✅" if exists else "❌"
        print(f"  {status} {name}")
        if not exists:
            all_present = False

    print(
        f"\n📊 Files Status: {'✅ All present' if all_present else '❌ Missing files'}"
    )

    print("\n🔧 Git Configuration:")
    for key, value in git_config.items():
        if key == "error":
            print(f"  ❌ Error: {value}")
        else:
            print(f"  📧 {key.title()}: {value}")

    # Check specific configurations
    expected_email = "knightprojeks@gmail.com"
    expected_username = "KNIGHTPROJEKS-0"
    expected_remote = "https://github.com/KNIGHTPROJEKS-0/LANCELOTT.git"

    config_correct = (
        git_config.get("email") == expected_email
        and git_config.get("name") == expected_username
        and git_config.get("remote") == expected_remote
    )

    print(
        f"\n🎯 Git Config Status: {'✅ Correct' if config_correct else '❌ Needs correction'}"
    )

    if not config_correct:
        print("\n🔧 Expected Configuration:")
        print(f"  📧 Email: {expected_email}")
        print(f"  👤 Name: {expected_username}")
        print(f"  🔗 Remote: {expected_remote}")

    print("\n🚀 Deployment Status:")
    if all_present and config_correct:
        print("  ✅ Ready for deployment - All components verified")
    else:
        print("  ⚠️  Issues found - Check above for details")

    return all_present and config_correct


def main():
    """Main verification function"""
    print("Starting deployment verification...\n")

    # Verify backend integration files
    file_results = verify_backend_integration()

    # Verify Git configuration
    git_config = verify_git_configuration()

    # Print results
    success = print_results(file_results, git_config)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
