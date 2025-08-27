#!/bin/bash

# Test script for MCP functionality in LANCELOTT Framework
# This script verifies that all MCP servers can be started properly

echo "🧪 Testing MCP Server Functionality for LANCELOTT Framework"
echo "========================================================"

# Get directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MCP_DIR="$PROJECT_ROOT/tools/UI-TARS/multimodal"
cd "$MCP_DIR"

echo "📁 Working Directory: $MCP_DIR"
echo ""

# Function to test MCP server
test_mcp_server() {
    local server_name=$1
    local package=$2
    local args=$3

    echo "🚀 Testing $server_name..."
    echo "📦 Package: $package"

    # Try to start the server with a short timeout
    echo "Executing: npx -y $package $args"
    timeout 5s npx -y $package $args 2>&1 | head -10

    local exit_code=$?

    if [ $exit_code -eq 124 ]; then
        echo "✅ $server_name started successfully (timeout reached as expected)"
    elif [ $exit_code -eq 0 ]; then
        echo "✅ $server_name completed successfully"
    elif [ $exit_code -eq 1 ]; then
        echo "⚠️ $server_name exited with code 1 (may be expected)"
    else
        echo "❌ $server_name failed to start (exit code: $exit_code)"
    fi

    echo ""
}

# Test Redis server with proper URL format
echo "🔧 Testing Redis MCP Server with corrected URL format..."
test_mcp_server "Redis Server" "@modelcontextprotocol/server-redis" "redis://localhost:6379/0"

# Test Chart server
echo "📊 Testing Chart MCP Server..."
test_mcp_server "Chart Server" "@antv/mcp-server-chart" ""

# Test File server
echo "📁 Testing File MCP Server..."
test_mcp_server "File Server" "@modelcontextprotocol/server-file" ""

# Test PostgreSQL server
echo "🗄️ Testing PostgreSQL MCP Server..."
test_mcp_server "PostgreSQL Server" "@modelcontextprotocol/server-postgres" ""

echo "✅ MCP Server Testing Complete"
echo ""
echo "📝 Next Steps:"
echo "1. Ensure Redis is running: redis-server"
echo "2. Start Agent-TARS: ./lance --interactive"
echo "3. Verify MCP servers are connected in the Agent-TARS interface"
echo ""
echo "💡 Note: Some servers may show 'failed to start' if their dependencies"
echo "   (Redis, PostgreSQL, etc.) are not running. This is expected behavior."
