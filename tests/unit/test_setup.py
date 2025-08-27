#!/usr/bin/env python3
"""
Simple test script to verify FastAPI setup
"""

print("Testing CERBERUS-FANGS LANCELOTT setup...")

try:
    import sys
    print(f"✓ Python {sys.version}")
    
    # Test basic imports
    import asyncio
    print("✓ asyncio available")
    
    import json
    print("✓ json available")
    
    import subprocess
    print("✓ subprocess available")
    
    import os
    from pathlib import Path
    print("✓ os and pathlib available")
    
    # Test if we can import our modules
    try:
        from core.config import settings
        print("✓ Configuration loaded")
        print(f"  - Base directory: {settings.BASE_DIR}")
        print(f"  - Host: {settings.HOST}:{settings.PORT}")
    except ImportError as e:
        print(f"✗ Could not import config: {e}")
    
    try:
        import fastapi
        print(f"✓ FastAPI {fastapi.__version__} available")
    except ImportError:
        print("✗ FastAPI not available")
    
    try:
        import uvicorn
        print("✓ Uvicorn available")
    except ImportError:
        print("✗ Uvicorn not available")
    
    # Check tool directories
    print("\nChecking tool directories:")
    tools = [
        "Argus", "Kraken", "Metabigor", "dismap", "Osmedeus", 
        "Spiderfoot", "Social-Analyzer", "Storm-Breaker", 
        "PhoneSploit-Pro", "Vajra", "RedTeam_ToolKit", "UI-TARS"
    ]
    
    for tool in tools:
        tool_path = Path(tool)
        if tool_path.exists():
            print(f"✓ {tool}")
        else:
            print(f"✗ {tool} (not found)")
    
    # Check nmap
    try:
        result = subprocess.run(["nmap", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ {version_line}")
        else:
            print("✗ nmap command failed")
    except subprocess.TimeoutExpired:
        print("✗ nmap command timed out")
    except FileNotFoundError:
        print("✗ nmap not found in PATH")
    
    print("\n🎉 CERBERUS-FANGS LANCELOTT basic setup verified!")
    print("\nNext steps:")
    print("1. Install remaining dependencies: pip install -r requirements-core.txt")
    print("2. Configure .env file")
    print("3. Run: python main.py")
    
except Exception as e:
    print(f"\n❌ Error during setup verification: {e}")
    import traceback
    traceback.print_exc()
