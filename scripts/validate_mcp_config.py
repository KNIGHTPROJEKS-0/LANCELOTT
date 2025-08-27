#!/usr/bin/env python3
"""
MCP Configuration Validation Script for LANCELOTT Framework
This script validates the MCP configuration files and checks for common issues.
"""

import json
import os
import sys
from pathlib import Path


def validate_json_config(config_path):
    """Validate the MCP JSON configuration file"""
    print(f"🔍 Validating JSON configuration: {config_path}")

    if not os.path.exists(config_path):
        print(f"❌ Configuration file not found: {config_path}")
        return False

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        print("✅ JSON syntax is valid")

        # Check required fields
        required_fields = ["name", "version", "servers"]
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required field: {field}")
                return False

        print("✅ Required fields present")

        # Validate servers configuration
        servers = config.get("servers", [])
        if not servers:
            print("⚠️ No servers configured")
        else:
            print(f"✅ Found {len(servers)} server(s) configured")

            for i, server in enumerate(servers):
                server_id = server.get("id", f"server_{i}")
                print(f"  📦 Server {i+1} ({server_id}):")

                # Check required server fields
                server_required = ["id", "name", "command", "args"]
                for field in server_required:
                    if field not in server:
                        print(f"    ❌ Missing required field: {field}")
                        return False

                # Check Redis server configuration
                if (
                    "redis" in server_id.lower()
                    or "redis" in server.get("name", "").lower()
                ):
                    args = server.get("args", [])
                    redis_url_found = False
                    for arg in args:
                        if "redis://" in arg:
                            redis_url_found = True
                            # Check if URL has database number
                            if "/0" in arg or "/1" in arg or "/2" in arg:
                                print(f"    ✅ Redis URL format is correct: {arg}")
                            else:
                                print(
                                    f"    ⚠️ Redis URL might be missing database number: {arg}"
                                )
                                print(f"    💡 Recommended format: {arg}/0")

                    if not redis_url_found:
                        print(f"    ⚠️ No Redis URL found in args")

                    # Check environment variables
                    env = server.get("env", {})
                    if "REDIS_URL" in env:
                        print(f"    ✅ REDIS_URL environment variable is set")
                    else:
                        print(f"    ⚠️ REDIS_URL environment variable is missing")

        # Check workspace configuration
        workspace = config.get("workspace", {})
        if workspace:
            print("✅ Workspace configuration found")
            if "path" in workspace:
                print(f"  📁 Workspace path: {workspace['path']}")
            if "toolsPath" in workspace:
                print(f"  🛠️ Tools path: {workspace['toolsPath']}")
        else:
            print("⚠️ No workspace configuration found")

        return True

    except json.JSONDecodeError as e:
        print(f"❌ JSON syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error validating configuration: {e}")
        return False


def validate_ts_config(config_path):
    """Validate the Agent-TARS TypeScript configuration file"""
    print(f"🔍 Validating TypeScript configuration: {config_path}")

    if not os.path.exists(config_path):
        print(f"❌ Configuration file not found: {config_path}")
        return False

    try:
        with open(config_path, "r") as f:
            content = f.read()

        print("✅ TypeScript configuration file exists")

        # Check for required sections
        required_sections = ["mcpServers", "workspace", "name", "version"]

        for section in required_sections:
            if section in content:
                print(f"✅ Found section: {section}")
            else:
                print(f"❌ Missing section: {section}")

        # Check Redis server configuration
        if "mcp-server-redis" in content:
            print("✅ Redis server configuration found")

            # Check for Redis URL with database number
            if "redis://localhost:6379/0" in content:
                print("✅ Redis URL format is correct")
            elif "redis://localhost:6379" in content:
                print("⚠️ Redis URL might be missing database number")
                print("💡 Recommended format: redis://localhost:6379/0")
        else:
            print("⚠️ Redis server configuration not found")

        # Check for other MCP servers
        mcp_servers = ["mcp-server-chart", "mcp-server-file", "mcp-server-postgres"]

        for server in mcp_servers:
            if server in content:
                print(f"✅ {server} configuration found")
            else:
                print(f"⚠️ {server} configuration not found")

        return True

    except Exception as e:
        print(f"❌ Error validating TypeScript configuration: {e}")
        return False


def main():
    """Main validation function"""
    print("🛡️ LANCELOTT MCP Configuration Validation")
    print("=" * 50)

    project_root = Path(__file__).parent.parent
    mcp_dir = project_root / "tools" / "UI-TARS" / "multimodal"

    print(f"📁 Project Root: {project_root}")
    print(f"📁 MCP Directory: {mcp_dir}")
    print()

    # Validate JSON configuration
    json_config_path = mcp_dir / "mcp-config.json"
    json_valid = validate_json_config(json_config_path)
    print()

    # Validate TypeScript configuration
    ts_config_path = mcp_dir / "agent-tars.config.ts"
    ts_valid = validate_ts_config(ts_config_path)
    print()

    # Overall result
    print("📊 Validation Summary")
    print("=" * 20)

    if json_valid and ts_valid:
        print("✅ All configurations are valid")
        print("🚀 MCP integration is properly configured")
        return 0
    else:
        print("❌ Some configuration issues found")
        print("📝 Please review the errors above and fix the configuration files")
        return 1


if __name__ == "__main__":
    sys.exit(main())
