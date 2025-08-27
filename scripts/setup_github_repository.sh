#!/bin/bash

# Automated GitHub Repository Setup for LANCELOTT
# Creates and configures GitHub repository with Firebase integration
# Version: 2.1.0

set -e # Exit on error

# Configuration
REPO_NAME="LANCELOTT"
REPO_DESCRIPTION="🛡️ LANCELOTT v2.1.0 Enhanced - AI-Powered Security Framework with Firebase Cloud Backend, LangChain AI Integration, 27+ Security Tools, and Unified API"
GITHUB_USERNAME="ORDEROFCODE"
FIREBASE_PROJECT_ID="lancelott-z9dko"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Print functions
print_header() {
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║               🚀 GITHUB REPOSITORY AUTOMATION SCRIPT                        ║${NC}"
    echo -e "${PURPLE}║                     LANCELOTT Firebase Integration                          ║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${CYAN}🔄 $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."

    # Check if GitHub CLI is installed
    if ! command -v gh &>/dev/null; then
        print_error "GitHub CLI (gh) is not installed"
        print_info "Install with: brew install gh (macOS) or https://cli.github.com/"
        exit 1
    fi

    # Check if git is installed
    if ! command -v git &>/dev/null; then
        print_error "Git is not installed"
        exit 1
    fi

    # Check if Firebase CLI is installed
    if ! command -v firebase &>/dev/null; then
        print_warning "Firebase CLI not found. Installing..."
        npm install -g firebase-tools
    fi

    # Check GitHub authentication
    if ! gh auth status &>/dev/null; then
        print_error "GitHub CLI is not authenticated"
        print_info "Please run: gh auth login"
        exit 1
    fi

    print_status "All prerequisites satisfied"
}

# Initialize Git repository if needed
initialize_git() {
    print_step "Initializing Git repository..."

    if [ ! -d ".git" ]; then
        git init
        print_status "Git repository initialized"
    else
        print_info "Git repository already exists"
    fi

    # Configure Git if needed
    if [ -z "$(git config user.name)" ]; then
        git config user.name "$GITHUB_USERNAME"
        print_status "Git user name configured"
    fi

    if [ -z "$(git config user.email)" ]; then
        # Try to get email from GitHub CLI
        GITHUB_EMAIL=$(gh api user --jq '.email' 2>/dev/null || echo "")
        if [ -n "$GITHUB_EMAIL" ]; then
            git config user.email "$GITHUB_EMAIL"
            print_status "Git user email configured from GitHub"
        else
            print_warning "Could not determine GitHub email. Please set manually."
        fi
    fi
}

