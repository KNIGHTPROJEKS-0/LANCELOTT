#!/bin/bash
# Quick LANCELOTT Environment Setup

echo "⚡ Quick LANCELOTT Setup"
echo "======================="

# Go to project directory
cd /Users/ORDEROFCODE/KNIGHTPROJEKS/CERBERUS-FANGS/LANCELOTT

# Activate virtual environment if it exists
if [[ -d ".venv" ]]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export LANCELOTT_ENV=development

# Quick dependency check
echo "📦 Installing critical dependencies..."
pip install fastapi uvicorn python-multipart python-jose[cryptography] >/dev/null 2>&1

echo ""
echo "🎯 LANCELOTT is ready!"
echo "Run one of these commands:"
echo "  python app.py"
echo "  make start"
echo "  uvicorn app:app --reload --host 0.0.0.0 --port 7777"
echo ""
echo "🌐 Once running, visit:"
echo "  Main: http://localhost:7777"
echo "  Docs: http://localhost:7777/docs"
echo ""
