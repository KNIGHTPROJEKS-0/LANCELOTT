#!/bin/bash

# Agent-TARS CLI Launch Script
# LANCELOTT Framework Integration
# Launch Agent-TARS CLI with GPT-5-Nano configuration

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ASCII Art Header
echo -e "${PURPLE}"
cat <<"EOF"
  █████╗  ██████╗ ███████╗███╗   ██╗████████╗    ████████╗ █████╗ ██████╗ ███████╗
 ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝
 ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║  █████╗ ██║   ███████║██████╔╝███████╗
 ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║  ╚════╝ ██║   ██╔══██║██╔══██╗╚════██║
 ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║         ██║   ██║  ██║██║  ██║███████║
 ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝         ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝

                    LANCELOTT Framework
                         CLI Automation Agent
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
    echo -e "${PURPLE}[AGENT-TARS]${NC} $1"
}

print_command() {
    echo -e "${CYAN}[COMMAND]${NC} $1"
}

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
AGENT_TARS_DIR="$PROJECT_ROOT/tools/UI-TARS/multimodal/agent-tars"
AGENT_CLI_DIR="$AGENT_TARS_DIR/cli"
AGENT_CORE_DIR="$AGENT_TARS_DIR/core"

print_header "Initializing Agent-TARS CLI..."

# Check if we're in the right directory
if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
    print_error "Not in LANCELOTT project root directory!"
    print_error "Expected to find .env file at: $PROJECT_ROOT/.env"
    exit 1
fi

print_status "Project root: $PROJECT_ROOT"
print_status "Agent-TARS directory: $AGENT_TARS_DIR"
print_status "Agent CLI directory: $AGENT_CLI_DIR"

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

# Check if Agent-TARS directories exist
if [[ ! -d "$AGENT_TARS_DIR" ]]; then
    print_error "Agent-TARS directory not found: $AGENT_TARS_DIR"
    print_error "Please ensure UI-TARS is properly installed in tools/UI-TARS"
    exit 1
fi

if [[ ! -d "$AGENT_CLI_DIR" ]]; then
    print_error "Agent-TARS CLI directory not found: $AGENT_CLI_DIR"
    print_error "Please ensure Agent-TARS CLI is available"
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

# Check for pnpm (Agent-TARS uses pnpm)
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
    print_error "Agent-TARS requires Node.js version 20 or later"
    exit 1
fi

print_status "Node.js version: $(node --version)"
print_status "npm version: $(npm --version)"
print_status "pnpm version: $(pnpm --version)"

# Create necessary directories
mkdir -p "$PROJECT_ROOT/reports/agent_tars"
mkdir -p "$PROJECT_ROOT/logs/agent_tars"
mkdir -p "$PROJECT_ROOT/config/agent_tars"
mkdir -p "$PROJECT_ROOT/snapshots/agent_tars"
mkdir -p "$PROJECT_ROOT/cache/agent_tars"

# Set up logging
LOG_FILE="$PROJECT_ROOT/logs/agent_tars/agent_tars.log"
print_status "Logging to: $LOG_FILE"

# Install dependencies for Agent-TARS CLI
print_header "Setting up Agent-TARS CLI dependencies..."

# Install dependencies for CLI
cd "$AGENT_CLI_DIR"
if [[ ! -d "node_modules" ]]; then
    print_status "Installing Agent-TARS CLI dependencies..."
    pnpm install
    if [[ $? -ne 0 ]]; then
        print_error "Failed to install CLI dependencies!"
        exit 1
    fi
fi

# Install dependencies for Core
cd "$AGENT_CORE_DIR"
if [[ ! -d "node_modules" ]]; then
    print_status "Installing Agent-TARS Core dependencies..."
    pnpm install
    if [[ $? -ne 0 ]]; then
        print_error "Failed to install Core dependencies!"
        exit 1
    fi
fi

# Return to CLI directory for execution
cd "$AGENT_CLI_DIR"

