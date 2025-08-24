# CERBERUS-FANGS: LANCELOTT Cybersecurity Toolkit

A comprehensive collection of cybersecurity tools for reconnaissance, vulnerability assessment, and penetration testing.

## 🛡️ Tool Arsenal

### 🔍 **Argus** - Web Application Security Scanner
**Location:** `./Argus/`
- **Purpose:** Comprehensive web application security assessment
- **Features:** 50+ security modules including SSL analysis, subdomain enumeration, vulnerability scanning
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

| Tool | README | Main Script | Purpose |
|------|--------|-------------|----------|
| Argus | `./Argus/README.md` | `argus.py` | Web Security Scanner |
| dismap | `./dismap/readme.md` | `dismap` | Asset Discovery |
| Kraken | `./Kraken/readme.md` | `kraken.py` | Brute Force Tool |
| Metabigor | `./Metabigor/README.md` | `metabigor` | OSINT Framework |
| Osmedeus | `./Osmedeus/README.md` | `osmedeus` | Automated Recon |
| PhoneSploit-Pro | `./PhoneSploit-Pro/README.md` | `phonesploitpro.py` | Android Exploitation |
| RedTeam_ToolKit | `./RedTeam_ToolKit/README.md` | `manage.py` | Web Platform |
| Social-Analyzer | `./Social-Analyzer/README.md` | `app.py` | Social Media OSINT |
| SPIDERFOOT | `./SPIDERFOOT/README.md` | `sf.py` | OSINT Automation |
| Storm-Breaker | `./Storm-Breaker/README.md` | `st.py` | Social Engineering |
| UI-TARS | `./UI-TARS/README.md` | `package.json` | AI Testing Framework |
| Vajra | `./Vajra/README.md` | `app.py` | Cloud Security Testing |

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