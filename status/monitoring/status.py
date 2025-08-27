#!/usr/bin/env python3
"""
CERBERUS-FANGS LANCELOTT - Status Check
Quick status verification for the security toolkit
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def check_port(port):
    """Check if a port is in use"""
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(("localhost", port))
        return result == 0


def main():
    print("🛡️ CERBERUS-FANGS LANCELOTT - Status Check")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # System Info
    print("📋 System Information:")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  Platform: {sys.platform}")
    print(f"  Working Directory: {os.getcwd()}")
    print()

    # Port Status
    print("🌐 Port Status:")
    ports_to_check = [7777, 8080, 9999]
    for port in ports_to_check:
        status = "🔴 IN USE" if check_port(port) else "🟢 AVAILABLE"
        note = ""
        if port == 8080:
            note = " (Jenkins - avoid this port)"
        elif port == 7777:
            note = " (FastAPI main server)"
        elif port == 9999:
            note = " (Minimal web interface)"
        print(f"  Port {port}: {status}{note}")
    print()

    # Tool Status
    print("🛠️ Security Tools Status:")

    # Check nmap
    try:
        result = subprocess.run(
            ["nmap", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.split("\n")[0]
            print(f"  ✅ {version}")
        else:
            print("  ❌ Nmap: Error running command")
    except:
        print("  ❌ Nmap: Not found or not accessible")

    # Check tool directories
    tools = [
        ("Argus", "./Argus"),
        ("Kraken", "./Kraken"),
        ("Metabigor", "./Metabigor"),
        ("Dismap", "./dismap"),
        ("Osmedeus", "./Osmedeus"),
        ("SpiderFoot", "./Spiderfoot"),
        ("Social Analyzer", "./Social-Analyzer"),
        ("Storm Breaker", "./Storm-Breaker"),
        ("PhoneSploit Pro", "./PhoneSploit-Pro"),
        ("Vajra", "./Vajra"),
        ("RedTeam ToolKit", "./RedTeam_ToolKit"),
        ("UI-TARS", "./UI-TARS"),
        ("SuperGateway", "./SuperGateway"),
        ("SuperCompat", "./SuperCompat"),
    ]

    available_tools = 0
    for name, path in tools:
        if Path(path).exists():
            print(f"  ✅ {name}")
            available_tools += 1
        else:
            print(f"  ❌ {name} (directory not found)")

    print()
    print(f"📊 Summary: {available_tools}/{len(tools)} tools available")

    # FastAPI Status
    print()
    print("⚡ FastAPI Setup Status:")

    # Check if virtual environment exists
    venv_exists = Path(".venv").exists()
    print(f"  Virtual Environment: {'✅ Present' if venv_exists else '❌ Missing'}")

    # Check if main files exist
    files_to_check = [
        ("main.py", "Main FastAPI application"),
        ("requirements.txt", "Full dependencies"),
        ("requirements-core.txt", "Core dependencies"),
        (".env.example", "Environment template"),
        ("setup.sh", "Full setup script"),
        ("quick_setup.sh", "Quick setup script"),
    ]

    for filename, description in files_to_check:
        exists = Path(filename).exists()
        print(
            f"  {filename}: {'✅ Present' if exists else '❌ Missing'} ({description})"
        )

    # Check if .env exists
    env_exists = Path(".env").exists()
    print(
        f"  .env configuration: {'✅ Present' if env_exists else '⚠️  Missing (copy from .env.example)'}"
    )

    print()
    print("🚀 Quick Start Options:")
    print()
    print("1️⃣ Minimal Interface (Currently Running):")
    print("   🌐 http://localhost:9999")
    print("   📝 Basic HTML interface with tool status")
    print()
    print("2️⃣ Quick FastAPI Setup:")
    print("   💻 scripts/quick_setup.sh")
    print("   ⚡ python main.py")
    print("   🌐 http://localhost:7777/docs")
    print()
    print("3️⃣ Full Setup with All Dependencies:")
    print("   💻 ./setup.sh")
    print("   ⚡ python main.py")
    print("   🌐 http://localhost:7777/docs")
    print()
    print("🔐 Default Credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   ⚠️  Change these in production!")
    print()

    # Recommendations
    print("💡 Recommendations:")
    if not venv_exists:
        print("   • Run scripts/quick_setup.sh to create virtual environment")
    if not env_exists:
        print("   • Copy .env.example to .env and configure")
    if available_tools < len(tools):
        print("   • Some tools are missing - check tool directories")
    print("   • Avoid port 8080 (Jenkins conflict)")
    print("   • Use port 7777 for main FastAPI server")
    print("   • Use port 9999 for development/testing")


if __name__ == "__main__":
    main()
