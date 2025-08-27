#!/usr/bin/env python3
"""
N8N Move Verification Script
Verifies that n8n has been successfully moved to the workflows directory
"""

import json
import os
import sys
from pathlib import Path


def check_n8n_move():
    """Verify n8n move completion"""
    print("🔍 Verifying N8N Move to Workflows Directory")
    print("=" * 50)

    results = {
        "source_removed": False,
        "destination_exists": False,
        "workflows_found": False,
        "startup_script": False,
        "config_valid": False,
    }

    # Check if original n8n directory is removed
    n8n_path = Path("n8n")
    if not n8n_path.exists():
        print("✅ Original n8n directory successfully removed")
        results["source_removed"] = True
    else:
        print("⚠️ Original n8n directory still exists")

    # Check if workflows directory exists and has n8n content
    workflows_path = Path("workflows")
    if workflows_path.exists():
        print("✅ Workflows directory exists")
        results["destination_exists"] = True

        # Check for GitHub workflows
        github_workflows = workflows_path / ".github" / "workflows"
        if github_workflows.exists():
            workflow_files = list(github_workflows.glob("*.yml"))
            print(f"✅ Found {len(workflow_files)} GitHub workflow files")
            results["workflows_found"] = True
        else:
            print("❌ GitHub workflows not found")
    else:
        print("❌ Workflows directory not found")

    # Check for n8n startup script
    startup_script = workflows_path / "start_n8n.sh"
    if startup_script.exists():
        print("✅ N8N startup script found")
        results["startup_script"] = True
    else:
        print("❌ N8N startup script not found")

    # Check configuration
    config_path = Path("config/lancelott.yaml")
    if config_path.exists():
        try:
            import yaml

            with open(config_path) as f:
                config = yaml.safe_load(f)

            n8n_url = config.get("integrations", {}).get("n8n_url")
            if n8n_url == "http://localhost:5678":
                print("✅ N8N configuration is valid")
                results["config_valid"] = True
            else:
                print(f"⚠️ N8N URL configured as: {n8n_url}")
        except Exception as e:
            print(f"❌ Configuration check failed: {e}")
    else:
        print("❌ Configuration file not found")

    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION RESULTS")
    print("=" * 50)

    total_checks = len(results)
    passed_checks = sum(results.values())

    for check, status in results.items():
        icon = "✅" if status else "❌"
        print(
            f"{icon} {check.replace('_', ' ').title()}: {'PASS' if status else 'FAIL'}"
        )

    print(f"\n📈 Overall Status: {passed_checks}/{total_checks} checks passed")

    if passed_checks == total_checks:
        print("🎉 N8N move completed successfully!")
        print("\n🚀 Next Steps:")
        print("  • Start N8N: cd workflows && ./start_n8n.sh")
        print("  • Access N8N: http://localhost:5678")
        print("  • Check LANCELOTT integration: python app.py")
        return True
    else:
        print("💥 Some verification checks failed!")
        return False


def main():
    """Main verification function"""
    print("🛡️ CERBERUS-FANGS LANCELOTT - N8N Move Verification")
    print()

    # Change to project root if needed
    if not Path("config/lancelott.yaml").exists():
        print("❌ Please run this script from the LANCELOTT project root directory")
        sys.exit(1)

    success = check_n8n_move()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
