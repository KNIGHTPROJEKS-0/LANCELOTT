#!/usr/bin/env python3
"""
Firebase Configuration Validation Script for LANCELOTT
Validates Firebase setup, configuration files, and deployment readiness

This script ensures that all Firebase configurations are correct and the
system is ready for deployment to Firebase hosting and functions.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


class FirebaseConfigValidator:
    """
    Comprehensive Firebase configuration validator for LANCELOTT
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.errors = []
        self.warnings = []
        self.info = []

    def log_error(self, message: str):
        """Log an error message"""
        self.errors.append(f"❌ {message}")

    def log_warning(self, message: str):
        """Log a warning message"""
        self.warnings.append(f"⚠️  {message}")

    def log_info(self, message: str):
        """Log an info message"""
        self.info.append(f"ℹ️  {message}")

    def validate_firebase_json(self) -> bool:
        """Validate firebase.json configuration"""
        firebase_json_path = self.project_root / "firebase.json"

        if not firebase_json_path.exists():
            self.log_error("firebase.json not found")
            return False

        try:
            with open(firebase_json_path, "r") as f:
                config = json.load(f)

            # Check required sections
            required_sections = ["hosting", "functions", "firestore", "storage"]
            for section in required_sections:
                if section not in config:
                    self.log_warning(
                        f"Missing {section} configuration in firebase.json"
                    )
                else:
                    self.log_info(f"Found {section} configuration")

            # Validate hosting configuration
            if "hosting" in config:
                hosting = config["hosting"]

                if "public" not in hosting:
                    self.log_error("hosting.public not specified in firebase.json")
                else:
                    public_dir = self.project_root / hosting["public"]
                    if not public_dir.exists():
                        self.log_error(
                            f"Public directory {hosting['public']} does not exist"
                        )
                    else:
                        self.log_info(f"Public directory {hosting['public']} exists")

                        # Check for index.html
                        index_path = public_dir / "index.html"
                        if not index_path.exists():
                            self.log_warning(
                                f"index.html not found in {hosting['public']}"
                            )
                        else:
                            self.log_info("index.html found in public directory")

            # Validate functions configuration
            if "functions" in config:
                functions = config["functions"]

                if "source" not in functions:
                    self.log_error("functions.source not specified in firebase.json")
                else:
                    functions_dir = self.project_root / functions["source"]
                    if not functions_dir.exists():
                        self.log_error(
                            f"Functions directory {functions['source']} does not exist"
                        )
                    else:
                        self.log_info(
                            f"Functions directory {functions['source']} exists"
                        )

                        # Check for main.py
                        main_py = functions_dir / "main.py"
                        if not main_py.exists():
                            self.log_error("main.py not found in functions directory")
                        else:
                            self.log_info("main.py found in functions directory")

                        # Check for requirements.txt
                        requirements = functions_dir / "requirements.txt"
                        if not requirements.exists():
                            self.log_error(
                                "requirements.txt not found in functions directory"
                            )
                        else:
                            self.log_info(
                                "requirements.txt found in functions directory"
                            )

            return len(self.errors) == 0

        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON in firebase.json: {e}")
            return False
        except Exception as e:
            self.log_error(f"Error reading firebase.json: {e}")
            return False

    def validate_firebaserc(self) -> bool:
        """Validate .firebaserc configuration"""
        firebaserc_path = self.project_root / ".firebaserc"

        if not firebaserc_path.exists():
            self.log_error(".firebaserc not found")
            return False

        try:
            with open(firebaserc_path, "r") as f:
                config = json.load(f)

            if "projects" not in config:
                self.log_error("No projects configuration in .firebaserc")
                return False

            projects = config["projects"]
            if "default" not in projects:
                self.log_error("No default project specified in .firebaserc")
                return False

            default_project = projects["default"]
            self.log_info(f"Default Firebase project: {default_project}")

            # Validate project ID format
            if not re.match(r"^[a-z0-9-]+$", default_project):
                self.log_warning(f"Project ID '{default_project}' may not be valid")

            return True

        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON in .firebaserc: {e}")
            return False
        except Exception as e:
            self.log_error(f"Error reading .firebaserc: {e}")
            return False

    def validate_firestore_rules(self) -> bool:
        """Validate Firestore security rules"""
        rules_path = self.project_root / "firestore.rules"

        if not rules_path.exists():
            self.log_error("firestore.rules not found")
            return False

        try:
            with open(rules_path, "r") as f:
                rules_content = f.read()

            # Basic syntax checks
            if "rules_version" not in rules_content:
                self.log_warning("rules_version not specified in firestore.rules")

            if "service cloud.firestore" not in rules_content:
                self.log_error("Invalid Firestore rules format")
                return False

            # Check for authentication requirements
            if "request.auth != null" in rules_content:
                self.log_info("Authentication checks found in Firestore rules")
            else:
                self.log_warning("No authentication checks found in Firestore rules")

            self.log_info("Firestore rules file appears valid")
            return True

        except Exception as e:
            self.log_error(f"Error reading firestore.rules: {e}")
            return False

    def validate_storage_rules(self) -> bool:
        """Validate Cloud Storage security rules"""
        rules_path = self.project_root / "storage.rules"

        if not rules_path.exists():
            self.log_error("storage.rules not found")
            return False

        try:
            with open(rules_path, "r") as f:
                rules_content = f.read()

            # Basic syntax checks
            if "rules_version" not in rules_content:
                self.log_warning("rules_version not specified in storage.rules")

            if "service firebase.storage" not in rules_content:
                self.log_error("Invalid Storage rules format")
                return False

            # Check for authentication requirements
            if "request.auth != null" in rules_content:
                self.log_info("Authentication checks found in Storage rules")
            else:
                self.log_warning("No authentication checks found in Storage rules")

            self.log_info("Storage rules file appears valid")
            return True

        except Exception as e:
            self.log_error(f"Error reading storage.rules: {e}")
            return False

    def validate_firestore_indexes(self) -> bool:
        """Validate Firestore indexes configuration"""
        indexes_path = self.project_root / "firestore.indexes.json"

        if not indexes_path.exists():
            self.log_warning("firestore.indexes.json not found")
            return True  # Optional file

        try:
            with open(indexes_path, "r") as f:
                indexes = json.load(f)

            if "indexes" not in indexes:
                self.log_warning("No indexes defined in firestore.indexes.json")
            else:
                index_count = len(indexes["indexes"])
                self.log_info(f"Found {index_count} Firestore indexes")

            if "fieldOverrides" in indexes:
                override_count = len(indexes["fieldOverrides"])
                self.log_info(f"Found {override_count} field overrides")

            return True

        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON in firestore.indexes.json: {e}")
            return False
        except Exception as e:
            self.log_error(f"Error reading firestore.indexes.json: {e}")
            return False

    def validate_environment_config(self) -> bool:
        """Validate environment configuration"""
        env_path = self.project_root / ".env"

        if not env_path.exists():
            self.log_warning(".env file not found")
            env_example_path = self.project_root / ".env.example"
            if env_example_path.exists():
                self.log_info(".env.example found - can be used as template")
            return True  # Not strictly required

        try:
            with open(env_path, "r") as f:
                env_content = f.read()

            # Check for Firebase-related environment variables
            firebase_vars = [
                "FIREBASE_PROJECT_ID",
                "FIREBASE_API_KEY",
                "FIREBASE_AUTH_DOMAIN",
                "FIREBASE_STORAGE_BUCKET",
                "FIREBASE_MESSAGING_SENDER_ID",
                "FIREBASE_APP_ID",
            ]

            for var in firebase_vars:
                if f"{var}=" in env_content:
                    self.log_info(f"Found {var} in environment configuration")
                else:
                    self.log_warning(f"Missing {var} in environment configuration")

            # Check for service account path
            if "FIREBASE_SERVICE_ACCOUNT_PATH=" in env_content:
                self.log_info("Found Firebase service account path configuration")
            else:
                self.log_warning("Missing Firebase service account path")

            return True

        except Exception as e:
            self.log_error(f"Error reading .env: {e}")
            return False

    def validate_service_account(self) -> bool:
        """Validate Firebase service account configuration"""
        # Check for service account in config/firebase/
        config_dir = self.project_root / "config" / "firebase"

        if not config_dir.exists():
            self.log_error("config/firebase directory not found")
            return False

        # Look for service account JSON files
        service_accounts = list(config_dir.glob("*.json"))

        if not service_accounts:
            self.log_error("No Firebase service account JSON files found")
            return False

        for sa_file in service_accounts:
            try:
                with open(sa_file, "r") as f:
                    sa_data = json.load(f)

                required_fields = [
                    "type",
                    "project_id",
                    "private_key_id",
                    "private_key",
                    "client_email",
                    "client_id",
                ]

                for field in required_fields:
                    if field not in sa_data:
                        self.log_error(
                            f"Missing {field} in service account {sa_file.name}"
                        )
                        return False

                if sa_data.get("type") != "service_account":
                    self.log_error(f"Invalid service account type in {sa_file.name}")
                    return False

                self.log_info(f"Valid service account found: {sa_file.name}")
                self.log_info(f"Project ID: {sa_data.get('project_id')}")

            except json.JSONDecodeError as e:
                self.log_error(f"Invalid JSON in service account {sa_file.name}: {e}")
                return False
            except Exception as e:
                self.log_error(f"Error reading service account {sa_file.name}: {e}")
                return False

        return True

    def validate_functions_code(self) -> bool:
        """Validate Firebase Functions code"""
        functions_dir = self.project_root / "functions"

        if not functions_dir.exists():
            self.log_warning("functions directory not found")
            return True  # Optional

        main_py = functions_dir / "main.py"
        if not main_py.exists():
            self.log_error("main.py not found in functions directory")
            return False

        try:
            with open(main_py, "r") as f:
                main_content = f.read()

            # Check for required imports
            required_imports = ["firebase_functions", "firebase_admin"]

            for import_name in required_imports:
                if import_name in main_content:
                    self.log_info(f"Found {import_name} import in main.py")
                else:
                    self.log_warning(f"Missing {import_name} import in main.py")

            # Check for function definitions
            if "def " in main_content or "@https_fn." in main_content:
                self.log_info("Function definitions found in main.py")
            else:
                self.log_warning("No function definitions found in main.py")

            return True

        except Exception as e:
            self.log_error(f"Error reading main.py: {e}")
            return False

    def validate_all(self) -> Tuple[bool, Dict[str, Any]]:
        """Run all validations and return results"""
        self.errors.clear()
        self.warnings.clear()
        self.info.clear()

        validations = [
            ("Firebase JSON", self.validate_firebase_json),
            ("Firebase RC", self.validate_firebaserc),
            ("Firestore Rules", self.validate_firestore_rules),
            ("Storage Rules", self.validate_storage_rules),
            ("Firestore Indexes", self.validate_firestore_indexes),
            ("Environment Config", self.validate_environment_config),
            ("Service Account", self.validate_service_account),
            ("Functions Code", self.validate_functions_code),
        ]

        results = {}
        overall_success = True

        for name, validation_func in validations:
            try:
                result = validation_func()
                results[name] = result
                if not result:
                    overall_success = False
            except Exception as e:
                self.log_error(f"Validation error in {name}: {e}")
                results[name] = False
                overall_success = False

        return overall_success, {
            "results": results,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
        }

    def print_results(self, overall_success: bool, details: Dict[str, Any]):
        """Print validation results in a formatted way"""
        print("🔥 Firebase Configuration Validation Report")
        print("=" * 60)
        print()

        # Print summary
        if overall_success:
            print("✅ Overall Status: PASSED")
        else:
            print("❌ Overall Status: FAILED")
        print()

        # Print individual results
        print("📋 Validation Results:")
        for name, result in details["results"].items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {name}")
        print()

        # Print errors
        if details["errors"]:
            print("❌ Errors:")
            for error in details["errors"]:
                print(f"  {error}")
            print()

        # Print warnings
        if details["warnings"]:
            print("⚠️  Warnings:")
            for warning in details["warnings"]:
                print(f"  {warning}")
            print()

        # Print info
        if details["info"]:
            print("ℹ️  Information:")
            for info in details["info"]:
                print(f"  {info}")
            print()

        # Print summary
        error_count = len(details["errors"])
        warning_count = len(details["warnings"])
        info_count = len(details["info"])

        print(
            f"📊 Summary: {error_count} errors, {warning_count} warnings, {info_count} info"
        )

        if overall_success:
            print("🚀 Ready for Firebase deployment!")
        else:
            print("🔧 Please fix the errors before deploying.")


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate Firebase configuration for LANCELOTT"
    )
    parser.add_argument(
        "--project-root", default=".", help="Path to project root directory"
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Only show errors and warnings"
    )

    args = parser.parse_args()

    validator = FirebaseConfigValidator(args.project_root)
    overall_success, details = validator.validate_all()

    if not args.quiet:
        validator.print_results(overall_success, details)
    else:
        # Quiet mode - only show errors and warnings
        for error in details["errors"]:
            print(error)
        for warning in details["warnings"]:
            print(warning)

    # Exit with appropriate code
    sys.exit(0 if overall_success else 1)


if __name__ == "__main__":
    main()
