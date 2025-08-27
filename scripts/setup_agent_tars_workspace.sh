#!/bin/bash

# Setup script for Agent-TARS workspace with LANCELOTT tools integration
# This script creates symbolic links to all LANCELOTT tools in the Agent-TARS workspace

echo "🔧 Setting up Agent-TARS workspace with LANCELOTT tools integration..."
echo "==============================================================="

# Get directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_TARS_WORKSPACE="$PROJECT_ROOT/tools/UI-TARS/agent-tars-workspace"
TOOLS_DIR="$AGENT_TARS_WORKSPACE/tools"

echo "📁 Project Root: $PROJECT_ROOT"
echo "📁 Agent-TARS Workspace: $AGENT_TARS_WORKSPACE"
echo "📁 Tools Directory: $TOOLS_DIR"
echo ""

# Create tools directory if it doesn't exist
mkdir -p "$TOOLS_DIR"

# Change to tools directory
cd "$PROJECT_ROOT/tools"

# Create symbolic links for all tools
echo "🔗 Creating symbolic links for LANCELOTT tools..."
echo ""

# List all directories in tools (excluding security directory)
for tool_dir in */; do
    # Skip the security directory and the UI-TARS directory
    if [[ "$tool_dir" != "security/" && "$tool_dir" != "UI-TARS/" ]]; then
        tool_name="${tool_dir%/}"
        link_path="$TOOLS_DIR/$tool_name"

        # Remove existing link if it exists
        if [ -L "$link_path" ] || [ -d "$link_path" ]; then
            rm -rf "$link_path"
        fi

        # Create symbolic link
        ln -s "../../$tool_dir" "$link_path"
        echo "✅ Created symlink: $tool_name -> ../../$tool_dir"
    fi
done

echo ""
echo "✅ Agent-TARS workspace setup complete!"
echo ""
echo "📁 Tools are now accessible at: $TOOLS_DIR"
echo ""
echo "🚀 You can now start Agent-TARS with full tool integration:"
echo "   cd $PROJECT_ROOT"
echo "   ./lance --interactive"
