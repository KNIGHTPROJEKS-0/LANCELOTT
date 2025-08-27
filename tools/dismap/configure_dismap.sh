#!/bin/bash

# Dismap Configuration Script
# This script helps configure dismap for easier usage

echo "🌀 Dismap Configuration Tool"
echo "================================"

# Check if dismap binary exists
if [ ! -f "./dismap" ]; then
    echo "❌ Error: dismap binary not found in current directory"
    echo "Please ensure you are in the dismap directory and the binary is present"
    exit 1
fi

# Make sure it's executable
chmod +x ./dismap

echo "✅ Dismap binary is ready and executable"

# Check if we can add to PATH
DISMAP_DIR=$(pwd)

echo ""
echo "📁 Current dismap location: $DISMAP_DIR"
echo ""

# Offer to create symlink
echo "🔗 Would you like to create a symlink in /usr/local/bin for global access? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    if sudo ln -sf "$DISMAP_DIR/dismap" /usr/local/bin/dismap; then
        echo "✅ Symlink created successfully! You can now run 'dismap' from anywhere."
    else
        echo "❌ Failed to create symlink. You may need administrator privileges."
        echo "💡 Alternative: Add this to your ~/.zshrc or ~/.bashrc:"
        echo "export PATH=\"$DISMAP_DIR:\$PATH\""
    fi
else
    echo "💡 To use dismap globally, add this to your ~/.zshrc or ~/.bashrc:"
    echo "export PATH=\"$DISMAP_DIR:\$PATH\""
fi

echo ""
echo "🎯 Quick Test Commands:"
echo "  Local usage:    ./dismap -h"
echo "  Test scan:      ./dismap -u https://example.com"
echo "  Network scan:   ./dismap -i 192.168.1.0/24"
echo "  Save results:   ./dismap -i 192.168.1.0/24 -o results.txt -j results.json"
echo ""
echo "📚 For more examples, check the readme.md file"
echo ""
echo "✅ Dismap configuration complete!"
