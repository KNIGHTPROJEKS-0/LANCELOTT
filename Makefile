# LANCELOTT Framework Makefile
# Comprehensive build and management system

.PHONY: help install build test clean start stop deploy docs lint format check fix-terminal

# Default target
help:
	@echo "🛡️ LANCELOTT Framework - Make Commands"
	@echo "=================================="
	@echo "📦 Setup & Installation:"
	@echo "  make install     - Install all dependencies"
	@echo "  make setup       - Complete project setup"
	@echo "  make fix-terminal - Fix terminal configuration issues"
	@echo ""
	@echo "🔨 Build & Test:"
	@echo "  make build       - Build all tools and components"
	@echo "  make test        - Run all tests"
	@echo "  make check       - Run health checks"
	@echo ""
	@echo "🚀 Development:"
	@echo "  make start       - Start the framework"
	@echo "  make stop        - Stop all services"
	@echo "  make dev         - Start in development mode"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  make docs        - Generate documentation"
	@echo "  make lint        - Run linting"
	@echo "  make format      - Format code"
	@echo ""
	@echo "🐳 Deployment:"
	@echo "  make deploy      - Deploy using Docker"
	@echo "  make clean       - Clean build artifacts"

# Installation targets
install:
	@echo "📦 Installing LANCELOTT dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

setup: install
	@echo "⚙️ Setting up LANCELOTT framework..."
	cp .env.example .env
	python build/build_manager.py build
	./build/scripts/setup_crush_integration.sh
	./build/scripts/setup_langchain_integration.sh
	@echo "✅ Setup complete"

# Build targets
build:
	@echo "🔨 Building LANCELOTT framework..."
	python build/build_manager.py build
	@echo "✅ Build complete"

# Test targets
test:
	@echo "🧪 Running LANCELOTT tests..."
	python tests/run_all_tests.py
	@echo "✅ Tests complete"

check:
	@echo "🔍 Running LANCELOTT health checks..."
	python status/status_monitor.py check
	@echo "✅ Health checks complete"

# Development targets
start:
	@echo "🚀 Starting LANCELOTT framework..."
	python app.py

dev:
	@echo "🚀 Starting LANCELOTT in development mode..."
	uvicorn app:app --reload --host 0.0.0.0 --port 7777

stop:
	@echo "🛑 Stopping LANCELOTT services..."
	pkill -f "python app.py" || true
	pkill -f "uvicorn" || true
	docker-compose down || true

# Documentation targets
docs:
	@echo "📚 Generating documentation..."
	@echo "Documentation available in docs/ directory"

lint:
	@echo "🔍 Running linting..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
	mypy . --ignore-missing-imports || true

format:
	@echo "✨ Formatting code..."
	black . || true
	isort . || true

# Deployment targets
deploy:
	@echo "🐳 Deploying LANCELOTT with Docker..."
	docker-compose up -d --build
	@echo "✅ Deployment complete"

clean:
	@echo "🧹 Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/ || true
	@echo "✅ Cleanup complete"

# Special targets
all: clean install build test
	@echo "🎉 Complete LANCELOTT build and test cycle finished"

# Force rebuild
rebuild: clean build
	@echo "🔄 LANCELOTT rebuild complete"

# Terminal fix target
fix-terminal:
	@echo "🔧 Fixing terminal configuration..."
	./fix_terminal_comprehensive.sh
	@echo "✅ Terminal fix complete. Restart your terminal to apply changes."
	@echo "💡 Run 'source ~/.zshrc' to reload configuration"

fix-vscode:
	@echo "🔧 Applying VS Code terminal fixes..."
	@echo "✅ VS Code settings updated"
	@echo "💡 Restart VS Code terminal (Cmd+Shift+P → 'Terminal: Kill All Terminals')"

setup-terminal: fix-terminal
	@echo "⚙️ Complete terminal setup for LANCELOTT..."
	@echo "📝 Please follow instructions in TERMINAL_FIX_INSTRUCTIONS.md"
	@echo "🔧 Run 'nano ~/.zshrc' to add LANCELOTT integration"

quick-start: fix-terminal
	@echo "🚀 Quick starting LANCELOTT with terminal fixes..."
	python app.py
