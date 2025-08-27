#!/usr/bin/env python3
"""
CERBERUS-FANGS LANCELOTT - Status Summary
"""

import os
from datetime import datetime


def print_header():
    print("🐺" * 25)
    print("🐺 CERBERUS-FANGS LANCELOTT - STATUS SUMMARY 🐺")
    print("🐺" * 25)
    print()


def check_unified_environment():
    print("📦 UNIFIED ENVIRONMENT STATUS")
    print("=" * 40)

    # Check requirements.txt
    if os.path.exists("requirements.txt"):
        with open("requirements.txt") as f:
            lines = [
                l.strip() for l in f.readlines() if l.strip() and not l.startswith("#")
            ]
        print(f"✅ Unified requirements.txt: {len(lines)} packages")
    else:
        print("❌ requirements.txt missing")

    # Check if old requirements files exist
    old_reqs = ["requirements-core.txt"]
    for req in old_reqs:
        if os.path.exists(req):
            print(f"⚠️  Legacy requirement file found: {req}")

    print()


def check_docker_integration():
    print("🐳 DOCKER INTEGRATION STATUS")
    print("=" * 40)

    files_to_check = {
        "Dockerfile": "Multi-stage container build",
        "docker-compose.yml": "Full stack orchestration",
        ".dockerignore": "Build optimization (optional)",
    }

    for file, desc in files_to_check.items():
        if os.path.exists(file):
            print(f"✅ {file}: {desc}")
        else:
            print(f"❌ {file}: {desc}")

    print()


def check_api_integration():
    print("🌐 API INTEGRATION STATUS")
    print("=" * 40)

    # Check main API file
    if os.path.exists("main.py"):
        print("✅ main.py: FastAPI main application")
    else:
        print("❌ main.py: FastAPI main application")

    # Check API routes
    route_dir = "api/routes"
    if os.path.exists(route_dir):
        routes = [
            f for f in os.listdir(route_dir) if f.endswith(".py") and f != "__init__.py"
        ]
        print(f"✅ API routes: {len(routes)} tool endpoints")
        for route in sorted(routes):
            tool_name = route.replace(".py", "").replace("_", "-")
            print(f"   📡 /api/v1/{tool_name}")
    else:
        print("❌ API routes directory missing")

    # Check port configuration
    if os.path.exists("core/port_config.py"):
        print("✅ Port configuration: Unified port mapping")
    else:
        print("❌ Port configuration missing")

    print()


def check_tools_status():
    print("🔧 SECURITY TOOLS STATUS")
    print("=" * 40)

    tools = {
        "Argus": "Web application reconnaissance",
        "Kraken": "Advanced brute force framework",
        "Spiderfoot": "OSINT automation tool",
        "Social-Analyzer": "Social media OSINT analysis",
        "RedTeam-ToolKit": "Django red team web app",
        "Storm-Breaker": "Social engineering toolkit",
        "PhoneSploit-Pro": "Android exploitation framework",
        "Metabigor": "Intelligence gathering tool",
        "Osmedeus": "Automated reconnaissance",
        "Webstor": "Web application storage analysis",
        "THC-Hydra": "Network login cracker",
        "dismap": "Asset discovery tool",
    }

    found_tools = 0
    total_tools = len(tools)

    for tool, desc in tools.items():
        if os.path.exists(tool):
            print(f"✅ {tool}: {desc}")
            found_tools += 1
        else:
            print(f"❌ {tool}: {desc}")

    print(f"\n📊 Tools Found: {found_tools}/{total_tools}")
    print()


def check_deployment_readiness():
    print("🚀 DEPLOYMENT READINESS")
    print("=" * 40)

    checks = {
        "startup.sh": "Unified startup script",
        "test_system.py": "System validation script",
        "DEPLOYMENT_GUIDE.md": "Deployment documentation",
        "logs": "Logging directory",
        "core": "Core framework directory",
    }

    ready_count = 0
    total_checks = len(checks)

    for item, desc in checks.items():
        if os.path.exists(item):
            print(f"✅ {item}: {desc}")
            ready_count += 1
        else:
            print(f"❌ {item}: {desc}")

    print(f"\n📊 Readiness: {ready_count}/{total_checks}")

    if ready_count == total_checks:
        print("🎉 SYSTEM READY FOR DEPLOYMENT!")
    else:
        print("⚠️  Some components missing")

    print()


def show_quick_start():
    print("🚀 QUICK START COMMANDS")
    print("=" * 40)

    print("Docker Deployment:")
    print("  docker-compose up -d --build")
    print()

    print("Manual Deployment:")
    print("  ./startup.sh")
    print()

    print("System Test:")
    print("  python3 test_system.py")
    print()

    print("Access API:")
    print("  curl http://localhost:7777/api/v1/health")
    print("  open http://localhost:7777/docs")
    print()


def main():
    print_header()
    check_unified_environment()
    check_docker_integration()
    check_api_integration()
    check_tools_status()
    check_deployment_readiness()
    show_quick_start()

    print("=" * 50)
    print(f"📅 Status generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🐺 CERBERUS-FANGS LANCELOTT - Ready to Hunt! 🐺")


if __name__ == "__main__":
    main()
