#!/bin/bash

# CERBERUS-FANGS LANCELOTT GitHub Deployment Script
# This script handles Git initialization, commit, and GitHub upload

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
██╗      █████╗ ███╗   ██╗ ██████╗███████╗██╗      ██████╗ ████████╗████████╗
██║     ██╔══██╗████╗  ██║██╔════╝██╔════╝██║     ██╔═══██╗╚══██╔══╝╚══██╔══╝
██║     ███████║██╔██╗ ██║██║     █████╗  ██║     ██║   ██║   ██║      ██║
██║     ██╔══██║██║╚██╗██║██║     ██╔══╝  ██║     ██║   ██║   ██║      ██║
███████╗██║  ██║██║ ╚████║╚██████╗███████╗███████╗╚██████╔╝   ██║      ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚══════╝ ╚═════╝    ╚═╝      ╚═╝

    LANCELOTT Security Framework Deployment
            GitHub Repository Upload Script
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
    echo -e "${BLUE}[DEPLOY]${NC} $1"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

print_header "Starting LANCELOTT GitHub Deployment..."

# Check if we're in the right directory
if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
    print_error "Not in LANCELOTT project root directory!"
    print_error "Expected to find .env file at: $PROJECT_ROOT/.env"
    exit 1
fi

print_status "Project root: $PROJECT_ROOT"

# Check for required commands
if ! command -v git &>/dev/null; then
    print_error "Git is not installed!"
    exit 1
fi

if ! command -v gh &>/dev/null; then
    print_warning "GitHub CLI is not installed. We'll use Git directly."
    USE_GH_CLI=false
else
    USE_GH_CLI=true
fi

# Configuration
GITHUB_USERNAME="KNIGHTPROJEKS-0"
GITHUB_EMAIL="knightprojeks@gmail.com"
REPO_NAME="LANCELOTT"
GITHUB_TOKEN="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"

print_header "Configuration Summary:"
echo -e "${CYAN}GitHub Username:${NC} $GITHUB_USERNAME"
echo -e "${CYAN}GitHub Email:${NC} $GITHUB_EMAIL"
echo -e "${CYAN}Repository Name:${NC} $REPO_NAME"
echo -e "${CYAN}Using GitHub CLI:${NC} $USE_GH_CLI"

# Step 1: Configure Git
print_header "Step 1: Configuring Git..."
git config user.name "$GITHUB_USERNAME"
git config user.email "$GITHUB_EMAIL"
print_status "Git configuration complete"

# Step 2: Check Git status
print_header "Step 2: Checking Git repository status..."

if [[ ! -d ".git" ]]; then
    print_status "Initializing Git repository..."
    git init
    git branch -M main
fi

# Step 3: Add all files
print_header "Step 3: Adding files to Git..."
git add .

# Step 4: Check what will be committed
print_header "Step 4: Checking staged files..."
git status --short | head -20
TOTAL_FILES=$(git status --porcelain | wc -l)
print_status "Total files to commit: $TOTAL_FILES"

# Step 5: Create commit
print_header "Step 5: Creating commit..."
COMMIT_MESSAGE="Initial commit: LANCELOTT Security Framework with Agent-TARS & UI-TARS integration

🛡️ LANCELOTT - Unified Security Toolkit
- Complete FastAPI-based security framework
- Integrated multiple security tools (Argus, Kraken, Metabigor, etc.)
- AI-powered automation with GPT-5-Nano Azure integration
- Agent-TARS CLI for multimodal AI automation
- UI-TARS Desktop for GUI automation
- Firebase authentication and cloud functions
- Comprehensive orchestration system
- Docker containerization support
- N8N workflow automation integration

Features:
✅ 15+ Security Tools Integration
✅ Azure AI Foundry GPT-5-Nano Integration
✅ Agent-TARS Multimodal AI CLI
✅ UI-TARS Desktop Automation
✅ Firebase Cloud Functions
✅ Comprehensive API Layer
✅ Docker & Orchestration Support"

git commit -m "$COMMIT_MESSAGE"
print_status "Commit created successfully"

# Step 6: Create GitHub repository and upload
print_header "Step 6: Creating GitHub repository and uploading..."

if [[ "$USE_GH_CLI" == true ]]; then
    print_status "Using GitHub CLI to create repository..."

    # Authenticate with GitHub CLI
    echo "$GITHUB_TOKEN" | gh auth login --with-token

    # Create repository
    gh repo create "$REPO_NAME" --public --description "🛡️ LANCELOTT - Unified Security Toolkit with AI-powered automation, Agent-TARS CLI, UI-TARS Desktop, and comprehensive penetration testing framework" --clone=false

    # Add remote and push
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git" 2>/dev/null || true
    git push -u origin main

else
    print_status "Using Git directly to push to GitHub..."

    # Add remote
    git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git" 2>/dev/null || true

    # Push to GitHub
    git push -u origin main
fi

print_header "Step 7: Deployment Complete!"
echo -e "${GREEN}✅ Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
echo -e "${GREEN}✅ Clone URL: git clone https://github.com/$GITHUB_USERNAME/$REPO_NAME.git${NC}"

print_header "Repository Information:"
echo -e "${CYAN}📁 Repository:${NC} $REPO_NAME"
echo -e "${CYAN}🔗 URL:${NC} https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo -e "${CYAN}👤 Owner:${NC} $GITHUB_USERNAME"
echo -e "${CYAN}📊 Total Files:${NC} $TOTAL_FILES"
echo -e "${CYAN}🌟 Features:${NC} Agent-TARS, UI-TARS, GPT-5-Nano, Firebase, Security Tools"

print_status "LANCELOTT Framework successfully deployed to GitHub!"
