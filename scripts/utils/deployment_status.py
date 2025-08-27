#!/usr/bin/env python3
"""
LANCELOTT Deployment Status Dashboard
Real-time monitoring of Firebase and GitHub deployment status

This script provides a comprehensive overview of the LANCELOTT deployment
status across all services and platforms.
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import aiohttp
import requests


class DeploymentStatusMonitor:
    """
    Monitors deployment status across Firebase, GitHub, and local services
    """

    def __init__(self):
        self.project_id = os.getenv("FIREBASE_PROJECT_ID", "lancelott-z9dko")
        self.github_repo = "ORDEROFCODE/LANCELOTT"
        self.local_port = int(os.getenv("APP_PORT", "7777"))

        self.services = {
            "firebase_hosting": f"https://{self.project_id}.web.app",
            "firebase_functions": f"https://us-central1-{self.project_id}.cloudfunctions.net",
            "api_health": f"https://{self.project_id}.web.app/api/health",
            "api_docs": f"https://{self.project_id}.web.app/docs",
            "local_service": f"http://localhost:{self.local_port}",
            "github_repo": f"https://github.com/{self.github_repo}",
            "firebase_console": f"https://console.firebase.google.com/project/{self.project_id}",
        }

    async def check_url_status(
        self, session: aiohttp.ClientSession, name: str, url: str
    ) -> Dict:
        """Check the status of a URL"""
        try:
            async with session.get(url, timeout=10) as response:
                return {
                    "name": name,
                    "url": url,
                    "status": response.status,
                    "online": response.status == 200,
                    "response_time": None,
                    "error": None,
                }
        except asyncio.TimeoutError:
            return {
                "name": name,
                "url": url,
                "status": "timeout",
                "online": False,
                "response_time": None,
                "error": "Request timeout",
            }
        except Exception as e:
            return {
                "name": name,
                "url": url,
                "status": "error",
                "online": False,
                "response_time": None,
                "error": str(e),
            }

    async def check_all_services(self) -> Dict[str, Dict]:
        """Check status of all services"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for name, url in self.services.items():
                tasks.append(self.check_url_status(session, name, url))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            status_dict = {}
            for result in results:
                if isinstance(result, dict):
                    status_dict[result["name"]] = result
                else:
                    # Handle exceptions
                    status_dict["unknown"] = {
                        "name": "unknown",
                        "url": "unknown",
                        "status": "error",
                        "online": False,
                        "response_time": None,
                        "error": str(result),
                    }

            return status_dict

    def check_firebase_cli(self) -> Dict:
        """Check Firebase CLI status"""
        try:
            result = subprocess.run(
                ["firebase", "--version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                return {"installed": True, "version": version, "error": None}
            else:
                return {
                    "installed": False,
                    "version": None,
                    "error": result.stderr.strip(),
                }
        except subprocess.TimeoutExpired:
            return {"installed": False, "version": None, "error": "Command timeout"}
        except FileNotFoundError:
            return {
                "installed": False,
                "version": None,
                "error": "Firebase CLI not found",
            }
        except Exception as e:
            return {"installed": False, "version": None, "error": str(e)}

    def check_git_status(self) -> Dict:
        """Check Git repository status"""
        try:
            # Check if we're in a git repository
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode != 0:
                return {
                    "is_repo": False,
                    "branch": None,
                    "remote": None,
                    "status": None,
                    "error": "Not a git repository",
                }

            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            current_branch = (
                branch_result.stdout.strip()
                if branch_result.returncode == 0
                else "unknown"
            )

            # Get remote URL
            remote_result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            remote_url = (
                remote_result.stdout.strip()
                if remote_result.returncode == 0
                else "none"
            )

            # Get status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            has_changes = (
                len(status_result.stdout.strip()) > 0
                if status_result.returncode == 0
                else False
            )

            return {
                "is_repo": True,
                "branch": current_branch,
                "remote": remote_url,
                "has_changes": has_changes,
                "error": None,
            }

        except Exception as e:
            return {
                "is_repo": False,
                "branch": None,
                "remote": None,
                "has_changes": None,
                "error": str(e),
            }

    def check_local_environment(self) -> Dict:
        """Check local development environment"""
        env_status = {}

        # Check Python version
        try:
            python_version = sys.version.split()[0]
            env_status["python"] = {
                "version": python_version,
                "executable": sys.executable,
                "available": True,
            }
        except Exception as e:
            env_status["python"] = {
                "version": None,
                "executable": None,
                "available": False,
                "error": str(e),
            }

        # Check virtual environment
        venv_active = hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        )

        env_status["virtual_env"] = {
            "active": venv_active,
            "path": os.environ.get("VIRTUAL_ENV"),
        }

        # Check key files
        project_root = Path(".")
        key_files = {
            ".env": project_root / ".env",
            "requirements.txt": project_root / "requirements.txt",
            "firebase.json": project_root / "firebase.json",
            "app.py": project_root / "app.py",
        }

        env_status["files"] = {}
        for name, path in key_files.items():
            env_status["files"][name] = {"exists": path.exists(), "path": str(path)}

        return env_status

    def check_github_actions(self) -> Dict:
        """Check GitHub Actions workflow status"""
        try:
            # This would require GitHub CLI or API token
            # For now, just check if workflow files exist
            workflows_dir = Path(".github/workflows")

            if not workflows_dir.exists():
                return {
                    "configured": False,
                    "workflows": [],
                    "error": "No .github/workflows directory found",
                }

            workflow_files = list(workflows_dir.glob("*.yml")) + list(
                workflows_dir.glob("*.yaml")
            )

            return {
                "configured": len(workflow_files) > 0,
                "workflows": [f.name for f in workflow_files],
                "count": len(workflow_files),
                "error": None,
            }

        except Exception as e:
            return {"configured": False, "workflows": [], "count": 0, "error": str(e)}

    def generate_status_report(self) -> Dict:
        """Generate comprehensive status report"""
        print("🔄 Checking LANCELOTT deployment status...")

        # Async service checks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            service_status = loop.run_until_complete(self.check_all_services())
        finally:
            loop.close()

        # Sync checks
        firebase_cli = self.check_firebase_cli()
        git_status = self.check_git_status()
        local_env = self.check_local_environment()
        github_actions = self.check_github_actions()

        # Calculate overall health
        online_services = sum(1 for s in service_status.values() if s["online"])
        total_services = len(service_status)
        health_percentage = (
            (online_services / total_services) * 100 if total_services > 0 else 0
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "project_id": self.project_id,
            "github_repo": self.github_repo,
            "overall_health": {
                "percentage": health_percentage,
                "status": (
                    "healthy"
                    if health_percentage >= 80
                    else "degraded" if health_percentage >= 50 else "unhealthy"
                ),
                "online_services": online_services,
                "total_services": total_services,
            },
            "services": service_status,
            "firebase_cli": firebase_cli,
            "git_status": git_status,
            "local_environment": local_env,
            "github_actions": github_actions,
        }

    def print_status_report(self, report: Dict):
        """Print formatted status report"""
        print("\n" + "=" * 80)
        print("🛡️  LANCELOTT DEPLOYMENT STATUS DASHBOARD")
        print("=" * 80)
        print(f"📅 Generated: {report['timestamp']}")
        print(f"🔥 Firebase Project: {report['project_id']}")
        print(f"📱 GitHub Repository: {report['github_repo']}")
        print()

        # Overall health
        health = report["overall_health"]
        health_emoji = (
            "🟢"
            if health["status"] == "healthy"
            else "🟡" if health["status"] == "degraded" else "🔴"
        )
        print(
            f"{health_emoji} Overall Health: {health['percentage']:.1f}% ({health['status'].upper()})"
        )
        print(
            f"📊 Services Online: {health['online_services']}/{health['total_services']}"
        )
        print()

        # Service status
        print("🌐 SERVICE STATUS")
        print("-" * 40)
        for name, status in report["services"].items():
            emoji = "✅" if status["online"] else "❌"
            print(f"{emoji} {name.replace('_', ' ').title()}")
            print(f"   URL: {status['url']}")
            if not status["online"] and status["error"]:
                print(f"   Error: {status['error']}")
            print()

        # Firebase CLI
        print("🔥 FIREBASE CLI")
        print("-" * 40)
        firebase = report["firebase_cli"]
        if firebase["installed"]:
            print(f"✅ Firebase CLI: {firebase['version']}")
        else:
            print(f"❌ Firebase CLI: Not installed")
            if firebase["error"]:
                print(f"   Error: {firebase['error']}")
        print()

        # Git status
        print("📱 GIT REPOSITORY")
        print("-" * 40)
        git = report["git_status"]
        if git["is_repo"]:
            print(f"✅ Git Repository: Active")
            print(f"   Branch: {git['branch']}")
            print(f"   Remote: {git['remote']}")
            print(f"   Changes: {'Yes' if git['has_changes'] else 'No'}")
        else:
            print(f"❌ Git Repository: {git['error']}")
        print()

        # Local environment
        print("🐍 LOCAL ENVIRONMENT")
        print("-" * 40)
        env = report["local_environment"]

        # Python
        python = env["python"]
        if python["available"]:
            print(f"✅ Python: {python['version']}")
        else:
            print(f"❌ Python: Not available")

        # Virtual environment
        venv = env["virtual_env"]
        if venv["active"]:
            print(f"✅ Virtual Environment: Active")
            if venv["path"]:
                print(f"   Path: {venv['path']}")
        else:
            print(f"❌ Virtual Environment: Not active")

        # Files
        print("   Files:")
        for filename, file_info in env["files"].items():
            emoji = "✅" if file_info["exists"] else "❌"
            print(f"   {emoji} {filename}")
        print()

        # GitHub Actions
        print("🚀 GITHUB ACTIONS")
        print("-" * 40)
        actions = report["github_actions"]
        if actions["configured"]:
            print(f"✅ GitHub Actions: {actions['count']} workflows configured")
            for workflow in actions["workflows"]:
                print(f"   - {workflow}")
        else:
            print(f"❌ GitHub Actions: Not configured")
            if actions["error"]:
                print(f"   Error: {actions['error']}")
        print()

        # Quick links
        print("🔗 QUICK LINKS")
        print("-" * 40)
        print(f"🌐 Dashboard: https://{report['project_id']}.web.app")
        print(f"📚 API Docs: https://{report['project_id']}.web.app/docs")
        print(
            f"🔥 Firebase Console: https://console.firebase.google.com/project/{report['project_id']}"
        )
        print(f"📱 GitHub Repo: https://github.com/{report['github_repo']}")
        print()

        # Recommendations
        print("💡 RECOMMENDATIONS")
        print("-" * 40)

        if health["percentage"] < 100:
            print("• Some services are offline - check error messages above")

        if not firebase["installed"]:
            print("• Install Firebase CLI: npm install -g firebase-tools")

        if not git["is_repo"]:
            print("• Initialize Git repository and connect to GitHub")

        if git["has_changes"]:
            print("• Commit and push pending changes")

        if not env["virtual_env"]["active"]:
            print("• Activate virtual environment: source .venv/bin/activate")

        if not actions["configured"]:
            print("• Set up GitHub Actions for automated deployment")

        print("\n" + "=" * 80)


