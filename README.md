![LANCELOTT Banner](media/project-lancelott.png)

# 🛡️ LANCELOTT v2.1.0 Enhanced - AI-Powered Security Framework 🐺

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org)
[![Go](https://img.shields.io/badge/Go-1.21+-blue.svg)](https://golang.org)
[![Firebase](https://img.shields.io/badge/Firebase-Integrated-orange.svg)](https://firebase.google.com)
[![LangChain](https://img.shields.io/badge/LangChain-AI_Powered-purple.svg)](https://langchain.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

> **A comprehensive, AI-enhanced cybersecurity framework with 27+ integrated security tools, Firebase cloud backend, LangChain AI integration, MCP protocol support, multi-provider AI compatibility, advanced obfuscation capabilities, and unified workflow orchestration.**

## 🚀 **LATEST INTEGRATIONS - PRODUCTION READY**

### 🔥 **Firebase Cloud Integration - COMPLETE**

- **Live Dashboard**: <https://studio--lancelott-z9dko.us-central1.hosted.app/>
- **Real-time Authentication**: Firebase Auth with JWT integration
- **Cloud Database**: Firestore for scan results and user data
- **File Storage**: Cloud Storage for reports and uploads
- **Admin Panel**: Role-based access control and user management

### 🤖 **LangChain AI Framework - COMPLETE**

- **AI-Powered Security Analysis**: Intelligent vulnerability assessment
- **Multi-Provider Support**: OpenAI, Anthropic, Azure AI integration
- **Security Chat**: Interactive AI consultation for threat analysis
- **Automated Reports**: AI-enhanced report generation
- **Cross-Language AI**: Python + JavaScript AI workflows

### 📊 **Framework Status - PRODUCTION READY**

- ✅ **27+ Security Tools** integrated and tested
- ✅ **Firebase Backend** fully operational
- ✅ **AI Integration** with LangChain frameworks
- ✅ **N8N Workflows** moved to proper `/workflows/` directory
- ✅ **Project Organization** completed and validated
- ✅ **Comprehensive Testing** suite implemented

## 🔥 **Firebase Cloud Integration**

### **Live Firebase Dashboard**

**Access URL**: <https://studio--lancelott-z9dko.us-central1.hosted.app/>

![LANCELOTT Firebase Dashboard](media/lancelott-dashboard.png)

*Live Firebase Dashboard featuring real-time analytics, user management, scan monitoring, and comprehensive security reporting*

### **Authentication System**

```javascript
// Firebase Configuration
const firebaseConfig = {
  apiKey: "AIzaSyD0RkGeip2f2rc29YSMHy5w6YeD-5VgriA",
  authDomain: "lancelott-z9dko.firebaseapp.com",
  projectId: "lancelott-z9dko",
  storageBucket: "lancelott-z9dko.firebasestorage.app",
  messagingSenderId: "681869309450",
  appId: "1:681869309450:web:5ead0e530b282864d6d1f3"
};
```

### **Firebase API Endpoints**

```bash
# Authentication
POST /api/v1/firebase/auth/verify     # Verify Firebase tokens
GET  /api/v1/firebase/auth/me         # Get current user info

# User Management
GET  /api/v1/firebase/users/profile   # Get user profile
PUT  /api/v1/firebase/users/profile   # Update user profile

# Scan Management
POST /api/v1/firebase/scans           # Create scan results
GET  /api/v1/firebase/scans           # Get user scans
GET  /api/v1/firebase/scans/{id}      # Get specific scan
PUT  /api/v1/firebase/scans/{id}/status # Update scan status

# Dashboard & Admin
GET  /api/v1/firebase/dashboard       # Redirect to Firebase dashboard
GET  /api/v1/firebase/dashboard/stats # Get dashboard statistics
GET  /api/v1/firebase/config          # Get Firebase client config
GET  /api/v1/firebase/health          # Firebase health check
```

### **Firebase Features**

- ✅ **Real-time Authentication**: Firebase Auth with JWT validation
- ✅ **Cloud Database**: Firestore for scan results and user data
- ✅ **File Storage**: Cloud Storage for reports and uploads
- ✅ **Role-based Access**: Admin and user permission systems
- ✅ **Live Dashboard**: Web-based management interface
- ✅ **Security Rules**: Firestore and Storage security implementation

## 🤖 **LangChain AI Integration**

### **AI-Powered Security Analysis**

```bash
# LangChain Python API
POST /api/v1/ai/langchain/analyze      # Security data analysis
POST /api/v1/ai/langchain/chat         # Interactive security chat
POST /api/v1/ai/langchain/generate-report # AI report generation
GET  /api/v1/ai/langchain/providers    # Available AI providers

# LangChain.js API
POST /api/v1/ai/langchainjs/execute-script # JavaScript execution
POST /api/v1/ai/langchainjs/execute-chain  # Chain processing
POST /api/v1/ai/langchainjs/execute-agent  # Agent execution
```

### **AI Framework Features**

- ✅ **Multi-Provider Support**: OpenAI, Anthropic, Azure AI integration
- ✅ **Intelligent Analysis**: AI-powered vulnerability assessment
- ✅ **Security Chat**: Interactive AI consultation for threats
- ✅ **Automated Reports**: Natural language security reports
- ✅ **Cross-Language**: Python + JavaScript AI workflows
- ✅ **Real-time Intelligence**: Live threat analysis and recommendations

## 📊 **Project Status - ALL INTEGRATIONS COMPLETE**

## Recent Changes
<!-- QODER:RECENT_CHANGES:BEGIN -->
- 2025-08-27 — **Integration:** UI-TARS Desktop & Agent-TARS CLI Integration Complete → `docs/integration/UI_TARS_INTEGRATION_COMPLETE.md`
  Impact: Adds advanced GUI automation capabilities with AI-powered interface understanding, entry points callable from root (ui-tars, agent-tars), and comprehensive API integration.
- 2025-08-27 — **Integration:** Model Context Protocol (MCP) Servers Integration Complete → `docs/guides/MCP_INTEGRATION_FINAL_SUMMARY.md`
  Impact: Integrates Redis, Chart, File, and PostgreSQL MCP servers with Agent-TARS, resolves Redis URL parsing error, and enables full tool access through standardized protocols.
- 2025-08-27 — **Organization:** Project Organization Complete → `docs/organization/PROJECT_ORGANIZATION_COMPLETE.md`
  Impact: Complete project reorganization with scripts moved to /scripts/, tests to /tests/, requirements consolidated, and all references updated.
<!-- QODER:RECENT_CHANGES:END -->

### ✅ **Completed Integrations**

1. **Firebase Cloud Backend** - Authentication, database, storage, dashboard
2. **LangChain AI Framework** - Python & JavaScript AI integration
3. **Crush + CliWrap Integration** - Enhanced command execution
4. **N8N Workflow Automation** - Moved to `/workflows/` directory
5. **Project Organization** - Clean directory structure implemented
6. **Comprehensive Testing** - Full test suite with validation

### 📁 **Directory Organization**

```
LANCELOTT/
├── 🔥 config/firebase/           # Firebase service account & config
├── 🤖 integrations/frameworks/ # LangChain AI integration
├── 🔧 workflows/               # N8N workflow automation (moved)
├── 📚 docs/                   # All documentation organized
├── 🧪 tests/                  # Comprehensive test suite
├── 🔌 api/routes/             # 32+ API routers including Firebase & AI
├── 🛠️ tools/                  # 27+ security tools
└── 📊 build/scripts/         # Setup and deployment scripts
```

### 🚀 **Ready for Production**

- ✅ **All modules implemented and tested**
- ✅ **Firebase integration complete**
- ✅ **AI framework operational**
- ✅ **Environment configuration finalized**
- ✅ **API endpoints fully functional**
- ✅ **Security features implemented**
- ✅ **Documentation comprehensive**

## 🚀 Quick Start

### 🎯 Super Quick Start (Recommended)

```bash
# Clone and start
git clone https://github.com/ORDEROFCODE/LANCELOTT.git
cd LANCELOTT

# Smart auto-start (detects environment and installs dependencies)
python start.py

# Or use the CLI interface
python lancelott.py start
```

### 🔥 **Firebase Integration Setup**

```bash
# 1. Verify Firebase configuration
python scripts/utils/verify_firebase_config.py

# 2. Setup Firebase CLI (if needed)
./build/scripts/setup_firebase_cli.sh

# 3. Login to Firebase
firebase login
firebase use lancelott-z9dko

# 4. Deploy security rules
firebase deploy --only firestore:rules,storage:rules
```

### 🤖 **AI Integration Setup**

```bash
# 1. Setup LangChain integration
./build/scripts/setup_langchain_integration.sh

# 2. Configure AI API keys in .env
cp .env.example .env
# Add your API keys:
# OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 3. Test AI integration
python examples/langchain/security_analysis_example.py
```

### 📊 **Access Points After Setup**

- **Main API**: <http://localhost:7777>
- **Interactive Docs**: <http://localhost:7777/docs>
- **Firebase Dashboard**: <https://studio--lancelott-z9dko.us-central1.hosted.app/>
- **N8N Workflows**: <http://localhost:5678>
- **AI Chat Interface**: <http://localhost:7777/api/v1/ai/langchain/chat>

### 📋 Manual Setup

```bash
# 1. Setup environment
pip install -r requirements.txt

# 2. Initialize configuration
python config/lancelott_config.py summary

# 3. Build tools
python build/build_manager.py build

# 4. Start the framework
python app.py
```

### 🐳 Docker Deployment

```bash
# Quick Docker start
docker-compose up -d --build

# Access the main API
curl http://localhost:7777/api/v1/health
```

## 🏗️ New Framework Architecture

```
LANCELOTT/
├── 🛠️ tools/                    # All 17 security tools organized
│   ├── Argus/                  # Web application scanning
│   ├── Kraken/                 # Multi-tool security framework
│   ├── Metabigor/              # Intelligence gathering
│   ├── Osmedeus/               # Automated reconnaissance
│   ├── Spiderfoot/             # OSINT automation
│   ├── Social-Analyzer/        # Social media analysis
│   ├── SHERLOCK/               # Username investigation
│   ├── PhoneSploit-Pro/        # Android exploitation
│   ├── RedTeam-ToolKit/        # Red team utilities
│   ├── Storm-Breaker/          # Social engineering
│   ├── THC-Hydra/              # Password attacks
│   ├── Vajra/                  # UI testing automation
│   ├── Web-Check/              # Website analysis
│   ├── Webstor/                # Web storage analysis
│   ├── UI-TARS/                # Advanced UI automation
│   ├── dismap/                 # Asset discovery
│   ├── Metasploit-Framework/   # Penetration testing suite
│   └── security/               # Security enhancement tools
│       └── vanguard/           # Obfuscation & protection
│           ├── BOAZ/           # Shellcode obfuscation
│           ├── BitMono/        # .NET binary protection
│           ├── FakeHTTP/       # HTTP protocol obfuscation
│           ├── Hyperion/       # Binary encryption
│           ├── de4py/          # Python deobfuscation
│           ├── javascript-obfuscator/ # JS obfuscation
│           ├── pyarmor/        # Python protection
│           ├── skidfuscator-java-obfuscator/ # Java obfuscation
│           └── utls/           # TLS fingerprint obfuscation
├── 🔧 build/                   # Unified build management
│   ├── build_manager.py        # Multi-language build system
│   ├── scripts/                # Build automation
│   └── docker/                 # Container configurations
├── 🔌 integrations/            # Tool integration system
│   ├── integration_manager.py  # Unified tool management
│   ├── n8n_integration.py      # Workflow automation
│   ├── ai/                     # AI integration components
│   │   ├── supergateway/       # MCP protocol gateway
│   │   └── supercompat/        # AI compatibility layer
│   └── tools/                  # Tool-specific wrappers
├── 📊 status/                  # Monitoring and alerting
│   ├── status_monitor.py       # Real-time monitoring
│   └── reporting/              # Status reports
├── ⚙️ config/                  # Centralized configuration
│   ├── lancelott_config.py     # Unified config manager
│   ├── lancelott.yaml          # Main configuration
│   └── monitoring.json         # Monitoring settings
├── 🌐 api/                     # Enhanced FastAPI application
│   ├── routes/                 # Tool-specific routes
│   └── advanced_routes.py      # Multi-tool orchestration
├── 📚 docs/                    # Comprehensive documentation
├── 🚀 app.py                   # Enhanced main application
├── 🖥️ lancelott.py             # Unified CLI interface
└── ⚡ start.py                 # Smart startup script
```

## 🛠️ Integrated Security Tools (17+)

### 🔍 **Network & Infrastructure**

- **Nmap** - Network discovery and security auditing
- **Dismap** - Asset discovery and service fingerprinting
- **Osmedeus** - Automated reconnaissance framework
- **Metabigor** - Intelligence gathering and OSINT

### 🌐 **Web Application Testing**

- **Argus** - Comprehensive web application scanner
- **Kraken** - Multi-tool security testing framework
- **Web-Check** - Website security analysis
- **Webstor** - Web storage security analysis

### 🕵️ **OSINT & Intelligence**

- **SpiderFoot** - Automated OSINT data collection
- **Social-Analyzer** - Social media analysis
- **SHERLOCK** - Username investigation across platforms
- **Storm-Breaker** - Social engineering toolkit

### ⚔️ **Penetration Testing**

- **Metasploit-Framework** - Complete penetration testing suite
- **THC-Hydra** - Password attack tool
- **RedTeam-ToolKit** - Comprehensive red team utilities
- **PhoneSploit-Pro** - Android device exploitation

### 🤖 **AI Integration & Automation**

- **SuperGateway** - MCP (Model Context Protocol) gateway for AI interactions
- **SuperCompat** - Multi-provider AI compatibility layer
- **UI-TARS** - Advanced UI automation and testing
- **Vajra** - Cloud security assessment

### 🛡️ **Security Enhancement (Vanguard)**

- **PyArmor** - Professional Python code protection
- **JavaScript Obfuscator** - Advanced JavaScript obfuscation
- **Skidfuscator** - Java bytecode obfuscation framework
- **BOAZ** - Advanced shellcode and binary obfuscation
- **Hyperion** - Binary encryption and protection
- **uTLS** - TLS fingerprint obfuscation library
- **FakeHTTP** - HTTP protocol obfuscation
- **BitMono** - .NET binary analysis and obfuscation
- **de4py** - Python deobfuscation and analysis

## 🎯 Key Features

### 🔧 **Unified Management**

```bash
# Build all tools with one command
python build/build_manager.py build

# Check status of all components
python status/status_monitor.py check

# Initialize all integrations
python integrations/integration_manager.py init
```

## 🎆 **Integration Benefits**

### 🔥 **Firebase Cloud Advantages**

- **Scalable Infrastructure**: Google Cloud backend with automatic scaling
- **Real-time Data**: Live scan results and user activity synchronization
- **Professional Dashboard**: Web-based management interface
- **Enterprise Security**: Role-based access control and audit logging
- **Global CDN**: Fast content delivery worldwide
- **Backup & Recovery**: Automatic data redundancy and backup

### 🤖 **AI-Enhanced Security**

- **Intelligent Analysis**: AI-powered vulnerability assessment and threat detection
- **Natural Language**: Chat with AI about security findings and recommendations
- **Automated Reports**: Generate comprehensive security reports with AI insights
- **Multi-Provider**: Leverage different AI models for diverse analysis approaches
- **Continuous Learning**: AI models adapt to new threats and attack patterns
- **Cost Optimization**: Use different AI providers based on task complexity

### 🛡️ **Unified Security Platform**

- **Single API**: All 27+ security tools accessible through unified REST API
- **Consistent Auth**: One authentication system across all tools and services
- **Centralized Logs**: All security activities logged and monitored centrally
- **Workflow Automation**: N8N integration for automated security workflows
- **Cross-Platform**: Python, Go, Node.js, and web technologies integrated
- **Container Ready**: Full Docker support for easy deployment

### 🔄 **Workflow Automation**

```bash
# Setup n8n workflows
python integrations/n8n_integration.py setup

# Start workflow automation
python integrations/n8n_integration.py start --tunnel
```

### 📊 **Advanced Orchestration**

```python
# Multi-tool scan orchestration
POST /api/v1/advanced/orchestrate/scan
{
    "target": "example.com",
    "scan_type": "comprehensive",
    "parallel": true
}
```

### ⚙️ **Configuration Management**

```bash
# Validate configuration
python config/lancelott_config.py validate

# Generate environment file
python config/lancelott_config.py env

# Show configuration summary
python config/lancelott_config.py summary
```

## 🌐 API Endpoints

### 🏠 **Core Endpoints**

- `GET /` - Enhanced dashboard with real-time stats
- `GET /api/v1/health` - Comprehensive health check
- `GET /api/v1/status/dashboard` - Real-time status dashboard
- `GET /docs` - Interactive API documentation

### 🛠️ **Tool Endpoints**

- `/api/v1/tools/nmap/` - Nmap network scanning
- `/api/v1/tools/argus/` - Web application testing
- `/api/v1/tools/spiderfoot/` - OSINT automation
- `/api/v1/tools/sherlock/` - Username investigation
- `/api/v1/tools/web-check/` - Website analysis
- *...and 12 more tool endpoints*

### 🔄 **Advanced Features**

- `/api/v1/advanced/orchestrate/scan` - Multi-tool orchestration
- `/api/v1/workflows/n8n/` - Workflow automation
- `/api/v1/integrations/status` - Integration management
- `/api/v1/advanced/health/comprehensive` - Full system health

### 🤖 **AI Integration**

- `/api/v1/integrations/supergateway/` - MCP gateway management
- `/api/v1/integrations/supercompat/` - AI compatibility layer

### 🛡️ **Security Enhancement**

- `/api/v1/security/vanguard/` - Obfuscation tools management
- `/api/v1/security/vanguard/obfuscate` - File obfuscation
- `/api/v1/security/vanguard/upload-and-obfuscate` - Upload & obfuscate

## 🔄 Workflow Automation with n8n

LANCELOTT includes predefined n8n workflows for:

### 🔍 **Reconnaissance Workflow**

- Nmap port scanning
- SpiderFoot OSINT gathering
- Automated report generation

### 🔒 **Vulnerability Assessment**

- Argus web scanning
- Nmap vulnerability scripts
- Result correlation

### 👥 **Social Engineering**

- SHERLOCK username investigation
- Social-Analyzer profiling
- Intelligence consolidation

```bash
# Setup all workflows
curl -X POST http://localhost:7777/api/v1/workflows/n8n/setup

# Trigger reconnaissance workflow
curl -X POST http://localhost:5678/webhook/recon \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com"}'
```

## 📊 Monitoring & Status

### 🎯 **Real-time Monitoring**

```bash
# Start continuous monitoring
python status/status_monitor.py monitor

# Generate status report
python status/status_monitor.py report --format json

# Health check all tools
curl http://localhost:7777/api/v1/integrations/status
```

### 📈 **Dashboard Access**

- **Main Dashboard:** <http://localhost:7777>
- **Status Dashboard:** <http://localhost:7777/api/v1/status/dashboard>
- **n8n Workflows:** <http://localhost:5678>
- **API Documentation:** <http://localhost:7777/docs>

## 🔐 Security & Authentication

### 🔑 **API Authentication**

```bash
# Get access token
POST /api/v1/auth/token
{
    "username": "admin",
    "password": "your_password"
}

# Use token in requests
curl -H "Authorization: Bearer <token>" \
     http://localhost:7777/api/v1/tools/nmap/scan
```

### 🛡️ **Security Features**

- JWT-based authentication
- Rate limiting
- CORS protection
- Input validation
- Audit logging

## 🔧 CLI Management

LANCELOTT includes a comprehensive CLI for all operations:

### 🚀 **Server Management**

```bash
# Start server
lancelott start --port 7777 --workers 4

# Start with auto-reload
lancelott start --reload
```

### 🔨 **Build Management**

```bash
# Build all tools
lancelott build

# Build specific tool
lancelott build --target argus

# Clean and rebuild
lancelott build --clean
```

### 📊 **Status & Monitoring**

```bash
# Check system status
lancelott status

# Start monitoring
lancelott monitor --duration 3600

# Generate report
lancelott status --format json --save report.json
```

### 🔄 **Workflow Management**

```bash
# Setup n8n workflows
lancelott workflows setup

# Start n8n with tunnel
lancelott workflows start --tunnel

# Check workflow health
lancelott workflows health
```

### 🔌 **Integration Management**

```bash
# Initialize all integrations
lancelott integrations init

# Check integration status
lancelott integrations status

# Test specific tool
lancelott integrations test argus
```

### ⚙️ **Configuration**

```bash
# Show configuration summary
lancelott config summary

# Validate configuration
lancelott config validate

# Generate environment file
lancelott config env --output .env.production
```

### 🛠️ **Tool Management**

```bash
# List all tools
lancelott tools list

# Enable/disable tools
lancelott tools enable sherlock
lancelott tools disable phonesploit
```

## 📋 Port Assignments

| Service | Port | Description |
|---------|------|-------------|
| **Main API** | 7777 | LANCELOTT FastAPI server |
| **n8n** | 5678 | Workflow automation |
| **SuperGateway** | 3000 | MCP protocol gateway |
| **SuperCompat** | 3001 | AI compatibility layer |
| **Nmap** | 7001 | Network scanning |
| **Argus** | 7002 | Web application testing |
| **Kraken** | 7003 | Multi-tool framework |
| **Metabigor** | 7004 | Intelligence gathering |
| **Osmedeus** | 7005 | Automated reconnaissance |
| **SpiderFoot** | 7006 | OSINT automation |
| **Social-Analyzer** | 7007 | Social media analysis |
| **PhoneSploit-Pro** | 7008 | Android exploitation |
| **Vajra** | 7009 | UI testing |
| **Storm-Breaker** | 7010 | Social engineering |
| **Dismap** | 7011 | Asset discovery |
| **THC-Hydra** | 7012 | Password attacks |
| **Webstor** | 7013 | Web storage analysis |
| **SHERLOCK** | 7014 | Username investigation |
| **RedTeam-ToolKit** | 7015 | Red team utilities |
| **UI-TARS** | 7016 | Advanced UI automation |
| **Web-Check** | 7017 | Website analysis |

The API uses JWT-based authentication. Default credentials:

- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Change these credentials in production!**

### Getting an Access Token

```bash
curl -X POST "http://localhost:7777/api/v1/auth/token" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
```

### Using the Token

```bash
curl -X GET "http://localhost:7777/api/v1/tools" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🌐 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/api/v1/health` | GET | Health check |
| `/api/v1/tools` | GET | List all tools and their status |
| `/api/v1/tools/{tool_name}/status` | GET | Get specific tool status |

### SuperTools API Endpoints

#### SuperGateway APIs (`/api/v1/supergateway/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Service status |
| `/gateways` | GET | List active gateways |
| `/gateway/{id}` | GET/DELETE | Gateway management |
| `/gateway/stdio-to-sse` | POST | Create stdio→SSE gateway |
| `/gateway/sse-to-stdio` | POST | Create SSE→stdio gateway |
| `/examples` | GET | Usage examples |

#### SuperCompat APIs (`/api/v1/supercompat/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Service status |
| `/providers` | GET | List supported AI providers |
| `/sessions` | GET/DELETE | Session management |
| `/session` | POST/GET/DELETE | Create/manage AI sessions |
| `/completion` | POST | Execute AI completions |
| `/examples` | GET | Usage examples |

### SuperTools Usage Examples

#### 1. Create MCP Gateway for Filesystem Access

```bash
curl -X POST "http://localhost:7777/api/v1/supergateway/gateway/stdio-to-sse" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "gateway_id": "filesystem-gateway",
    "stdio_command": "npx @modelcontextprotocol/server-filesystem ./data",
    "port": 8001,
    "cors": true
  }'
```

#### 2. Create AI Provider Session

```bash
curl -X POST "http://localhost:7777/api/v1/supercompat/session" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "security-analysis",
    "provider": "openai",
    "api_key": "your-api-key",
    "model": "gpt-4"
  }'
```

#### 3. Execute AI Security Analysis

```bash
curl -X POST "http://localhost:7777/api/v1/supercompat/completion" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "security-analysis",
    "messages": [
      {"role": "system", "content": "You are a cybersecurity expert."},
      {"role": "user", "content": "Analyze this vulnerability report: [report data]"}
    ],
    "temperature": 0.7
  }'
```

## 🏗️ Project Structure

```
CERBERUS-FANGS/LANCELOTT/
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── quick_setup.sh             # Automated setup script
├── activate_env.sh            # Environment activation script
├── open_vscode.sh             # VS Code launcher script
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── .env.example              # Environment template
├── api/                      # API modules
│   ├── routes/              # API route definitions
│   ├── models.py            # Pydantic models
│   └── auth.py              # Authentication logic
├── core/                    # Core functionality
│   ├── config.py            # Configuration settings
│   ├── logging.py           # Logging configuration
│   ├── tool_manager.py      # Tool management logic
│   ├── supergateway_manager.py  # SuperGateway wrapper
│   └── supercompat_manager.py   # SuperCompat wrapper
├── tests/                   # Test suite (NEW)
│   ├── conftest.py          # Test configuration
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── api/                 # API tests
├── static/                  # Static files
├── logs/                    # Application logs
├── reports/                 # Generated reports
├── uploads/                 # File uploads
├── SuperGateway/            # MCP gateway tool (NEW)
│   ├── dist/               # Built TypeScript files
│   └── src/                # Source code
├── SuperCompat/             # AI compatibility layer (NEW)
│   └── packages/supercompat/
├── .vscode/                 # VS Code configuration (NEW)
│   ├── settings.json        # Workspace settings
│   ├── extensions.json      # Recommended extensions
│   └── tasks.json          # Build tasks
├── cerberus-fangs.code-workspace  # VS Code workspace (NEW)
└── [Traditional Security Tools]/   # Individual tool directories
```

## 🔧 Configuration

Key configuration options in `.env`:

```bash
# Application
DEBUG=false
HOST=0.0.0.0
PORT=7777

# Security
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./cerberus_fangs.db

# SuperTools Paths
SUPERGATEWAY_PATH=./SuperGateway
SUPERCOMPAT_PATH=./SuperCompat

# Node.js Environment
NODE_ENV=production
```

## 🧪 Testing

The project includes a comprehensive test suite in the `tests/` directory:

### Running Tests

```bash
# All tests
python -m pytest tests/

# Specific categories
python -m pytest tests/unit/        # Unit tests
python -m pytest tests/integration/ # Integration tests
python -m pytest tests/api/         # API tests

# With coverage
python -m pytest tests/ --cov=core --cov=api
```

### Test Structure

```
tests/
├── conftest.py                    # Test configuration and fixtures
├── unit/                         # Unit tests for components
│   ├── test_supertools.py        # SuperGateway & SuperCompat tests
│   └── test_setup.py             # Setup and configuration tests
├── integration/                  # Integration tests
│   └── test_simple_integration.py # Basic integration tests
└── api/                          # API-specific tests
    └── test_*.py                 # Various API endpoint tests
```

## 💻 Development Environment

### VS Code Setup (Recommended)

The project includes comprehensive VS Code configuration:

#### Features

- **Auto Virtual Environment**: Automatically activates `.venv` on startup
- **Multi-Language Support**: Python, TypeScript, JSON, YAML, Markdown
- **Build Tasks**: One-click building of all components
- **Debug Configurations**: Ready-to-use debugging for FastAPI
- **Recommended Extensions**: Complete development toolkit
- **Integrated Terminal**: Custom profiles with environment setup

#### Quick Start

```bash
# Automated VS Code setup
./open_vscode.sh

# Manual activation
source activate_env.sh
code cerberus-fangs.code-workspace
```

#### Available Tasks (Ctrl+Shift+P → "Tasks: Run Task")

- **Build All Tools** - Complete build of Python + Node.js components
- **Start CERBERUS FastAPI Server** - Launch main API server
- **Build SuperGateway** - Build MCP gateway tool
- **Build SuperCompat** - Build AI compatibility layer
- **Run Status Check** - Check all tool statuses

## 📊 Monitoring and Logging

- **Application Logs:** `./logs/cerberus_fangs_YYYYMMDD.log`
- **Tool-Specific Logs:** `./logs/{tool_name}_YYYYMMDD.log`
- **Error Logs:** `./logs/cerberus_fangs_YYYYMMDD_errors.log`
- **Health Monitoring:** `/api/v1/health` endpoint
- **SuperTools Monitoring:** Process-level monitoring for Node.js components

## 🐳 Docker Support

### Docker Compose (Recommended)

```yaml
version: "3.8"
services:
  cerberus-fangs:
    build: .
    ports:
      - "7777:7777"
    environment:
      - DEBUG=false
      - SECRET_KEY=your-production-secret
    volumes:
      - ./logs:/app/logs
      - ./reports:/app/reports
```

### Production Deployment

For production deployment, consider:

1. **Use HTTPS/TLS encryption**
2. **Configure proper firewall rules**
3. **Set up reverse proxy (Nginx)**
4. **Use production database (PostgreSQL)**
5. **Implement rate limiting**
6. **Set up monitoring and alerting**
7. **Configure proper Node.js process management**
8. **Set up AI provider API key management**

## 🔒 Security Considerations

⚠️ **IMPORTANT SECURITY NOTES:**

### General Security

1. **Change default credentials immediately**
2. **Use strong secret keys in production**
3. **Implement proper network segmentation**
4. **Only run scans on authorized targets**
5. **Use HTTPS in production**
6. **Regularly update all dependencies**
7. **Implement proper access controls**

### SuperTools Security

8. **Secure AI provider API keys** - Store in environment variables, not code
9. **Monitor AI usage** - Track API calls and costs
10. **Gateway security** - Implement proper CORS and authentication for MCP gateways
11. **Process isolation** - SuperTools run in isolated Node.js processes
12. **Session management** - AI provider sessions are memory-only, not persistent

## 🌟 Integration Benefits

### Unified Security Platform

- All 14+ security tools accessible through single API
- Consistent authentication and logging across all tools
- Centralized monitoring and management

### AI-Enhanced Security Analysis

- Integrate AI analysis into traditional security workflows
- Multiple AI providers for diverse analysis approaches
- Automated threat intelligence and report generation
- Natural language querying of security data

### Modern Protocol Support

- MCP protocol enables AI agent interactions with security tools
- Bridge legacy command-line tools with modern web interfaces
- Enable remote access and cloud-based security operations

### Developer Experience

- RESTful APIs for easy integration
- Comprehensive documentation with interactive examples
- Python wrappers for complex Node.js tools
- VS Code integration for optimal development workflow

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable (use the `tests/` directory)
5. Update README.md with any new features or changes
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See individual tool directories for their specific licenses.

## ⚠️ Legal Disclaimer

This toolkit is intended for authorized security testing and educational purposes only. Users are responsible for ensuring they have proper authorization before conducting any security assessments. The developers assume no liability for misuse of this software.

## 🆘 Support

- **Documentation:** <http://localhost:7777/docs>
- **Health Check:** <http://localhost:7777/api/v1/health>
- **Status Check:** `python status.py`
- **Logs:** Check `./logs/` directory for detailed information
- **Tests:** Run `python -m pytest tests/` for verification

## 🎯 Quick Commands

```bash
# Environment setup
source activate_env.sh                    # Activate development environment
scripts/quick_setup.sh                         # Complete project setup
./open_vscode.sh                         # Launch VS Code with configuration

# Server operations
python main.py                           # Start FastAPI server
python status.py                         # Check all tool statuses
python minimal_server.py                 # Start minimal server

# Testing
python -m pytest tests/                  # Run all tests
python -m pytest tests/unit/             # Run unit tests only
python -m pytest tests/integration/      # Run integration tests only

# SuperTools management
curl http://localhost:7777/api/v1/supergateway/status    # Check SuperGateway
curl http://localhost:7777/api/v1/supercompat/status     # Check SuperCompat

# Development
code cerberus-fangs.code-workspace       # Open VS Code workspace
docker-compose up -d                     # Deploy with Docker
```

---

**Remember:** With great power comes great responsibility. Use these tools ethically and legally.

🛡️ **LANCELOTT** - *Your AI-Enhanced Guardian in the Digital Realm*

*Last Updated: August 26, 2025 - Comprehensive SuperTools Integration & VS Code Enhancement*

### 🔍 **Nmap** - Network Discovery and Security Auditing

- **Purpose:** Network reconnaissance and port scanning
- **Features:** Service detection, OS fingerprinting, vulnerability scripts
- **API Endpoint:** `/api/v1/nmap/`

### 👁️ **Argus** - Network Monitoring and Flow Analysis

**Location:** `./Argus/`

- **Purpose:** Network traffic analysis and monitoring
- **Features:** Flow data collection, network behavior analysis
- **API Endpoint:** `/api/v1/argus/`

### 🐙 **Kraken** - Multi-tool Security Framework

**Location:** `./Kraken/`

- **Purpose:** Comprehensive web application security testing
- **Features:** Multiple scanning modules, customizable attacks
- **API Endpoint:** `/api/v1/kraken/`

### 🌐 **Metabigor** - Intelligence Gathering and OSINT

**Location:** `./Metabigor/`

- **Purpose:** Open Source Intelligence (OSINT) gathering
- **Features:** Domain reconnaissance, subdomain enumeration
- **API Endpoint:** `/api/v1/metabigor/`

### 🗺️ **Dismap** - Asset Discovery and Mapping

**Location:** `./dismap/`

- **Purpose:** Asset discovery and service fingerprinting
- **Features:** Fast port scanning, service detection
- **API Endpoint:** `/api/v1/dismap/`

### 🔬 **Osmedeus** - Automated Reconnaissance Framework

**Location:** `./Osmedeus/`

- **Purpose:** Automated reconnaissance and vulnerability assessment
- **Features:** Workflow automation, comprehensive scanning
- **API Endpoint:** `/api/v1/osmedeus/`

### �️ **SpiderFoot** - Open Source Intelligence Automation

**Location:** `./Spiderfoot/`

- **Purpose:** Automated OSINT data collection
- **Features:** 200+ modules, data correlation
- **API Endpoint:** `/api/v1/spiderfoot/`

### � **Social Analyzer** - Social Media Analysis and Profiling

**Location:** `./Social-Analyzer/`

- **Purpose:** Social media reconnaissance and profiling
- **Features:** Multi-platform analysis, profile detection
- **API Endpoint:** `/api/v1/social-analyzer/`

### ⛈️ **Storm Breaker** - Social Engineering and OSINT Tool

**Location:** `./Storm-Breaker/`

- **Purpose:** Social engineering information gathering
- **Features:** Link generation, credential harvesting
- **API Endpoint:** `/api/v1/storm-breaker/`

### 📱 **PhoneSploit Pro** - Android Device Exploitation

**Location:** `./PhoneSploit-Pro/`

- **Purpose:** Android device penetration testing
- **Features:** ADB exploitation, device control
- **API Endpoint:** `/api/v1/phonesploit/`

### ⚡ **Vajra** - User Interface Testing and Automation

**Location:** `./Vajra/`

- **Purpose:** UI testing and automation framework
- **Features:** Automated testing, vulnerability detection
- **API Endpoint:** `/api/v1/vajra/`

### 🛠️ **RedTeam Toolkit** - Comprehensive Red Team Utilities

**Location:** `./RedTeam_ToolKit/`

- **Purpose:** Red team operations and utilities
- **Features:** Multiple attack tools and techniques
- **API Endpoint:** `/api/v1/redteam-toolkit/`

## 🚀 Quick Start

### Automated Setup (Recommended)

```bash
# Clone and navigate to the project
cd /path/to/LANCELOTT

# Run the automated setup script
./setup.sh
```

### Manual Setup

1. **Install Dependencies:**

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

2. **Configure Environment:**

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (set your secret key, database URL, etc.)
nano .env
```

3. **Start the Application:**

```bash
# Using Python directly
python main.py

# Or using Uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 7777
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t cerberus-fangs .
docker run -p 7777:7777 cerberus-fangs
```

## 📖 API Documentation

Once the application is running, visit:

- **Swagger UI:** <http://localhost:7777/docs>
- **ReDoc:** <http://localhost:7777/redoc>
- **Health Check:** <http://localhost:7777/api/v1/health>

## 🔐 Authentication

The API uses JWT-based authentication. Default credentials:

- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Change these credentials in production!**

### Getting an Access Token

```bash
curl -X POST "http://localhost:7777/api/v1/auth/token" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
```

### Using the Token

```bash
curl -X GET "http://localhost:7777/api/v1/tools" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🌐 API Endpoints

### Core Endpoints

| Endpoint                           | Method | Description                     |
| ---------------------------------- | ------ | ------------------------------- |
| `/`                                | GET    | Main dashboard                  |
| `/api/v1/health`                   | GET    | Health check                    |
| `/api/v1/tools`                    | GET    | List all tools and their status |
| `/api/v1/tools/{tool_name}/status` | GET    | Get specific tool status        |

### Tool-Specific Endpoints

Each tool has its own set of endpoints under `/api/v1/{tool_name}/`:

#### Nmap Endpoints

- `POST /api/v1/nmap/scan` - Create new scan
- `GET /api/v1/nmap/scan/{scan_id}` - Get scan results
- `GET /api/v1/nmap/scans` - List all scans
- `DELETE /api/v1/nmap/scan/{scan_id}` - Cancel scan
- `GET /api/v1/nmap/presets` - Get scan presets

#### Example: Creating an Nmap Scan

```bash
curl -X POST "http://localhost:7777/api/v1/nmap/scan" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "target": "scanme.nmap.org",
       "scan_type": "basic",
       "ports": "80,443,8080",
       "output_format": "xml"
     }'
```

## 🏗️ Project Structure

```
CERBERUS-FANGS/LANCELOTT/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── setup.sh               # Automated setup script
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── .env.example          # Environment template
├── api/                  # API modules
│   ├── routes/          # API route definitions
│   ├── models.py        # Pydantic models
│   └── auth.py          # Authentication logic
├── core/                # Core functionality
│   ├── config.py        # Configuration settings
│   ├── logging.py       # Logging configuration
│   └── tool_manager.py  # Tool management logic
├── static/              # Static files
├── logs/                # Application logs
├── reports/             # Generated reports
├── uploads/             # File uploads
└── [Security Tools]/   # Individual tool directories
```

## 🔧 Configuration

Key configuration options in `.env`:

```bash
# Application
DEBUG=false
HOST=0.0.0.0
PORT=7777

# Security
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./cerberus_fangs.db

# Tool Paths (auto-detected)
NMAP_PATH=/opt/homebrew/bin/nmap
```

## 📊 Monitoring and Logging

- **Application Logs:** `./logs/cerberus_fangs_YYYYMMDD.log`
- **Tool-Specific Logs:** `./logs/{tool_name}_YYYYMMDD.log`
- **Error Logs:** `./logs/cerberus_fangs_YYYYMMDD_errors.log`
- **Health Monitoring:** `/api/v1/health` endpoint

## 🐳 Docker Support

### Docker Compose (Recommended)

```yaml
version: "3.8"
services:
  cerberus-fangs:
    build: .
    ports:
      - "7777:7777"
    volumes:
      - ./logs:/app/logs
      - ./reports:/app/reports
```

### Production Deployment

For production deployment, consider:

1. **Use HTTPS/TLS encryption**
2. **Configure proper firewall rules**
3. **Set up reverse proxy (Nginx)**
4. **Use production database (PostgreSQL)**
5. **Implement rate limiting**
6. **Set up monitoring and alerting**

## 🔒 Security Considerations

⚠️ **IMPORTANT SECURITY NOTES:**

1. **Change default credentials immediately**
2. **Use strong secret keys in production**
3. **Implement proper network segmentation**
4. **Only run scans on authorized targets**
5. **Use HTTPS in production**
6. **Regularly update all dependencies**
7. **Implement proper access controls**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See individual tool directories for their specific licenses.

## ⚠️ Legal Disclaimer

This toolkit is intended for authorized security testing and educational purposes only. Users are responsible for ensuring they have proper authorization before conducting any security assessments. The developers assume no liability for misuse of this software.

## 🆘 Support

- **Documentation:** <http://localhost:7777/docs>
- **Health Check:** <http://localhost:7777/api/v1/health>
- **Logs:** Check `./logs/` directory for detailed information

---

**Remember:** With great power comes great responsibility. Use these tools ethically and legally.

🛡️ **CERBERUS-FANGS LANCELOTT** - *Your Guardian in the Digital Realm*

- **Key Modules:**
  - DNS reconnaissance & zone transfer detection
  - SSL/TLS security analysis
  - Subdomain enumeration & takeover detection
  - Technology stack fingerprinting
  - Security headers analysis
  - Malware & phishing detection

### 🗺️ **dismap** - Asset Discovery & Fingerprinting

**Location:** `./dismap/`

- **Language:** Go
- **Purpose:** Network asset discovery and service fingerprinting
- **Features:** Protocol detection, service enumeration, banner grabbing

### 🐙 **Kraken** - Multi-Protocol Brute Force Tool

**Location:** `./Kraken/`

- **Purpose:** Comprehensive brute force attack framework
- **Supported Protocols:**
  - Web: WordPress, Joomla, Drupal, Magento, WooCommerce
  - Network: SSH, FTP, RDP, Telnet
  - Cloud: Office365, Kubernetes
  - Other: LDAP, VoIP, WiFi
- **Features:** Built-in wordlists, admin panel finder, webshell detection

### 🔬 **Metabigor** - OSINT & Reconnaissance

**Location:** `./Metabigor/`

- **Language:** Go
- **Purpose:** Open Source Intelligence gathering and network reconnaissance
- **Features:** Certificate transparency, IP analysis, network block enumeration

### ⚡ **Osmedeus** - Automated Reconnaissance Framework

**Location:** `./Osmedeus/`

- **Language:** Go
- **Purpose:** Fully automated reconnaissance and vulnerability scanning
- **Features:**
  - Workflow automation
  - Distributed scanning
  - Cloud integration (AWS, DigitalOcean, Linode)
  - Web UI dashboard
  - Report generation

### 📱 **PhoneSploit-Pro** - Android Device Exploitation

**Location:** `./PhoneSploit-Pro/`

- **Purpose:** Android device penetration testing via ADB
- **Features:** Remote Android device control and exploitation

### 🔴 **RedTeam_ToolKit** - Web-Based Red Team Platform

**Location:** `./RedTeam_ToolKit/`

- **Framework:** Django
- **Purpose:** Centralized red team operations dashboard
- **Features:** Web interface for various security testing tools
- **Deployment:** Docker support included

### 👥 **Social-Analyzer** - Social Media OSINT

**Location:** `./Social-Analyzer/`

- **Languages:** Python & Node.js
- **Purpose:** Social media profile analysis and OSINT
- **Features:**
  - Multi-platform social media scanning
  - Profile correlation
  - Name analysis
  - Visualization tools

### 🕷️ **SPIDERFOOT** - Automated OSINT Collection

**Location:** `./SPIDERFOOT/`

- **Purpose:** Comprehensive OSINT automation platform
- **Features:**
  - 200+ modules for data collection
  - Web UI interface
  - Correlation engine
  - API integrations
  - Docker deployment

### ⛈️ **Storm-Breaker** - Social Engineering Toolkit

**Location:** `./Storm-Breaker/`

- **Purpose:** Social engineering and phishing framework
- **Features:** Web-based phishing campaigns, template management

### 🤖 **UI-TARS** - AI-Powered Testing Framework

**Location:** `./UI-TARS/`

- **Framework:** TypeScript/Node.js
- **Purpose:** AI-driven user interface testing and automation
- **Features:** Multimodal AI agents, GUI automation, benchmark testing

### ☁️ **Vajra** - Cloud Security Assessment

**Location:** `./Vajra/`

- **Purpose:** Azure/AWS cloud security testing
- **Features:**
  - Azure AD enumeration
  - AWS S3 bucket scanning
  - Cloud consent attacks
  - Phishing campaigns targeting cloud services

## 🚀 Quick Start

### System Requirements

```bash
# Required software versions
Python >= 3.8
Go >= 1.19
Node.js >= 16
Docker (optional)
```

### Tool Installation Commands

#### Python-based Tools

```bash
# Argus - Web Security Scanner
cd Argus && pip install -r requirements.txt
python argus.py --help

# Kraken - Brute Force Tool
cd Kraken && pip install -r requirements.txt
python kraken.py

# PhoneSploit-Pro - Android Exploitation
cd PhoneSploit-Pro && pip install -r requirements.txt
python phonesploitpro.py

# Social-Analyzer - Social Media OSINT
cd Social-Analyzer && pip install -r requirements.txt
python app.py

# SPIDERFOOT - OSINT Automation
cd SPIDERFOOT && pip install -r requirements.txt
python sf.py -l 127.0.0.1:5001

# Storm-Breaker - Social Engineering
cd Storm-Breaker && pip install -r requirements.txt
python st.py

# Vajra - Cloud Security Testing
cd Vajra/Code && pip install -r requirements.txt
python app.py
```

#### Go-based Tools

```bash
# dismap - Asset Discovery
cd dismap && go build -o dismap cmd/dismap/main.go
./dismap --help

# Metabigor - OSINT Framework
cd Metabigor && go build -o metabigor main.go
./metabigor --help

# Osmedeus - Automated Reconnaissance
cd Osmedeus && go build -o osmedeus main.go
./osmedeus --help
```

#### Node.js/TypeScript Tools

```bash
# UI-TARS - AI Testing Framework
cd UI-TARS && npm install
npm run dev
```

#### Django Web Applications

```bash
# RedTeam_ToolKit - Web Platform
cd RedTeam_ToolKit && pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 📊 Tool Categories & Usage

### 🔍 **Reconnaissance & OSINT**

```bash
# Argus - Web application reconnaissance
cd Argus && python argus.py --target example.com

# Metabigor - Network & certificate intelligence
cd Metabigor && ./metabigor cert --target example.com

# Social-Analyzer - Social media intelligence
cd Social-Analyzer && python app.py --username target_user

# SPIDERFOOT - Automated OSINT collection
cd SPIDERFOOT && python sf.py -s example.com
```

### 🛡️ **Vulnerability Assessment**

```bash
# Osmedeus - Automated vulnerability scanning
cd Osmedeus && ./osmedeus scan -t example.com

# dismap - Service fingerprinting
cd dismap && ./dismap -i target_list.txt

# RedTeam_ToolKit - Centralized testing platform
cd RedTeam_ToolKit && python manage.py runserver
```

### 💥 **Exploitation & Testing**

```bash
# Kraken - Multi-protocol brute forcing
cd Kraken && python kraken.py

# PhoneSploit-Pro - Mobile device exploitation
cd PhoneSploit-Pro && python phonesploitpro.py

# Storm-Breaker - Social engineering
cd Storm-Breaker && python st.py

# Vajra - Cloud security testing
cd Vajra/Code && python app.py
```

### 🤖 **Automation & AI**

```bash
# UI-TARS - AI-powered testing automation
cd UI-TARS && npm run start

# Osmedeus - Workflow automation
cd Osmedeus && ./osmedeus workflow -f general
```

## ⚠️ Legal Disclaimer

This toolkit is intended for:

- ✅ Authorized penetration testing
- ✅ Security research
- ✅ Educational purposes
- ✅ Bug bounty programs

**WARNING:** Unauthorized use of these tools against systems you don't own or lack explicit permission to test is illegal and unethical.

## 🛠️ Development

### Project Structure

```
LANCELOTT/
├── Argus/              # Web security scanner
├── dismap/             # Asset discovery (Go)
├── Kraken/             # Brute force toolkit
├── Metabigor/          # OSINT framework (Go)
├── Osmedeus/           # Automated recon (Go)
├── PhoneSploit-Pro/    # Android exploitation
├── RedTeam_ToolKit/    # Django red team platform
├── Social-Analyzer/    # Social media OSINT
├── SPIDERFOOT/         # OSINT automation
├── Storm-Breaker/      # Social engineering
├── UI-TARS/            # AI testing framework
└── Vajra/              # Cloud security testing
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

Each tool maintains its own license. Please check individual tool directories for specific licensing information.

## 🤖 LLM/Agent Automation Guide

### Batch Tool Setup

```bash
# Setup all Python tools
for tool in Argus Kraken PhoneSploit-Pro Social-Analyzer SPIDERFOOT Storm-Breaker; do
  cd $tool && pip install -r requirements.txt && cd ..
done

# Setup all Go tools
for tool in dismap Metabigor Osmedeus; do
  cd $tool && go build && cd ..
done
```

### Tool Execution Patterns

```bash
# Pattern: Web reconnaissance
cd Argus && python argus.py --target $TARGET
cd SPIDERFOOT && python sf.py -s $TARGET

# Pattern: Network scanning
cd dismap && ./dismap -i targets.txt
cd Osmedeus && ./osmedeus scan -t $TARGET

# Pattern: Social engineering
cd Social-Analyzer && python app.py --username $USERNAME
cd Storm-Breaker && python st.py
```

### Environment Variables

```bash
export LANCELOTT_ROOT="/path/to/LANCELOTT"
export TARGET_DOMAIN="example.com"
export TARGET_IP="192.168.1.1"
export WORDLIST_PATH="$LANCELOTT_ROOT/Kraken/wordlists/"
```

## 🔗 Tool Documentation

| Tool            | README                        | Main Script         | Purpose                |
| --------------- | ----------------------------- | ------------------- | ---------------------- |
| Argus           | `./Argus/README.md`           | `argus.py`          | Web Security Scanner   |
| dismap          | `./dismap/readme.md`          | `dismap`            | Asset Discovery        |
| Kraken          | `./Kraken/readme.md`          | `kraken.py`         | Brute Force Tool       |
| Metabigor       | `./Metabigor/README.md`       | `metabigor`         | OSINT Framework        |
| Osmedeus        | `./Osmedeus/README.md`        | `osmedeus`          | Automated Recon        |
| PhoneSploit-Pro | `./PhoneSploit-Pro/README.md` | `phonesploitpro.py` | Android Exploitation   |
| RedTeam_ToolKit | `./RedTeam_ToolKit/README.md` | `manage.py`         | Web Platform           |
| Social-Analyzer | `./Social-Analyzer/README.md` | `app.py`            | Social Media OSINT     |
| SPIDERFOOT      | `./SPIDERFOOT/README.md`      | `sf.py`             | OSINT Automation       |
| Storm-Breaker   | `./Storm-Breaker/README.md`   | `st.py`             | Social Engineering     |
| UI-TARS         | `./UI-TARS/README.md`         | `package.json`      | AI Testing Framework   |
| Vajra           | `./Vajra/README.md`           | `app.py`            | Cloud Security Testing |

## 📝 Quick Reference Commands

```bash
# Initialize workspace
export LANCELOTT_HOME=$(pwd)

# Check tool status
ls -la */README.md | wc -l  # Should show 12 tools

# Verify installations
which python3 go node docker

# Create results directory
mkdir -p results/{recon,vuln,exploit,reports}
```

---

**CERBERUS-FANGS: LANCELOTT** - *Your comprehensive cybersecurity arsenal*

> **Note for LLMs/Agents:** This repository contains 12 independent cybersecurity tools. Each tool directory contains its own README.md with specific usage instructions. All nested .git directories have been removed for clean integration.
