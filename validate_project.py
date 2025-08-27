#!/usr/bin/env python3
"""
LANCELOTT Project Validation Script
Comprehensive validation of project structure, dependencies, and configuration
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class LANCELOTTProjectValidator:
    """Comprehensive project validation system"""

    def __init__(self):
        self.project_root = Path(".")
        self.validation_results = {
            "structure": {"passed": 0, "failed": 0, "issues": []},
            "configuration": {"passed": 0, "failed": 0, "issues": []},
            "dependencies": {"passed": 0, "failed": 0, "issues": []},
            "documentation": {"passed": 0, "failed": 0, "issues": []},
            "tests": {"passed": 0, "failed": 0, "issues": []},
            "tools": {"passed": 0, "failed": 0, "issues": []},
        }

    def print_header(self):
        """Print validation header"""
        print("🛡️" * 50)
        print("🛡️ LANCELOTT PROJECT VALIDATION SUITE")
        print("🛡️" * 50)
        print()

    def validate_project_structure(self) -> bool:
        """Validate project directory structure"""
        print("📂 Validating Project Structure...")

        required_dirs = [
            "api",
            "config",
            "core",
            "tools",
            "integrations",
            "workflows",
            "tests",
            "docs",
            "build",
            "status",
        ]

        required_files = [
            "app.py",
            "requirements.txt",
            "Dockerfile",
            "docker-compose.yml",
            "README.md",
            "Makefile",
            ".env.example",
            "project.json",
        ]

        # Check required directories
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                print(f"  ✅ Directory: {dir_name}")
                self.validation_results["structure"]["passed"] += 1
            else:
                print(f"  ❌ Missing directory: {dir_name}")
                self.validation_results["structure"]["failed"] += 1
                self.validation_results["structure"]["issues"].append(
                    f"Missing directory: {dir_name}"
                )

        # Check required files
        for file_name in required_files:
            file_path = self.project_root / file_name
            if file_path.exists() and file_path.is_file():
                print(f"  ✅ File: {file_name}")
                self.validation_results["structure"]["passed"] += 1
            else:
                print(f"  ❌ Missing file: {file_name}")
                self.validation_results["structure"]["failed"] += 1
                self.validation_results["structure"]["issues"].append(
                    f"Missing file: {file_name}"
                )

        return self.validation_results["structure"]["failed"] == 0

    def validate_configuration(self) -> bool:
        """Validate configuration files"""
        print("\n⚙️ Validating Configuration Files...")

        config_files = [
            ("config/lancelott.yaml", "YAML"),
            ("project.json", "JSON"),
            ("docker-compose.yml", "YAML"),
            (".env.example", "ENV"),
        ]

        for file_path, file_type in config_files:
            full_path = self.project_root / file_path

            if not full_path.exists():
                print(f"  ❌ Missing config file: {file_path}")
                self.validation_results["configuration"]["failed"] += 1
                continue

            try:
                if file_type == "YAML":
                    with open(full_path) as f:
                        yaml.safe_load(f)
                elif file_type == "JSON":
                    with open(full_path) as f:
                        json.load(f)

                print(f"  ✅ Valid {file_type}: {file_path}")
                self.validation_results["configuration"]["passed"] += 1

            except Exception as e:
                print(f"  ❌ Invalid {file_type}: {file_path} - {e}")
                self.validation_results["configuration"]["failed"] += 1
                self.validation_results["configuration"]["issues"].append(
                    f"Invalid {file_type}: {file_path}"
                )

        return self.validation_results["configuration"]["failed"] == 0

    def validate_dependencies(self) -> bool:
        """Validate Python dependencies"""
        print("\n📦 Validating Dependencies...")

        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            print("  ❌ Missing requirements.txt")
            self.validation_results["dependencies"]["failed"] += 1
            return False

        try:
            with open(requirements_file) as f:
                requirements = f.read()

            # Check for essential packages
            essential_packages = [
                "fastapi",
                "uvicorn",
                "pydantic",
                "python-dotenv",
                "requests",
                "aiofiles",
                "rich",
                "langchain",
            ]

            for package in essential_packages:
                if package in requirements:
                    print(f"  ✅ Package: {package}")
                    self.validation_results["dependencies"]["passed"] += 1
                else:
                    print(f"  ❌ Missing package: {package}")
                    self.validation_results["dependencies"]["failed"] += 1
                    self.validation_results["dependencies"]["issues"].append(
                        f"Missing package: {package}"
                    )

            return self.validation_results["dependencies"]["failed"] == 0

        except Exception as e:
            print(f"  ❌ Error reading requirements.txt: {e}")
            self.validation_results["dependencies"]["failed"] += 1
            return False

    def validate_documentation(self) -> bool:
        """Validate documentation structure"""
        print("\n📚 Validating Documentation...")

        doc_files = [
            "README.md",
            "PROJECT_STATUS.md",
            "docs/INDEX.md",
            "docs/CONFIGURATION_GUIDE.md",
            "tests/TEST_GUIDE.md",
        ]

        for doc_file in doc_files:
            doc_path = self.project_root / doc_file
            if doc_path.exists() and doc_path.stat().st_size > 0:
                print(f"  ✅ Documentation: {doc_file}")
                self.validation_results["documentation"]["passed"] += 1
            else:
                print(f"  ❌ Missing/empty documentation: {doc_file}")
                self.validation_results["documentation"]["failed"] += 1
                self.validation_results["documentation"]["issues"].append(
                    f"Missing documentation: {doc_file}"
                )

        return self.validation_results["documentation"]["failed"] == 0

    def validate_tests(self) -> bool:
        """Validate test structure"""
        print("\n🧪 Validating Test Structure...")

        test_dirs = [
            "tests/framework",
            "tests/tools",
            "tests/integration",
            "tests/api",
            "tests/unit",
        ]
        test_files = [
            "tests/run_all_tests.py",
            "tests/conftest.py",
            "tests/TEST_GUIDE.md",
        ]

        # Check test directories
        for test_dir in test_dirs:
            dir_path = self.project_root / test_dir
            if dir_path.exists():
                print(f"  ✅ Test directory: {test_dir}")
                self.validation_results["tests"]["passed"] += 1
            else:
                print(f"  ❌ Missing test directory: {test_dir}")
                self.validation_results["tests"]["failed"] += 1
                self.validation_results["tests"]["issues"].append(
                    f"Missing test directory: {test_dir}"
                )

        # Check test files
        for test_file in test_files:
            file_path = self.project_root / test_file
            if file_path.exists():
                print(f"  ✅ Test file: {test_file}")
                self.validation_results["tests"]["passed"] += 1
            else:
                print(f"  ❌ Missing test file: {test_file}")
                self.validation_results["tests"]["failed"] += 1
                self.validation_results["tests"]["issues"].append(
                    f"Missing test file: {test_file}"
                )

        return self.validation_results["tests"]["failed"] == 0

    def validate_tools_integration(self) -> bool:
        """Validate security tools integration"""
        print("\n🛠️ Validating Tools Integration...")

        # Check tools directory
        tools_dir = self.project_root / "tools"
        if not tools_dir.exists():
            print("  ❌ Missing tools directory")
            self.validation_results["tools"]["failed"] += 1
            return False

        # Check for key tools
        key_tools = ["crush", "Argus", "Kraken", "nmap", "feroxbuster"]

        for tool in key_tools:
            tool_path = tools_dir / tool
            if tool_path.exists():
                print(f"  ✅ Tool: {tool}")
                self.validation_results["tools"]["passed"] += 1
            else:
                print(f"  ⚠️ Missing tool: {tool}")
                self.validation_results["tools"]["failed"] += 1
                self.validation_results["tools"]["issues"].append(
                    f"Missing tool: {tool}"
                )

        # Check integrations
        integrations_dir = self.project_root / "integrations"
        if integrations_dir.exists():
            print(f"  ✅ Integrations directory exists")
            self.validation_results["tools"]["passed"] += 1
        else:
            print(f"  ❌ Missing integrations directory")
            self.validation_results["tools"]["failed"] += 1

        return self.validation_results["tools"]["failed"] == 0

    def validate_project_manifest(self) -> bool:
        """Validate project manifest (project.json)"""
        print("\n📋 Validating Project Manifest...")

        manifest_path = self.project_root / "project.json"
        if not manifest_path.exists():
            print("  ❌ Missing project.json")
            return False

        try:
            with open(manifest_path) as f:
                manifest = json.load(f)

            required_fields = [
                "name",
                "version",
                "description",
                "architecture",
                "components",
            ]

            for field in required_fields:
                if field in manifest:
                    print(f"  ✅ Manifest field: {field}")
                    self.validation_results["configuration"]["passed"] += 1
                else:
                    print(f"  ❌ Missing manifest field: {field}")
                    self.validation_results["configuration"]["failed"] += 1

            return True

        except Exception as e:
            print(f"  ❌ Error reading project manifest: {e}")
            return False

    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)

        total_passed = sum(cat["passed"] for cat in self.validation_results.values())
        total_failed = sum(cat["failed"] for cat in self.validation_results.values())
        total_tests = total_passed + total_failed

        for category, results in self.validation_results.items():
            status = "✅" if results["failed"] == 0 else "❌"
            print(
                f"{status} {category.upper()}: {results['passed']} passed, {results['failed']} failed"
            )

        print(f"\n📈 OVERALL: {total_passed}/{total_tests} checks passed")

        if total_failed == 0:
            print("\n🎉 PROJECT VALIDATION SUCCESSFUL!")
            print("✅ All validation checks passed")
            print("🚀 LANCELOTT project is properly scaffolded and ready for use!")
        else:
            print(f"\n💥 PROJECT VALIDATION FAILED!")
            print(f"❌ {total_failed} validation checks failed")
            print("\n🔧 Issues to fix:")
            for category, results in self.validation_results.items():
                for issue in results["issues"]:
                    print(f"  • {issue}")

        return total_failed == 0

    def run_validation(self) -> bool:
        """Run complete project validation"""
        self.print_header()

        # Run all validation checks
        structure_valid = self.validate_project_structure()
        config_valid = self.validate_configuration()
        deps_valid = self.validate_dependencies()
        docs_valid = self.validate_documentation()
        tests_valid = self.validate_tests()
        tools_valid = self.validate_tools_integration()
        manifest_valid = self.validate_project_manifest()

        # Print summary
        success = self.print_summary()

        return success


def main():
    """Main validation function"""
    validator = LANCELOTTProjectValidator()
    success = validator.run_validation()

    if success:
        print("\n🎯 Next Steps:")
        print("  1. Run: make install")
        print("  2. Run: make setup")
        print("  3. Start: make start")
        print("  4. Test: make test")
        print("  5. Access: http://localhost:7777")

        sys.exit(0)
    else:
        print("\n🛠️ Fix the issues above and run validation again")
        sys.exit(1)


if __name__ == "__main__":
    main()