async def main():
    """Main function"""
    monitor = DeploymentStatusMonitor()

    # Handle command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--json":
            # Output JSON format
            report = monitor.generate_status_report()
            print(json.dumps(report, indent=2))
            return
        elif command == "--continuous":
            # Continuous monitoring
            print("🔄 Starting continuous monitoring (Ctrl+C to stop)...")
            try:
                while True:
                    report = monitor.generate_status_report()
                    monitor.print_status_report(report)
                    print("⏱️  Refreshing in 30 seconds...")
                    time.sleep(30)
                    print("\033[2J\033[H")  # Clear screen
            except KeyboardInterrupt:
                print("\n👋 Monitoring stopped")
                return
        elif command == "--help":
            print("🛡️ LANCELOTT Deployment Status Monitor")
            print("")
            print("Usage: python deployment_status.py [option]")
            print("")
            print("Options:")
            print("  --json        Output status in JSON format")
            print("  --continuous  Continuous monitoring mode")
            print("  --help        Show this help message")
            print("")
            return

    # Default: single status check
    report = monitor.generate_status_report()
    monitor.print_status_report(report)

    # Exit code based on health
    health_percentage = report["overall_health"]["percentage"]
    if health_percentage >= 80:
        sys.exit(0)  # Healthy
    elif health_percentage >= 50:
        sys.exit(1)  # Degraded
    else:
        sys.exit(2)  # Unhealthy


if __name__ == "__main__":
    asyncio.run(main())
