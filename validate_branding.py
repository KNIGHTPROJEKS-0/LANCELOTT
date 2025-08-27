#!/usr/bin/env python3
"""
LANCELOTT Branding and Entry Point Validation Report
Comprehensive verification of branding consistency and command functionality
Generated: 2025-08-27
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def validate_entry_points():
    """Validate entry point commands"""
    project_root = Path(__file__).parent

    entry_points = {
        "lance": {
            "file": project_root / "lance",
            "purpose": "Agent-TARS CLI Entry Point",
            "target": "Agent-TARS CLI",
            "branding": "LANCELOTT Framework",
        },
        "lancelott": {
            "file": project_root / "lancelott",
            "purpose": "UI-TARS Desktop Entry Point",
            "target": "UI-TARS Desktop",
            "branding": "LANCELOTT Framework",
        },
        "agent-tars": {
            "file": project_root / "agent-tars",
            "purpose": "Alternative Agent-TARS Entry Point",
            "target": "Agent-TARS CLI",
            "branding": "LANCELOTT Framework",
        },
        "ui-tars": {
            "file": project_root / "ui-tars",
            "purpose": "Alternative UI-TARS Entry Point",
            "target": "UI-TARS Desktop",
            "branding": "LANCELOTT Framework",
        },
    }

    validation_results = {}

    for cmd_name, cmd_info in entry_points.items():
        results = {
            "exists": cmd_info["file"].exists(),
            "executable": False,
            "proper_branding": False,
            "correct_shebang": False,
            "targets_correct_script": False,
        }

        if results["exists"]:
            # Check if executable
            results["executable"] = os.access(cmd_info["file"], os.X_OK)

            # Read file content for validation
            try:
                with open(cmd_info["file"], "r") as f:
                    content = f.read()

                # Check branding
                results["proper_branding"] = "LANCELOTT Framework" in content

                # Check shebang
                results["correct_shebang"] = content.startswith("#!/bin/bash")

                # Check script targeting
                results["targets_correct_script"] = "launch_" in content

            except Exception as e:
                results["error"] = str(e)

        validation_results[cmd_name] = results

    return validation_results


def validate_branding_consistency():
    """Validate LANCELOTT branding consistency across key files"""
    project_root = Path(__file__).parent

    key_files = {
        "app.py": ["LANCELOTT", "title>LANCELOTT</title>"],
        "main.py": ["Starting LANCELOTT API", "Shutting down LANCELOTT API"],
        "lancelott.py": ["🛡️  LANCELOTT"],
        "core/config.py": ['APP_NAME: str = "LANCELOTT"'],
        "config/lancelott_config.py": ["LANCELOTT - Unified Configuration"],
        "api/routes/ui_tars_router.py": ["LANCELOTT Framework Integration"],
        "scripts/launch_agent_tars.sh": ["LANCELOTT Framework"],
        "scripts/launch_ui_tars.sh": ["LANCELOTT Framework"],
        "docker-compose.yml": ["lancelott:", "container_name: lancelott"],
        "firebase.json": ["lancelott-z9dko"],
    }

    branding_results = {}

    for file_path, required_terms in key_files.items():
        file_full_path = project_root / file_path
        results = {
            "exists": file_full_path.exists(),
            "branding_found": [],
            "branding_missing": [],
            "all_branding_correct": False,
        }

        if results["exists"]:
            try:
                with open(file_full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                for term in required_terms:
                    if term in content:
                        results["branding_found"].append(term)
                    else:
                        results["branding_missing"].append(term)

                results["all_branding_correct"] = len(results["branding_missing"]) == 0

            except Exception as e:
                results["error"] = str(e)

        branding_results[file_path] = results

    return branding_results


def check_cerberus_fangs_references():
    """Check for any remaining CERBERUS-FANGS references"""
    project_root = Path(__file__).parent

    # Files that should NOT contain CERBERUS-FANGS (critical files only)
    critical_files = [
        "app.py",
        "main.py",
        "lancelott.py",
        "start.py",
        "core/config.py",
        "config/lancelott_config.py",
        "lance",
        "lancelott",
        "agent-tars",
        "ui-tars",
    ]

    remaining_references = {}

    for file_path in critical_files:
        file_full_path = project_root / file_path

        if file_full_path.exists():
            try:
                with open(file_full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                if "CERBERUS-FANGS" in content:
                    # Find line numbers with CERBERUS-FANGS
                    lines = content.split("\n")
                    found_lines = []
                    for i, line in enumerate(lines, 1):
                        if "CERBERUS-FANGS" in line:
                            found_lines.append(f"Line {i}: {line.strip()}")

                    remaining_references[file_path] = found_lines

            except Exception as e:
                remaining_references[file_path] = [f"Error reading file: {e}"]

    return remaining_references


def generate_validation_report():
    """Generate comprehensive validation report"""
    print("🛡️ LANCELOTT BRANDING & ENTRY POINT VALIDATION REPORT")
    print("=" * 65)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Validator: LANCELOTT Framework Validation System")
    print()

    # Validate Entry Points
    print("🚀 ENTRY POINT COMMANDS VALIDATION")
    print("-" * 40)
    entry_results = validate_entry_points()

    all_entry_points_valid = True
    for cmd_name, results in entry_results.items():
        status_icon = "✅" if all(results.values()) else "❌"
        print(f"{status_icon} {cmd_name}")
        print(f"    Exists: {'✅' if results['exists'] else '❌'}")
        print(f"    Executable: {'✅' if results['executable'] else '❌'}")
        print(f"    Proper Branding: {'✅' if results['proper_branding'] else '❌'}")
        print(f"    Correct Shebang: {'✅' if results['correct_shebang'] else '❌'}")
        print(
            f"    Targets Script: {'✅' if results['targets_correct_script'] else '❌'}"
        )

        if not all(results.values()):
            all_entry_points_valid = False
        print()

    # Validate Branding Consistency
    print("🎯 BRANDING CONSISTENCY VALIDATION")
    print("-" * 40)
    branding_results = validate_branding_consistency()

    all_branding_valid = True
    for file_path, results in branding_results.items():
        if results["exists"]:
            status_icon = "✅" if results["all_branding_correct"] else "❌"
            print(f"{status_icon} {file_path}")

            if results["branding_found"]:
                print(f"    ✅ Found: {', '.join(results['branding_found'])}")

            if results["branding_missing"]:
                print(f"    ❌ Missing: {', '.join(results['branding_missing'])}")
                all_branding_valid = False
        else:
            print(f"⚠️ {file_path} - File not found")
        print()

    # Check for remaining CERBERUS-FANGS references
    print("🔍 CERBERUS-FANGS REFERENCES CHECK")
    print("-" * 40)
    remaining_refs = check_cerberus_fangs_references()

    if remaining_refs:
        print("❌ Found remaining CERBERUS-FANGS references in critical files:")
        for file_path, lines in remaining_refs.items():
            print(f"  📄 {file_path}:")
            for line in lines:
                print(f"    {line}")
        print()
    else:
        print("✅ No CERBERUS-FANGS references found in critical files")
        print()

    # Overall Status
    print("📊 OVERALL VALIDATION STATUS")
    print("-" * 40)

    total_checks = 3
    passed_checks = 0

    if all_entry_points_valid:
        passed_checks += 1
        print("✅ Entry Point Commands: PASS")
    else:
        print("❌ Entry Point Commands: FAIL")

    if all_branding_valid:
        passed_checks += 1
        print("✅ Branding Consistency: PASS")
    else:
        print("❌ Branding Consistency: FAIL")

    if not remaining_refs:
        passed_checks += 1
        print("✅ Legacy Reference Cleanup: PASS")
    else:
        print("❌ Legacy Reference Cleanup: FAIL")

    print()
    print(f"📈 Validation Score: {passed_checks}/{total_checks} checks passed")

    if passed_checks == total_checks:
        print("🎉 LANCELOTT FRAMEWORK VALIDATION: COMPLETE ✅")
        print()
        print("🚀 Ready to use:")
        print("  ./lance        # Launch Agent-TARS CLI")
        print("  ./lancelott    # Launch UI-TARS Desktop")
        print("  ./agent-tars   # Alternative Agent-TARS entry")
        print("  ./ui-tars      # Alternative UI-TARS entry")
    else:
        print("⚠️ LANCELOTT FRAMEWORK VALIDATION: ISSUES FOUND")
        print("Please address the issues above before proceeding.")

    print()
    print("🛡️ LANCELOTT - Your Guardian in the Digital Realm")


if __name__ == "__main__":
    generate_validation_report()
