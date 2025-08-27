#!/usr/bin/env python3
"""
CERBERUS-FANGS LANCELOTT - Smart Startup Script
Automatically detects and runs the appropriate application entry point
"""

import os
import subprocess
import sys
from pathlib import Path


def detect_environment():
    """Detect the current environment and available components"""
    project_root = Path(__file__).parent

    # Check for enhanced app
    enhanced_app = project_root / "app.py"
    legacy_app = project_root / "main.py"
    cli_tool = project_root / "lancelott.py"

    # Check for configuration
    config_file = project_root / "config" / "lancelott.yaml"

    # Check for virtual environment
    venv_python = None
    possible_venvs = [
        project_root / ".venv" / "bin" / "python",
        project_root / "venv" / "bin" / "python",
        project_root / ".venv" / "Scripts" / "python.exe",
        project_root / "venv" / "Scripts" / "python.exe",
    ]

    for venv_path in possible_venvs:
        if venv_path.exists():
            venv_python = str(venv_path)
            break

    return {
        "enhanced_app": enhanced_app.exists(),
        "legacy_app": legacy_app.exists(),
        "cli_tool": cli_tool.exists(),
        "config_exists": config_file.exists(),
        "venv_python": venv_python,
        "project_root": project_root,
    }


def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "aiohttp",
        "psutil",
        "pyyaml",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    return missing_packages


def install_dependencies(missing_packages, venv_python=None):
    """Install missing dependencies"""
    python_cmd = venv_python or sys.executable

    print(f"📦 Installing missing dependencies: {', '.join(missing_packages)}")

    try:
        cmd = [python_cmd, "-m", "pip", "install"] + missing_packages
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False


def show_startup_banner():
    """Show startup banner"""
    banner = """
🛡️  LANCELOTT v2.1.0
════════════════════════════════════
Professional Penetration Testing Suite
Enhanced Security Framework with AI Integration
"""
    print(banner)


def show_usage():
    """Show usage information"""
    usage = """
🚀 LANCELOTT Startup Options:

Direct Commands:
  python start.py                    # Smart auto-start (recommended)
  python start.py --cli              # Use CLI interface
  python start.py --legacy           # Use legacy mode
  python start.py --config           # Show configuration
  python start.py --check            # Check system health

Enhanced App:
  python app.py                      # Direct enhanced app
  python lancelott.py start          # CLI start command
  python lancelott.py --help         # Full CLI help

Legacy Support:
  python main.py                     # Legacy compatibility

Advanced:
  uvicorn app:app --host 0.0.0.0 --port 7777 --reload
  python -m uvicorn app:app --workers 4
"""
    print(usage)


def main():
    """Main startup logic"""
    args = sys.argv[1:]

    # Handle help and usage
    if "--help" in args or "-h" in args:
        show_usage()
        return

    show_startup_banner()

    # Detect environment
    env = detect_environment()
    print(f"📂 Project root: {env['project_root']}")

    # Handle specific flags
    if "--config" in args:
        if env["config_exists"]:
            print("⚙️ Configuration file found")
            try:
                from config.lancelott_config import get_config

                config = get_config()
                summary = config.get_configuration_summary()
                print(f"🔧 API: {summary['api']['host']}:{summary['api']['port']}")
                print(
                    f"🛠️ Tools: {summary['tools']['enabled']}/{summary['tools']['total']} enabled"
                )
            except Exception as e:
                print(f"❌ Failed to load configuration: {e}")
        else:
            print("⚠️ No configuration file found")
        return

    if "--check" in args:
        print("🔍 Checking system health...")
        missing_deps = check_dependencies()
        if missing_deps:
            print(f"⚠️ Missing dependencies: {missing_deps}")
            print("💡 Run with --install-deps to install them")
        else:
            print("✅ All dependencies are installed")

        print(f"📱 Enhanced app: {'✅' if env['enhanced_app'] else '❌'}")
        print(f"🔧 CLI tool: {'✅' if env['cli_tool'] else '❌'}")
        print(f"⚙️ Configuration: {'✅' if env['config_exists'] else '❌'}")
        print(f"🐍 Virtual env: {'✅' if env['venv_python'] else '❌'}")
        return

    if "--install-deps" in args:
        missing_deps = check_dependencies()
        if missing_deps:
            success = install_dependencies(missing_deps, env["venv_python"])
            if not success:
                sys.exit(1)
        else:
            print("✅ All dependencies already installed")
        return

    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        print(f"⚠️ Missing dependencies: {missing_deps}")
        print("📦 Installing dependencies automatically...")
        if not install_dependencies(missing_deps, env["venv_python"]):
            print("❌ Failed to install dependencies. Please install manually:")
            print(f"   pip install {' '.join(missing_deps)}")
            sys.exit(1)

    # Determine startup mode
    if "--cli" in args:
        if env["cli_tool"]:
            print("🖥️ Starting CLI interface...")
            os.execv(
                env["venv_python"] or sys.executable,
                [sys.executable, str(env["project_root"] / "lancelott.py")]
                + [arg for arg in args if arg != "--cli"],
            )
        else:
            print("❌ CLI tool not found")
            sys.exit(1)

    elif "--legacy" in args:
        if env["legacy_app"]:
            print("🔄 Starting legacy application...")
            os.execv(
                env["venv_python"] or sys.executable,
                [sys.executable, str(env["project_root"] / "main.py")],
            )
        else:
            print("❌ Legacy application not found")
            sys.exit(1)

    else:
        # Smart auto-start
        if env["enhanced_app"]:
            print("🚀 Starting enhanced LANCELOTT application...")
            print("🌐 API will be available at: http://localhost:7777")
            print("📚 Documentation: http://localhost:7777/docs")
            print("🔄 Workflows: http://localhost:5678 (n8n)")
            print("\n⌨️  Press Ctrl+C to stop\n")

            try:
                os.execv(
                    env["venv_python"] or sys.executable,
                    [sys.executable, str(env["project_root"] / "app.py")],
                )
            except KeyboardInterrupt:
                print("\n👋 LANCELOTT stopped by user")
            except Exception as e:
                print(f"❌ Failed to start application: {e}")
                sys.exit(1)

        elif env["legacy_app"]:
            print("🔄 Enhanced app not found, falling back to legacy...")
            os.execv(
                env["venv_python"] or sys.executable,
                [sys.executable, str(env["project_root"] / "main.py")],
            )

        else:
            print("❌ No application entry point found")
            print("💡 Please ensure the project is properly set up")
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Startup interrupted by user")
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        sys.exit(1)
