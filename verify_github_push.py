#!/usr/bin/env python3
"""
Repository Push Verification Script
Verifies that the backend integration changes were successfully pushed to GitHub
"""

import sys
from typing import Dict, List, Optional

import requests


def check_github_repository(owner: str, repo: str) -> Dict[str, any]:
    """
    Check if GitHub repository exists and get basic info

    Args:
        owner: Repository owner
        repo: Repository name

    Returns:
        Dictionary with repository information
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return {"exists": True, "data": response.json()}
        elif response.status_code == 404:
            return {"exists": False, "error": "Repository not found"}
        else:
            return {
                "exists": False,
                "error": f"HTTP {response.status_code}: {response.text}",
            }
    except Exception as e:
        return {"exists": False, "error": f"Request failed: {str(e)}"}


def check_file_in_repo(owner: str, repo: str, file_path: str) -> Dict[str, any]:
    """
    Check if a specific file exists in the GitHub repository

    Args:
        owner: Repository owner
        repo: Repository name
        file_path: Path to the file to check

    Returns:
        Dictionary with file existence status
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return {"exists": True, "size": response.json().get("size", 0)}
        elif response.status_code == 404:
            return {"exists": False, "error": "File not found"}
        else:
            return {"exists": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"exists": False, "error": f"Request failed: {str(e)}"}


def verify_backend_integration_upload() -> bool:
    """
    Verify that backend integration files were uploaded to GitHub

    Returns:
        True if verification successful, False otherwise
    """
    owner = "KNIGHTPROJEKS-0"
    repo = "LANCELOTT"

    print("🔍 Verifying Repository Push to GitHub")
    print("=" * 50)

    # Check if repository exists
    repo_status = check_github_repository(owner, repo)
    if not repo_status["exists"]:
        print(
            f"❌ Repository not accessible: {repo_status.get('error', 'Unknown error')}"
        )
        return False

    print(f"✅ Repository exists: https://github.com/{owner}/{repo}")

    # Files to check
    critical_files = [
        "core/firebase_config.py",
        "api/routes/tars_api.py",
        "app.py",
        ".gitignore",
        ".github/workflows/ci-cd.yml",
        "test_tars_api_endpoints.py",
        "verify_deployment.py",
        "requirements.txt",
    ]

    print("\n📁 Checking Critical Backend Integration Files:")

    all_files_present = True
    for file_path in critical_files:
        file_status = check_file_in_repo(owner, repo, file_path)

        if file_status["exists"]:
            size = file_status.get("size", 0)
            print(f"  ✅ {file_path} (size: {size} bytes)")
        else:
            print(f"  ❌ {file_path} - {file_status.get('error', 'Not found')}")
            all_files_present = False

    print(
        f"\n📊 Upload Status: {'✅ SUCCESS' if all_files_present else '❌ INCOMPLETE'}"
    )

    if all_files_present:
        print("\n🎉 Backend Integration Successfully Uploaded!")
        print(f"🔗 Repository: https://github.com/{owner}/{repo}")
        print("✅ All critical files are accessible on GitHub")
    else:
        print("\n⚠️  Some files are missing from the repository")
        print("🔄 You may need to push again or check your Git configuration")

    return all_files_present


def main():
    """Main verification function"""
    try:
        success = verify_backend_integration_upload()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