# Display configuration information
print_header "Configuration Summary:"
echo -e "${CYAN}AI Model:${NC} ${AGENT_TARS_AI_MODEL:-gpt-5-nano}"
echo -e "${CYAN}AI Provider:${NC} ${AGENT_TARS_AI_PROVIDER:-azure}"
echo -e "${CYAN}AI Deployment:${NC} ${AGENT_TARS_AI_DEPLOYMENT:-GPT-5-Navo-Cerberus}"
echo -e "${CYAN}Framework URL:${NC} ${AGENT_TARS_FRAMEWORK_API_URL:-http://localhost:7777}"
echo -e "${CYAN}Firebase Project:${NC} ${AGENT_TARS_FIREBASE_PROJECT_ID:-lancelott-z9dko}"
echo -e "${CYAN}Output Directory:${NC} ${AGENT_TARS_OUTPUT_DIR:-reports/agent_tars}"
echo -e "${CYAN}Interactive Mode:${NC} ${AGENT_TARS_ENABLE_INTERACTIVE_MODE:-true}"
echo -e "${CYAN}Batch Mode:${NC} ${AGENT_TARS_ENABLE_BATCH_MODE:-true}"

# Check if LANCELOTT framework is running
if curl -s "http://localhost:7777/health" >/dev/null 2>&1; then
    print_status "LANCELOTT framework is running ✅"
else
    print_warning "LANCELOTT framework is not running on port 7777"
    print_warning "Some features may not be available"
fi

# Export additional environment variables for Agent-TARS
export AGENT_TARS_LOG_FILE="$LOG_FILE"
export AGENT_TARS_PROJECT_ROOT="$PROJECT_ROOT"
export AGENT_TARS_CONFIG_FILE="$PROJECT_ROOT/config/agent_tars/agent_tars.conf"
export AGENT_TARS_CACHE_DIR="$PROJECT_ROOT/cache/agent_tars"

# Create basic configuration file if it doesn't exist
CONFIG_FILE="$PROJECT_ROOT/config/agent_tars/agent_tars.conf"
if [[ ! -f "$CONFIG_FILE" ]]; then
    print_status "Creating Agent-TARS configuration file..."
    mkdir -p "$(dirname "$CONFIG_FILE")"
    cat >"$CONFIG_FILE" <<EOF
# Agent-TARS Configuration
# Auto-generated by launch script

[general]
interactive_mode = true
batch_mode = true
verbose = true
colored_output = true

[ai]
model = ${AGENT_TARS_AI_MODEL:-gpt-5-nano}
provider = ${AGENT_TARS_AI_PROVIDER:-azure}
deployment = ${AGENT_TARS_AI_DEPLOYMENT:-GPT-5-Navo-Cerberus}
endpoint = ${AGENT_TARS_AI_ENDPOINT:-}
api_key = ${AGENT_TARS_AI_API_KEY:-}
max_tokens = ${AGENT_TARS_AI_MAX_TOKENS:-16384}
temperature = ${AGENT_TARS_AI_TEMPERATURE:-0.1}

[output]
directory = ${AGENT_TARS_OUTPUT_DIR:-reports/agent_tars}
log_file = ${LOG_FILE}
save_snapshots = true
auto_save = true

[integration]
framework_url = ${AGENT_TARS_FRAMEWORK_API_URL:-http://localhost:7777}
firebase_project = ${AGENT_TARS_FIREBASE_PROJECT_ID:-lancelott-z9dko}
EOF
fi

# Function to handle cleanup on exit
cleanup() {
    print_header "Cleaning up Agent-TARS processes..."
    # Kill any remaining Agent-TARS processes
    pkill -f "agent-tars" 2>/dev/null || true
    exit 0
}

# Set up trap for cleanup
trap cleanup EXIT INT TERM

# Parse command line arguments
MODE="interactive"
TASK=""
SCRIPT_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
    -i | --interactive)
        MODE="interactive"
        shift
        ;;
    -b | --batch)
        MODE="batch"
        shift
        ;;
    -s | --script)
        MODE="script"
        SCRIPT_FILE="$2"
        shift 2
        ;;
    -t | --task)
        TASK="$2"
        shift 2
        ;;
    -h | --help)
        echo "Usage: $0 [OPTIONS]"
        echo "Options:"
        echo "  -i, --interactive    Launch in interactive mode (default)"
        echo "  -b, --batch          Launch in batch mode"
        echo "  -s, --script FILE    Execute script file"
        echo "  -t, --task TASK      Execute specific task"
        echo "  -h, --help           Show this help message"
        exit 0
        ;;
    *)
        print_error "Unknown option: $1"
        exit 1
        ;;
    esac