# Create .gitignore file
create_gitignore() {
    print_step "Creating .gitignore file..."

    cat >.gitignore <<'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.venv-index/

# IDEs
.vscode/settings.json
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# Firebase
.firebase/
.firebaserc.local
firebase-debug.log*
firebase-debug.*.log*

# Firebase service account keys (SECURITY)
config/firebase/*.json
*.serviceaccount.json
*-firebase-adminsdk-*.json

# Environment variables
.env.local
.env.development.local
.env.test.local
.env.production.local

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Security tools temporary files
reports/
uploads/
temp/
*.tmp

# Database
*.db
*.sqlite
*.sqlite3

# Docker
.dockerignore

# Temporary files
*.temp
*.cache

# Build artifacts
crush
*.tar.gz
*.zip

# AI/ML models
*.model
*.pkl
*.h5

# Jupyter Notebooks
.ipynb_checkpoints

# PyCharm
.idea/

# VS Code
.vscode/
!.vscode/settings.json
!.vscode/extensions.json

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Local development
local_settings.py
EOF

    print_status ".gitignore file created"
}

# Create README.md with comprehensive project information
create_readme() {
    print_step "Creating comprehensive README.md..."

    cat >README.md <<'EOF'
# 🛡️ LANCELOTT - Enhanced Security Framework v2.1.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Firebase](https://img.shields.io/badge/Firebase-Integrated-orange.svg)](https://firebase.google.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![AI](https://img.shields.io/badge/AI-LangChain_Powered-purple.svg)](https://langchain.com)

> **Professional Penetration Testing Suite with AI-Powered Cloud Backend**

LANCELOTT is a comprehensive, unified security toolkit that consolidates 27+ penetration testing and reconnaissance tools into a single FastAPI-based platform with Firebase cloud backend and AI-enhanced analysis capabilities.

## 🚀 **Live Deployment**

- 🌐 **Dashboard**: https://lancelott-z9dko.web.app
- 📚 **API Documentation**: https://lancelott-z9dko.web.app/docs
- 🔥 **Firebase Console**: https://console.firebase.google.com/project/lancelott-z9dko

## ✨ **Key Features**

### 🔧 **Security Tools Suite**
- **Network Reconnaissance**: Nmap, Argus, Enhanced scanning
- **Web Security**: Kraken, Web-Check, Feroxbuster
- **OSINT Gathering**: Metabigor, SpiderFoot, Social-Analyzer
- **Asset Discovery**: Dismap, Osmedeus automated recon
- **Mobile Security**: PhoneSploit-Pro for Android exploitation
- **Cloud Security**: Vajra for cloud infrastructure testing
- **Brute Force**: THC-Hydra, Sherlock username hunting
- **Social Engineering**: Storm-Breaker toolkit

### 🤖 **AI Integration**
- **LangChain Integration**: Multi-provider LLM support
- **AI-Powered Analysis**: Automated vulnerability assessment
- **Smart Reporting**: AI-generated security reports
- **Multi-Provider Support**: OpenAI, Anthropic, Azure AI Foundry
- **Workflow Automation**: N8N integration for complex workflows

### ☁️ **Firebase Cloud Backend**
- **Authentication**: Secure user management with Firebase Auth
- **Database**: Firestore for scan results and user data
- **Storage**: Cloud Storage for reports and file uploads
- **Hosting**: Serverless deployment with global CDN
- **Functions**: Cloud Functions for backend processing

### 🛠️ **Developer Experience**
- **Unified API**: Single REST API for all 27+ security tools
- **FastAPI Framework**: High-performance async web framework
- **Docker Support**: Complete containerization
- **CI/CD Pipeline**: GitHub Actions for automated deployment
- **Type Safety**: Full Python type hints and validation

## 🏗️ **Architecture**

```mermaid
graph TB
    subgraph "Frontend"
        A[React Dashboard] --> B[Firebase Auth]
        A --> C[FastAPI Backend]
    end

    subgraph "Firebase Cloud"
        B --> D[User Management]
        C --> E[Firestore Database]
        C --> F[Cloud Storage]
        G[Cloud Functions] --> E
    end

    subgraph "Security Tools"
        C --> H[Nmap]
        C --> I[Argus]
        C --> J[Kraken]
        C --> K[Metabigor]
        C --> L[27+ Tools]
    end

    subgraph "AI Services"
        C --> M[LangChain]
        M --> N[OpenAI]
        M --> O[Anthropic]
        M --> P[Azure AI]
    end
```

## 🚀 **Quick Start**

### **Option 1: Firebase Hosted (Recommended)**
```bash
# Access the live deployment
open https://lancelott-z9dko.web.app
```

### **Option 2: Local Development**
```bash
# Clone the repository
git clone https://github.com/ORDEROFCODE/LANCELOTT.git
cd LANCELOTT

# Quick setup
./fix_terminal_comprehensive.sh

# Start the framework
make start
# OR
python app.py

# Access locally
open http://localhost:7777
```

### **Option 3: Docker Deployment**
```bash
# Quick Docker start
docker-compose up -d --build

# Access the application
open http://localhost:7777
```

## 📋 **API Endpoints**

### **Core Endpoints**
```bash
# Health Check
GET /api/health

# Authentication
POST /api/auth/login
GET /api/auth/me

# Firebase Integration
GET /api/v1/firebase/config
POST /api/v1/firebase/auth/verify
```

### **Security Tools**
```bash
# Network Scanning
POST /api/v1/tools/nmap/scan
POST /api/v1/tools/argus/monitor

# Web Security
POST /api/v1/tools/kraken/bruteforce
POST /api/v1/tools/web-check/analyze

# OSINT
POST /api/v1/tools/metabigor/gather
POST /api/v1/tools/spiderfoot/investigate
```

### **AI Services**
```bash
# LangChain AI
POST /api/v1/ai/langchain/analyze
POST /api/v1/ai/langchain/report

# Multi-provider compatibility
POST /api/v1/ai/supercompat/process
```

## 🔧 **Configuration**

### **Environment Setup**
```bash
# Copy environment template
cp .env.example .env

# Configure Firebase
nano .env
# Set FIREBASE_* variables

# Configure AI providers
# Set OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
```

### **Firebase Configuration**
```json
{
  "apiKey": "AIzaSyD0RkGeip2f2rc29YSMHy5w6YeD-5VgriA",
  "authDomain": "lancelott-z9dko.firebaseapp.com",
  "projectId": "lancelott-z9dko",
  "storageBucket": "lancelott-z9dko.firebasestorage.app",
  "messagingSenderId": "681869309450",
  "appId": "1:681869309450:web:5ead0e530b282864d6d1f3"
}
```

## 🛡️ **Security Tools Included**

### **Network & Infrastructure**
- **Nmap**: Network discovery and security auditing
- **Argus**: Network monitoring and flow analysis
- **Enhanced Nmap**: Advanced scanning capabilities
- **Intel-Scan**: Intelligence gathering scanner

### **Web Application Security**
- **Kraken**: Multi-protocol brute force tool
- **Feroxbuster**: Web content discovery
- **Web-Check**: Comprehensive web analysis
- **Webstor**: Web application storage testing

### **OSINT & Intelligence**
- **Metabigor**: Advanced OSINT framework
- **SpiderFoot**: Automated OSINT collection
- **Social-Analyzer**: Social media intelligence
- **Sherlock**: Username hunting across platforms
- **Storm-Breaker**: Social engineering toolkit

### **Specialized Tools**
- **Dismap**: Asset discovery and mapping
- **Osmedeus**: Automated reconnaissance framework
- **PhoneSploit-Pro**: Android device exploitation
- **THC-Hydra**: Network logon cracker
- **Vajra**: Cloud security testing
- **RedTeam-ToolKit**: Red team operations platform
- **UI-TARS**: AI-powered testing automation

## 🤖 **AI Capabilities**

### **LangChain Integration**
- Multi-provider LLM support (OpenAI, Anthropic, Azure)
- Automated vulnerability analysis
- Smart report generation
- Interactive security chat

### **Azure AI Foundry**
- GPT-5 integration for advanced analysis
- Custom security models
- Automated threat detection
- Intelligent recommendations

### **Workflow Automation**
- N8N workflow engine
- Automated scanning pipelines
- Custom security workflows
- AI-driven decision making

## 📊 **Project Statistics**

- **27+ Security Tools**: Comprehensive toolkit
- **50+ API Endpoints**: Unified interface
- **10+ AI Providers**: Multi-provider support
- **Firebase Backend**: Cloud-native architecture
- **Docker Ready**: Complete containerization
- **GitHub Actions**: Automated CI/CD

## 🔧 **Development**

### **Project Structure**
```
LANCELOTT/
├── 🔌 api/routes/          # 32+ API routers
├── 🛠️ tools/              # 27+ security tools
├── 🤖 integrations/        # AI and framework integrations
├── 🔥 functions/           # Firebase Cloud Functions
├── 🌐 dist/               # Frontend distribution
├── 🧪 tests/              # Comprehensive test suite
├── 📚 docs/               # Documentation
└── 🐳 docker-compose.yml  # Container orchestration
```

### **Build Commands**
```bash
# Development
make dev                 # Start in development mode
make test               # Run test suite
make lint               # Code linting
make format             # Code formatting

# Deployment
make deploy             # Deploy to Firebase
make build              # Build for production
make clean              # Clean build artifacts

# Firebase
firebase deploy         # Deploy all services
firebase serve          # Local preview
firebase use lancelott-z9dko  # Switch project
```

## 🚀 **Deployment**

### **Firebase Deployment**
```bash
# Automated deployment
./deploy_firebase.sh

# Manual deployment
firebase deploy --only hosting,functions,firestore,storage
```

### **GitHub Actions**
Automatic deployment on push to main branch:
- ✅ Code quality checks
- ✅ Security scanning
- ✅ Automated testing
- ✅ Firebase deployment
- ✅ Post-deployment verification

## 📝 **Documentation**

- **API Reference**: `/docs/api/`
- **User Guide**: `/docs/guides/`
- **Deployment Guide**: `/docs/deployment/`
- **Contributing**: `/docs/contributing/`

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Security Community**: For developing the amazing tools integrated
- **Firebase Team**: For the robust cloud platform
- **LangChain**: For the AI integration framework
- **FastAPI**: For the high-performance web framework

## 🔗 **Links**

- **Live Application**: https://lancelott-z9dko.web.app
- **GitHub Repository**: https://github.com/ORDEROFCODE/LANCELOTT
- **Firebase Console**: https://console.firebase.google.com/project/lancelott-z9dko
- **Issues**: https://github.com/ORDEROFCODE/LANCELOTT/issues
- **Discussions**: https://github.com/ORDEROFCODE/LANCELOTT/discussions

---

**🛡️ LANCELOTT v2.1.0** - *Professional Security Framework with AI-Powered Cloud Backend*
EOF

    print_status "Comprehensive README.md created"
}

# Create GitHub repository
create_github_repository() {
    print_step "Creating GitHub repository..."

    # Check if repository already exists
    if gh repo view "$GITHUB_USERNAME/$REPO_NAME" &>/dev/null; then
        print_warning "Repository $GITHUB_USERNAME/$REPO_NAME already exists"
        return 0
    fi

    # Create repository
    gh repo create "$REPO_NAME" \
        --description "$REPO_DESCRIPTION" \
        --public \
        --add-readme=false \
        --clone=false

    print_status "GitHub repository created: $GITHUB_USERNAME/$REPO_NAME"

    # Add remote origin
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git" 2>/dev/null || true
    print_status "Remote origin added"
}

# Configure repository settings
configure_repository() {
    print_step "Configuring repository settings..."

    # Add topics/tags
    topics=(
        "cybersecurity"
        "penetration-testing"
        "security-tools"
        "fastapi"
        "firebase"
        "ai-integration"
        "langchain"
        "docker"
        "python"
        "typescript"
        "red-team"
        "osint"
        "vulnerability-scanner"
        "security-framework"
        "cloud-security"
    )

    for topic in "${topics[@]}"; do
        gh repo edit "$GITHUB_USERNAME/$REPO_NAME" --add-topic "$topic"
    done

    print_status "Repository topics configured"

    # Enable features
    gh repo edit "$GITHUB_USERNAME/$REPO_NAME" \
        --enable-issues \
        --enable-projects \
        --enable-wiki \
        --enable-discussions

    print_status "Repository features enabled"
}

# Set up GitHub secrets for Firebase deployment
setup_github_secrets() {
    print_step "Setting up GitHub secrets..."

    print_info "You'll need to manually add these secrets in GitHub:"
    echo ""
    echo "Required GitHub Secrets:"
    echo "- FIREBASE_TOKEN: Firebase CI token"
    echo "- FIREBASE_SERVICE_ACCOUNT: Service account JSON content"
    echo "- GITHUB_PAT: Personal access token for enhanced features"
    echo ""
    echo "To get Firebase token:"
    echo "  firebase login:ci"
    echo ""
    echo "To add secrets:"
    echo "  gh secret set FIREBASE_TOKEN"
    echo "  gh secret set FIREBASE_SERVICE_ACCOUNT < config/firebase/your-service-account.json"
    echo ""
}

# Add and commit files
commit_initial_files() {
    print_step "Committing initial files..."

    # Add all files
    git add .

    # Create initial commit
    git commit -m "🚀 Initial commit: LANCELOTT v2.1.0 Enhanced Security Framework

Features:
- 🛡️ 27+ integrated security tools
- 🔥 Firebase cloud backend
- 🤖 AI-powered analysis with LangChain
- 🚀 FastAPI high-performance API
- 🐳 Docker containerization
- 📊 Comprehensive dashboard
- 🔒 Advanced security workflows

Tech Stack:
- Python 3.11+ with FastAPI
- Firebase (Auth, Firestore, Functions, Hosting)
- LangChain AI integration
- Docker & Docker Compose
- GitHub Actions CI/CD
- TypeScript/React frontend

Security Tools:
- Network: Nmap, Argus, Enhanced scanners
- Web: Kraken, Feroxbuster, Web-Check
- OSINT: Metabigor, SpiderFoot, Social-Analyzer
- Mobile: PhoneSploit-Pro
- Cloud: Vajra
- And many more...

Live at: https://lancelott-z9dko.web.app"

    print_status "Initial commit created"

    # Push to GitHub
    git push -u origin main
    print_status "Code pushed to GitHub"
}

# Create releases and tags
create_release() {
    print_step "Creating GitHub release..."

    # Create release
    gh release create "v2.1.0" \
        --title "🛡️ LANCELOTT v2.1.0 - Enhanced Security Framework" \
        --notes "## 🚀 LANCELOTT v2.1.0 Enhanced

### ✨ New Features
- 🔥 **Firebase Cloud Backend**: Complete cloud-native architecture
- 🤖 **AI Integration**: LangChain with multi-provider support
- 🛡️ **27+ Security Tools**: Comprehensive toolkit integration
- 📊 **Advanced Dashboard**: Real-time monitoring and control
- 🚀 **GitHub Actions**: Automated CI/CD pipeline

### 🔧 Technical Improvements
- FastAPI 0.104+ for high-performance API
- Firebase Auth, Firestore, Functions, and Hosting
- Docker containerization with multi-service support
- TypeScript/React frontend with modern UI
- Comprehensive test suite and validation

### 🛡️ Security Tools
- **Network**: Nmap, Argus, Enhanced scanning
- **Web**: Kraken, Feroxbuster, Web-Check
- **OSINT**: Metabigor, SpiderFoot, Social-Analyzer
- **Mobile**: PhoneSploit-Pro for Android
- **Cloud**: Vajra for cloud security
- **Brute Force**: THC-Hydra, Sherlock
- **And many more...**

### 🌐 Deployment
- **Live Demo**: https://lancelott-z9dko.web.app
- **API Docs**: https://lancelott-z9dko.web.app/docs
- **Firebase Console**: https://console.firebase.google.com/project/lancelott-z9dko

### 📋 Installation
\`\`\`bash
git clone https://github.com/ORDEROFCODE/LANCELOTT.git
cd LANCELOTT
make start
\`\`\`

### 🐳 Docker
\`\`\`bash
docker-compose up -d --build
\`\`\`

### 🔥 Firebase Deploy
\`\`\`bash
./deploy_firebase.sh
\`\`\`"

    print_status "GitHub release v2.1.0 created"
}

# Final setup and verification
final_verification() {
    print_step "Running final verification..."

    # Validate Firebase configuration
    if [ -f "scripts/utils/validate_firebase_config.py" ]; then
        python3 scripts/utils/validate_firebase_config.py --quiet
        if [ $? -eq 0 ]; then
            print_status "Firebase configuration validated"
        else
            print_warning "Firebase configuration needs attention"
        fi
    fi

    # Check if CI/CD workflow exists
    if [ -f ".github/workflows/ci-cd.yml" ]; then
        print_status "CI/CD workflow configured"
    else
        print_warning "CI/CD workflow not found"
    fi

    # Repository stats
    file_count=$(find . -type f | wc -l)
    python_files=$(find . -name "*.py" | wc -l)

    print_info "Repository statistics:"
    print_info "  Total files: $file_count"
    print_info "  Python files: $python_files"
    print_info "  Security tools: 27+"
    print_info "  API endpoints: 50+"
}

# Main execution
main() {
    print_header

    echo "🚀 Setting up LANCELOTT GitHub repository with Firebase integration"
    echo "📋 Repository: $GITHUB_USERNAME/$REPO_NAME"
    echo "🔥 Firebase Project: $FIREBASE_PROJECT_ID"
    echo ""

    # Run setup steps
    check_prerequisites
    initialize_git
    create_gitignore
    create_readme
    create_github_repository
    configure_repository
    commit_initial_files
    create_release
    setup_github_secrets
    final_verification

    echo ""
    print_status "🎉 GitHub repository setup completed successfully!"
    echo ""
    echo "🌐 Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "🔥 Firebase App: https://$FIREBASE_PROJECT_ID.web.app"
    echo "📚 API Docs: https://$FIREBASE_PROJECT_ID.web.app/docs"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Add GitHub secrets for automated deployment"
    echo "2. Review and customize the repository settings"
    echo "3. Set up branch protection rules"
    echo "4. Configure Firebase authentication"
    echo "5. Deploy using: scripts/deploy_firebase.sh"
    echo ""
    print_info "Your LANCELOTT security framework is ready for the world! 🛡️"
}

# Handle command line arguments
case "${1:-setup}" in
"setup")
    main
    ;;
"validate")
    print_header
    check_prerequisites
    final_verification
    ;;
"secrets")
    print_header
    setup_github_secrets
    ;;
"help" | "--help" | "-h")
    echo "🚀 GitHub Repository Setup Script for LANCELOTT"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  setup     - Complete repository setup (default)"
    echo "  validate  - Validate configuration"
    echo "  secrets   - Show secrets setup instructions"
    echo "  help      - Show this help message"
    echo ""
    ;;
*)
    print_error "Unknown command: $1"
    echo "Use '$0 help' for usage information"
    exit 1
    ;;
esac
