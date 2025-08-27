#!/bin/bash

# Test script for MCP servers in LANCELOTT Framework
# This script verifies that all MCP servers can be started properly

echo "🧪 Testing MCP Server Configuration for LANCELOTT Framework"
echo "========================================================="

# Get directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MCP_DIR="$PROJECT_ROOT/tools/UI-TARS/multimodal"
cd "$MCP_DIR"

echo "📁 Working Directory: $MCP_DIR"

# Function to test MCP server
test_mcp_server() {
    local server_name=$1
    local command=$2
    local args=$3

    echo "🚀 Testing $server_name..."

    # Try to start the server with a short timeout
    timeout 10s $command $args 2>&1 | head -20

    if [ $? -eq 124 ]; then
        echo "✅ $server_name started successfully (timeout reached as expected)"
    elif [ $? -eq 0 ]; then
        echo "✅ $server_name completed successfully"
    else
        echo "❌ $server_name failed to start"
    fi

    echo ""
}

# Test Redis server with proper URL format
echo "🔧 Testing Redis MCP Server with corrected URL format..."
test_mcp_server "Redis Server" "npx" "-y @modelcontextprotocol/server-redis redis://localhost:6379/0"

# Test Chart server
echo "📊 Testing Chart MCP Server..."
test_mcp_server "Chart Server" "npx" "-y @antvis/mcp-server-chart"

# Test File server
echo "📁 Testing File MCP Server..."
test_mcp_server "File Server" "npx" "-y @modelcontextprotocol/server-file"

echo "✅ MCP Server Testing Complete"
echo ""
echo "📝 Next Steps:"
echo "1. Ensure Redis is running: redis-server"
echo "2. Start Agent-TARS: ./agent-tars --interactive"
echo "3. Verify MCP servers are connected in the Agent-TARS interface"
