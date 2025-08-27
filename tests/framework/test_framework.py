#!/usr/bin/env python3
"""
LANCELOTT Framework Validation Test
Tests the reorganized framework components
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def test_framework_structure():
    """Test the basic framework structure"""
    print("🔍 Testing LANCELOTT Framework Structure...")

    # Test directory structure
    required_dirs = [
        "tools",
        "build",
        "integrations",
        "status",
        "config",
        "api",
        "docs",
    ]

    print("\n📁 Directory Structure Test:")
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ - MISSING")

    # Test key files
    key_files = [
        "app.py",
        "lancelott.py",
        "start.py",
        "config/lancelott.yaml",
        "config/lancelott_config.py",
        "README.md",
    ]

    print("\n📄 Key Files Test:")
    for file_name in key_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"  ✅ {file_name}")
        else:
            print(f"  ❌ {file_name} - MISSING")

    # Test tools directory
    print("\n🛠️ Tools Directory Test:")
    tools_dir = project_root / "tools"
    if tools_dir.exists():
        tools = [d.name for d in tools_dir.iterdir() if d.is_dir()]
        print(f"  ✅ Found {len(tools)} security tools:")
        for tool in sorted(tools):
            print(f"    - {tool}")
    else:
        print("  ❌ Tools directory not found")


def test_python_imports():
    """Test Python imports for key components"""
    print("\n🐍 Python Import Tests:")

    # Add project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))

    test_imports = [
        ("config.lancelott_config", "Configuration System"),
        ("build.build_manager", "Build Manager"),
        ("integrations.integration_manager", "Integration Manager"),
        ("status.status_monitor", "Status Monitor"),
        ("core.config", "Legacy Configuration"),
    ]

    for module_name, description in test_imports:
        try:
            __import__(module_name)
            print(f"  ✅ {description}: Import OK")
        except ImportError as e:
            print(f"  ❌ {description}: Import Failed - {e}")
        except Exception as e:
            print(f"  ⚠️ {description}: Import Warning - {e}")


def test_configuration():
    """Test configuration system"""
    print("\n⚙️ Configuration System Test:")

    try:
        from config.lancelott_config import get_config

        config = get_config()

        print(f"  ✅ Configuration loaded successfully")
        print(f"  📊 Total tools configured: {len(config.tools)}")
        print(f"  🔧 Enabled tools: {len(config.get_enabled_tools())}")
        print(f"  🌐 API Port: {config.api.port}")

        # Test configuration validation
        issues = config.validate_configuration()
        if issues:
            print(f"  ⚠️ Configuration validation issues found: {len(issues)}")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print(f"  ✅ Configuration validation: PASSED")

    except Exception as e:
        print(f"  ❌ Configuration test failed: {e}")


def test_build_system():
    """Test build system"""
    print("\n🔨 Build System Test:")

    try:
        from build.build_manager import BuildManager

        build_manager = BuildManager()

        print(f"  ✅ Build manager created successfully")

        # Get build targets
        targets = build_manager._define_build_targets()
        print(f"  📦 Build targets defined: {len(targets)}")

        # Check for different build types
        build_types = set()
        for target in targets.values():
            if "build_type" in target:
                build_types.add(target["build_type"])

        print(f"  🔧 Build types supported: {', '.join(sorted(build_types))}")

    except Exception as e:
        print(f"  ❌ Build system test failed: {e}")


def test_integration_system():
    """Test integration system"""
    print("\n🔗 Integration System Test:")

    try:
        from integrations.integration_manager import IntegrationManager

        integration_manager = IntegrationManager()

        print(f"  ✅ Integration manager created successfully")

        # Check default configurations
        default_configs = integration_manager._load_default_configs()
        print(f"  🛠️ Default tool configs: {len(default_configs)}")

        # Check tool status
        status = integration_manager.get_tool_status()
        print(f"  📊 Tool status entries: {len(status)}")

    except Exception as e:
        print(f"  ❌ Integration system test failed: {e}")


def test_documentation():
    """Test documentation completeness"""
    print("\n📚 Documentation Test:")

    project_root = Path(__file__).parent
    docs_dir = project_root / "docs"

    required_docs = [
        "docs/api/API_REFERENCE.md",
        "docs/tools/TOOLS_REFERENCE.md",
        "docs/CONFIGURATION_GUIDE.md",
        "README.md",
    ]

    for doc_file in required_docs:
        doc_path = project_root / doc_file
        if doc_path.exists():
            size_kb = doc_path.stat().st_size / 1024
            print(f"  ✅ {doc_file} ({size_kb:.1f}KB)")
        else:
            print(f"  ❌ {doc_file} - MISSING")


def main():
    """Run all framework tests"""
    print("🛡️ CERBERUS-FANGS LANCELOTT Framework Validation")
    print("=" * 60)

    test_framework_structure()
    test_python_imports()
    test_configuration()
    test_build_system()
    test_integration_system()
    test_documentation()

    print("\n" + "=" * 60)
    print("🎯 Framework validation completed!")
    print("\n💡 To start the framework:")
    print("  python start.py")
    print("  python app.py")
    print("  python lancelott.py start")


if __name__ == "__main__":
    main()
