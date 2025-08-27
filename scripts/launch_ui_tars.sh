#!/bin/bash

# UI-TARS Desktop Launch Script
# LANCELOTT Framework Integration
# Launch UI-TARS Desktop with GPT-5-Nano configuration

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Header
echo -e "${CYAN}"
cat <<"EOF"
 ██╗   ██╗██╗      ████████╗ █████╗ ██████╗ ███████╗
 ██║   ██║██║      ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝
 ██║   ██║██║  █████╗ ██║   ███████║██████╔╝███████╗
 ██║   ██║██║  ╚════╝ ██║   ██╔══██║██╔══██╗╚════██║
 ╚██████╔╝██║         ██║   ██║  ██║██║  ██║███████║
  ╚═════╝ ╚═╝         ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝

      LANCELOTT Framework
           Desktop GUI Automation
        Powered by GPT-5-Nano Azure AI
EOF
echo -e "${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[UI-TARS]${NC} $1"
}

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
UI_TARS_DIR="$PROJECT_ROOT/tools/UI-TARS"

print_header "Initializing UI-TARS Desktop..."

# Check if we're in the right directory
if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
    print_error "Not in LANCELOTT project root directory!"
    print_error "Expected to find .env file at: $PROJECT_ROOT/.env"
    exit 1
fi

print_status "Project root: $PROJECT_ROOT"
print_status "UI-TARS directory: $UI_TARS_DIR"

# Load environment variables
if [[ -f "$PROJECT_ROOT/.env" ]]; then
    print_status "Loading environment variables from .env"
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
else
    print_error ".env file not found!"
    exit 1
fi

# Check if UI-TARS directory exists
if [[ ! -d "$UI_TARS_DIR" ]]; then
    print_error "UI-TARS directory not found: $UI_TARS_DIR"
    print_error "Please ensure UI-TARS is properly installed in tools/UI-TARS"
    exit 1
fi

# Check for Node.js
if ! command -v node &>/dev/null; then
    print_error "Node.js is not installed!"
    print_error "Please install Node.js (version 20 or later) from https://nodejs.org/"
    exit 1
fi

# Check for npm
if ! command -v npm &>/dev/null; then
    print_error "npm is not installed!"
    print_error "npm should come with Node.js installation"
    exit 1
fi

# Check for pnpm (UI-TARS uses pnpm)
if ! command -v pnpm &>/dev/null; then
    print_warning "pnpm is not installed. Installing pnpm..."
    npm install -g pnpm
    if [[ $? -ne 0 ]]; then
        print_error "Failed to install pnpm!"
        exit 1
    fi
fi

# Verify Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [[ $NODE_VERSION -lt 20 ]]; then
    print_error "Node.js version $NODE_VERSION is too old!"
    print_error "UI-TARS requires Node.js version 20 or later"
    exit 1
fi

print_status "Node.js version: $(node --version)"
print_status "npm version: $(npm --version)"
print_status "pnpm version: $(pnpm --version)"

# Change to UI-TARS directory
cd "$UI_TARS_DIR"

# Check if package.json exists
if [[ ! -f "package.json" ]]; then
    print_error "package.json not found in UI-TARS directory!"
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [[ ! -d "node_modules" ]]; then
    print_status "Installing UI-TARS dependencies..."
    pnpm install
    if [[ $? -ne 0 ]]; then
        print_error "Failed to install dependencies!"
        exit 1
    fi
fi

# Check for required configuration files
CONFIG_FILES=(
    "cerberus-gpt5-nano-preset.yaml"
    "ui-tars.conf"
)

for config_file in "${CONFIG_FILES[@]}"; do
    if [[ ! -f "$config_file" ]]; then
        print_warning "Configuration file not found: $config_file"
        print_warning "Using default configuration..."
    else
        print_status "Found configuration: $config_file"
    fi
done

# Display configuration information
print_header "Configuration Summary:"
echo -e "${CYAN}AI Model:${NC} ${UI_TARS_AI_MODEL:-gpt-5-nano}"
echo -e "${CYAN}AI Provider:${NC} ${UI_TARS_AI_PROVIDER:-azure}"
echo -e "${CYAN}AI Deployment:${NC} ${UI_TARS_AI_DEPLOYMENT:-GPT-5-Navo-Cerberus}"
echo -e "${CYAN}Desktop Port:${NC} ${UI_TARS_PORT:-8765}"
echo -e "${CYAN}Web Port:${NC} ${UI_TARS_WEB_PORT:-5173}"
echo -e "${CYAN}Framework URL:${NC} ${UI_TARS_FRAMEWORK_API_URL:-http://localhost:7777}"
echo -e "${CYAN}Firebase Project:${NC} ${UI_TARS_FIREBASE_PROJECT_ID:-lancelott-z9dko}"

# Check if LANCELOTT framework is running
if curl -s "http://localhost:7777/health" >/dev/null 2>&1; then
    print_status "LANCELOTT framework is running ✅"
else
    print_warning "LANCELOTT framework is not running on port 7777"
    print_warning "Some features may not be available"
fi

# Create necessary directories
mkdir -p "$PROJECT_ROOT/reports/ui_tars_automation"
mkdir -p "$PROJECT_ROOT/reports/screenshots"
mkdir -p "$PROJECT_ROOT/reports/recordings"
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/cache/ui_tars"

# Set up logging
LOG_FILE="$PROJECT_ROOT/logs/ui_tars_desktop.log"
print_status "Logging to: $LOG_FILE"

# Export additional environment variables for UI-TARS
export UI_TARS_PRESET_PATH="$UI_TARS_DIR/cerberus-gpt5-nano-preset.yaml"
export UI_TARS_LOG_FILE="$LOG_FILE"
export UI_TARS_PROJECT_ROOT="$PROJECT_ROOT"

# Function to handle cleanup on exit
cleanup() {
    print_header "Cleaning up UI-TARS processes..."
    # Kill any remaining UI-TARS processes
    pkill -f "ui-tars" 2>/dev/null || true
    pkill -f "electron" 2>/dev/null || true
    exit 0
}

# Set up trap for cleanup
trap cleanup EXIT INT TERM

# Display launch information
print_header "Launching UI-TARS Desktop..."
echo -e "${GREEN}🚀 Starting UI-TARS Desktop Application${NC}"
echo -e "${BLUE}📱 Desktop app will open automatically${NC}"
echo -e "${BLUE}🌐 Web interface: http://localhost:${UI_TARS_WEB_PORT:-5173}${NC}"
echo -e "${BLUE}🔧 Internal API: http://localhost:${UI_TARS_PORT:-8765}${NC}"
echo -e "${YELLOW}⏹️  Press Ctrl+C to stop${NC}"
echo ""

# Launch UI-TARS Desktop
print_status "Executing: pnpm run dev:ui-tars"

# Start UI-TARS with proper logging
pnpm run dev:ui-tars 2>&1 | tee -a "$LOG_FILE"

# If we reach here, the process has ended
print_header "UI-TARS Desktop has stopped"
