#!/bin/bash

# Dismap Installation Verification Script

echo "🌀 Dismap Installation Verification"
echo "===================================="
echo ""

# Check if dismap binary exists and is executable
echo "📁 Checking dismap binary..."
DISMAP_PATH="/Users/ORDEROFCODE/KNIGHTPROJEKS/CERBERUS-FANGS/LANCELOTT/dismap/dismap"
if [ -x "$DISMAP_PATH" ]; then
    echo "✅ Dismap binary found and executable at: $DISMAP_PATH"
    ls -la "$DISMAP_PATH"
else
    echo "❌ Dismap binary not found or not executable"
fi

echo ""
echo "🔗 Checking symlinks..."
if [ -L "/usr/local/bin/dismap" ]; then
    echo "✅ System-wide symlink exists: /usr/local/bin/dismap"
    ls -la /usr/local/bin/dismap
else
    echo "❌ System-wide symlink not found"
fi

if [ -L "/usr/local/bin/dismap-enhanced" ]; then
    echo "✅ Enhanced symlink exists: /usr/local/bin/dismap-enhanced"
    ls -la /usr/local/bin/dismap-enhanced
else
    echo "❌ Enhanced symlink not found"
fi

echo ""
echo "🛤️  Checking PATH configuration..."
if echo $PATH | grep -q "/Users/ORDEROFCODE/KNIGHTPROJEKS/CERBERUS-FANGS/LANCELOTT/dismap"; then
    echo "✅ Dismap directory is in PATH"
else
    echo "❌ Dismap directory not found in PATH"
fi

echo ""
echo "🧪 Testing commands..."
echo "Testing 'which dismap':"
which dismap

echo ""
echo "Testing 'which dismap-enhanced':"
which dismap-enhanced

echo ""
echo "Testing dismap version:"
dismap -h | head -10

echo ""
echo "🎯 Available Commands:"
echo "  dismap                    - Original dismap tool"
echo "  dismap-enhanced           - Enhanced wrapper with presets"
echo "  dismap-enhanced quick     - Quick scan with JSON output"
echo "  dismap-enhanced net       - Network scan with common ports"
echo "  dismap-enhanced full      - Full port scan"
echo "  dismap-enhanced stealth   - Stealth scan"
echo "  dismap-enhanced fast      - Fast scan"
echo ""
echo "✅ Dismap is fully configured and ready to use!"
echo "📍 You can now run 'dismap' or 'dismap-enhanced' from anywhere in your system."