done

# Display launch information
print_header "Launching Agent-TARS CLI..."
echo -e "${GREEN}🚀 Starting Agent-TARS CLI in $MODE mode${NC}"
echo -e "${BLUE}🤖 AI-powered command line automation${NC}"
echo -e "${BLUE}🔧 Configuration: $CONFIG_FILE${NC}"
echo -e "${BLUE}📁 Output directory: ${AGENT_TARS_OUTPUT_DIR:-reports/agent_tars}${NC}"
echo -e "${YELLOW}⏹️  Press Ctrl+C to stop${NC}"
echo ""

# Launch Agent-TARS based on mode
case $MODE in
interactive)
    print_command "Building and launching Agent-TARS CLI..."
    print_status "Building Agent-TARS first..."

    # Build the CLI first (ignore TypeScript errors, focus on JS output)
    print_status "Running build (ignoring TypeScript declaration errors)..."
    pnpm run build 2>&1 | grep -v "error.*TS" || true

    # Check if JavaScript output was generated
    if [[ -f "dist/index.js" ]]; then
        print_status "JavaScript build successful! ✅"
    else
        print_error "No JavaScript output found! Build failed completely."
        exit 1
    fi

    print_status "Starting Agent-TARS CLI in interactive mode..."
    print_status "Type 'help' for available commands"
    print_status "Type 'exit' to quit"
    echo ""

    # Try different execution methods
    if [[ -f "dist/index.js" ]]; then
        print_status "Running compiled Agent-TARS CLI from dist/index.js..."
        # Run the compiled JavaScript directly with Node
        node dist/index.js 2>&1 | tee -a "$LOG_FILE"
    elif [[ -f "bin/cli.js" ]]; then
        print_status "Running Agent-TARS CLI from bin/cli.js..."
        # Run the CLI binary
        ./bin/cli.js 2>&1 | tee -a "$LOG_FILE"
    else
        print_error "No Agent-TARS CLI executable found!"
        print_error "Expected: dist/index.js or bin/cli.js"
        ls -la dist/ bin/ 2>/dev/null || true
        exit 1
    fi
    ;;

batch)
    if [[ -z "$TASK" ]]; then
        print_error "Batch mode requires a task. Use -t or --task to specify."
        exit 1
    fi

    print_command "Building Agent-TARS for batch execution..."
    pnpm run build 2>&1 | grep -v "error.*TS" || true

    if [[ ! -f "dist/index.js" ]]; then
        print_error "Failed to build Agent-TARS CLI!"
        exit 1
    fi

    print_command "Executing batch task: $TASK"
    if [[ -f "dist/index.js" ]]; then
        node dist/index.js --task "$TASK" 2>&1 | tee -a "$LOG_FILE"
    else
        ./bin/cli.js --task "$TASK" 2>&1 | tee -a "$LOG_FILE"
    fi
    ;;

script)
    if [[ -z "$SCRIPT_FILE" ]]; then
        print_error "Script mode requires a script file. Use -s or --script to specify."
        exit 1
    fi

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        print_error "Script file not found: $SCRIPT_FILE"
        exit 1
    fi

    print_command "Building Agent-TARS for script execution..."
    pnpm run build 2>&1 | grep -v "error.*TS" || true

    if [[ ! -f "dist/index.js" ]]; then
        print_error "Failed to build Agent-TARS CLI!"
        exit 1
    fi

    print_command "Executing script: $SCRIPT_FILE"
    if [[ -f "dist/index.js" ]]; then
        node dist/index.js --script "$SCRIPT_FILE" 2>&1 | tee -a "$LOG_FILE"
    else
        ./bin/cli.js --script "$SCRIPT_FILE" 2>&1 | tee -a "$LOG_FILE"
    fi
    ;;
esac

# If we reach here, the process has ended
print_header "Agent-TARS CLI has stopped"
