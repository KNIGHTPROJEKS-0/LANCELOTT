# LANCELOTT Tools Documentation

## Overview

CERBERUS-FANGS LANCELOTT includes 17+ integrated security tools organized into categories for comprehensive penetration testing and security assessment.

## Tool Categories

### Network Reconnaissance

Tools for network discovery, port scanning, and infrastructure analysis.

### Web Application Testing

Tools for web application security assessment and vulnerability discovery.

### OSINT & Intelligence Gathering

Tools for open source intelligence and information gathering.

### Mobile & IoT Security

Tools for mobile device and IoT security testing.

### Social Engineering

Tools for social engineering assessments and awareness testing.

### Penetration Testing

Comprehensive penetration testing and exploitation tools.

---

## Network Reconnaissance Tools

### Nmap

**Location**: `nmap/`
**Type**: Network Scanner
**Port**: 7001
**Status**: Optional

Advanced network discovery and security auditing tool.

**Features**:

- Host discovery
- Port scanning
- Service detection
- OS fingerprinting
- Vulnerability scanning with NSE scripts

**Usage via API**:

```bash
POST /api/v1/tools/nmap/scan
{
  "target": "192.168.1.0/24",
  "scan_type": "comprehensive",
  "ports": "1-65535",
  "scripts": ["vuln", "discovery"]
}
```

**Direct Usage**:

```bash
./nmap/nmap -sC -sV -A target.com
```

### Dismap

**Location**: `tools/dismap/`
**Type**: Asset Discovery
**Port**: 7011
**Status**: Enabled

Asset discovery and service detection tool.

**Features**:

- Asset discovery
- Service fingerprinting
- Technology stack detection
- Passive reconnaissance

**Build Requirements**:

- Go 1.18+

**Usage via API**:

```bash
POST /api/v1/tools/dismap/scan
{
  "target": "example.com",
  "mode": "discovery",
  "passive": true
}
```

---

## Web Application Testing Tools

### Argus

**Location**: `tools/Argus/`
**Type**: Web Scanner
**Port**: 7002
**Status**: Enabled

Web application security scanner with comprehensive vulnerability detection.

**Features**:

- SQL injection detection
- XSS vulnerability scanning
- Directory enumeration
- Authentication bypass testing

**Build Requirements**:

- Python 3.8+
- pip dependencies

**Usage via API**:

```bash
POST /api/v1/tools/argus/scan
{
  "url": "https://target.com",
  "scan_depth": "comprehensive",
  "modules": ["sqli", "xss", "directory"]
}
```

### Kraken

**Location**: `tools/Kraken/`
**Type**: Advanced Web Scanner
**Port**: 7003
**Status**: Enabled

Advanced web application security testing framework.

**Features**:

- Advanced vulnerability detection
- Custom payload generation
- API security testing
- WebSocket testing

**Usage via API**:

```bash
POST /api/v1/tools/kraken/scan
{
  "target": "https://api.target.com",
  "test_types": ["api", "websocket"],
  "authentication": {
    "type": "bearer",
    "token": "auth_token"
  }
}
```

### Web-Check

**Location**: `tools/Web-Check/`
**Type**: Website Analyzer
**Port**: 7017
**Status**: Optional

Comprehensive website analysis and security assessment tool.

**Features**:

- SSL/TLS analysis
- Security headers check
- Performance analysis
- Accessibility testing
- Security score calculation

**Build Requirements**:

- Node.js 16+
- npm dependencies

**Usage via API**:

```bash
POST /api/v1/tools/web-check/scan
{
  "url": "https://target.com",
  "full_scan": true,
  "check_ssl": true,
  "check_security": true
}
```

### Webstor

**Location**: `tools/Webstor/`
**Type**: Web Storage Analyzer
**Port**: 7013
**Status**: Optional

Web storage and session analysis tool.

**Features**:

- Session token analysis
- Local storage inspection
- Cookie security assessment
- Storage vulnerability detection

---

## OSINT & Intelligence Tools

### Metabigor

**Location**: `tools/Metabigor/`
**Type**: OSINT Framework
**Port**: 7004
**Status**: Enabled

Comprehensive OSINT and reconnaissance framework.

**Features**:

- Domain reconnaissance
- Subdomain enumeration
- Technology detection
- Social media intelligence

**Build Requirements**:

- Go 1.18+

**Usage via API**:

```bash
POST /api/v1/tools/metabigor/recon
{
  "target": "target.com",
  "modules": ["subdomain", "technology", "social"],
  "passive": true
}
```

### SpiderFoot

**Location**: `tools/Spiderfoot/`
**Type**: OSINT Automation
**Port**: 7006
**Status**: Enabled

Automated OSINT collection and analysis platform.

**Features**:

- Automated data collection
- 200+ data sources
- Relationship mapping
- Real-time monitoring

**Usage via API**:

```bash
POST /api/v1/tools/spiderfoot/scan
{
  "target": "target.com",
  "modules": ["all"],
  "scan_type": "passive"
}
```

### SHERLOCK

**Location**: `tools/SHERLOCK/sherlock_project/`
**Type**: Username Investigation
**Port**: 7014
**Status**: Enabled

Username investigation across social networks.

**Features**:

- 400+ social network support
- Username availability checking
- Profile discovery
- Bulk username searches

**Usage via API**:

```bash
POST /api/v1/tools/sherlock/search
{
  "usernames": ["target_user"],
  "sites": ["all"],
  "timeout": 60
}
```

### Social-Analyzer

**Location**: `tools/Social-Analyzer/`
**Type**: Social Media Analysis
**Port**: 7007
**Status**: Enabled

API, CLI, and web app for analyzing social media profiles.

**Features**:

- Profile analysis
- Social graph mapping
- Content analysis
- Behavioral patterns

**Usage via API**:

```bash
POST /api/v1/tools/social-analyzer/analyze
{
  "username": "target_user",
  "platforms": ["twitter", "facebook", "instagram"],
  "analysis_depth": "comprehensive"
}
```

---

## Penetration Testing Tools

### Osmedeus

**Location**: `tools/Osmedeus/`
**Type**: Reconnaissance Framework
**Port**: 7005
**Status**: Enabled

Fully automated reconnaissance and vulnerability scanning framework.

**Features**:

- Automated reconnaissance
- Vulnerability scanning
- Reporting
- Workflow automation

**Build Requirements**:

- Go 1.18+

**Usage via API**:

```bash
POST /api/v1/tools/osmedeus/scan
{
  "target": "target.com",
  "workflow": "general",
  "modules": ["recon", "vuln", "screenshot"]
}
```

### Vajra

**Location**: `tools/Vajra/`
**Type**: Security Testing
**Port**: 7009
**Status**: Enabled

User interface for various security testing tools.

**Features**:

- Tool integration
- Result correlation
- Report generation
- Workflow management

**Usage via API**:

```bash
POST /api/v1/tools/vajra/scan
{
  "target": "target.com",
  "tools": ["nmap", "dirb", "nikto"],
  "parallel": true
}
```

### THC-Hydra

**Location**: `tools/THC-Hydra/`
**Type**: Login Cracker
**Port**: 7012
**Status**: Enabled

Network login cracker supporting numerous protocols.

**Features**:

- 50+ protocol support
- Parallel attacks
- Custom wordlists
- Proxy support

**Build Requirements**:

- GCC compiler
- Development libraries

**Usage via API**:

```bash
POST /api/v1/tools/hydra/attack
{
  "target": "192.168.1.100",
  "service": "ssh",
  "userlist": "users.txt",
  "passlist": "passwords.txt"
}
```

### RedTeam-ToolKit

**Location**: `tools/RedTeam-ToolKit/`
**Type**: Red Team Framework
**Port**: 7015
**Status**: Enabled

Comprehensive red team testing toolkit.

**Features**:

- Multiple attack vectors
- Payload generation
- Persistence mechanisms
- Evasion techniques

**Usage via API**:

```bash
POST /api/v1/tools/redteam-toolkit/operation
{
  "target": "target.com",
  "operation_type": "phishing",
  "templates": ["business"],
  "duration": "24h"
}
```

---

## Mobile & IoT Security Tools

### PhoneSploit-Pro

**Location**: `tools/PhoneSploit-Pro/`
**Type**: Android Exploitation
**Port**: 7008
**Status**: Optional

Android device exploitation and testing tool.

**Features**:

- ADB exploitation
- Device information gathering
- File system access
- Application analysis

**Usage via API**:

```bash
POST /api/v1/tools/phonesploit/exploit
{
  "target_ip": "192.168.1.50",
  "adb_port": 5555,
  "actions": ["info", "apps", "files"]
}
```

---

## Social Engineering Tools

### Storm-Breaker

**Location**: `tools/Storm-Breaker/`
**Type**: Social Engineering
**Port**: 7010
**Status**: Optional

Social engineering toolkit for awareness testing.

**Features**:

- Phishing page generation
- Social media tracking
- Location tracking
- Device information gathering

**Usage via API**:

```bash
POST /api/v1/tools/storm-breaker/campaign
{
  "campaign_type": "phishing",
  "template": "social_media",
  "target_platform": "all"
}
```

---

## Specialized Tools

### UI-TARS

**Location**: `tools/UI-TARS/`
**Type**: UI Testing
**Port**: 7016
**Status**: Optional

User interface security testing framework.

**Features**:

- UI vulnerability detection
- Automated testing
- Visual regression testing
- Accessibility testing

**Build Requirements**:

- Node.js 16+
- TypeScript
- Electron dependencies

---

## Tool Management

### Building Tools

Use the unified build manager:

```bash
python lancelott.py build --tool <tool_name>
python lancelott.py build --all
python lancelott.py build --type python
```

### Tool Status

Check tool status:

```bash
python lancelott.py status --tools
python lancelott.py status --tool <tool_name>
```

### Integration Management

Manage tool integrations:

```bash
python lancelott.py integrations --enable <tool_name>
python lancelott.py integrations --disable <tool_name>
python lancelott.py integrations --status
```

## Configuration

### Tool Configuration

Each tool can be configured in `config/lancelott.yaml`:

```yaml
tools:
  tool_name:
    name: "Tool Display Name"
    executable_path: "tools/ToolName/tool"
    wrapper_module: "integrations.tools.tool_wrapper"
    port: 7001
    dependencies: ["python3", "pip"]
    enabled: true
    optional: false
    build_type: "python"
    build_command: ["pip", "install", "-r", "requirements.txt"]
```

### Environment Variables

Tool-specific environment variables can be set:

```bash
export TOOL_NAME_CONFIG="/path/to/config"
export TOOL_NAME_DATA="/path/to/data"
```

## Troubleshooting

### Common Issues

1. **Tool Not Found**: Ensure tool is properly built and paths are correct
2. **Port Conflicts**: Check port assignments in configuration
3. **Dependencies Missing**: Install required dependencies for tool type
4. **Permission Issues**: Ensure proper file permissions for executables

### Logging

Tool execution logs are available:

```bash
tail -f logs/lancelott.log
python lancelott.py logs --tool <tool_name>
```

### Support

For tool-specific issues:

1. Check tool's original documentation
2. Verify LANCELOTT integration wrapper
3. Review build and configuration logs
4. Test tool independently outside framework

## Contributing

To add new tools to LANCELOTT:

1. Create tool directory in `tools/`
2. Implement tool wrapper in `integrations/tools/`
3. Add configuration to `config/lancelott.yaml`
4. Update build manager for tool type
5. Create API router if needed
6. Add documentation and tests

### Tool Wrapper Template

```python
#!/usr/bin/env python3
"""
Tool Wrapper Template
"""

from integrations.base_tool_wrapper import BaseToolWrapper

class ToolWrapper(BaseToolWrapper):
    def __init__(self):
        super().__init__(
            name="ToolName",
            executable_path="tools/ToolName/tool",
            config_file="config/tool.conf"
        )

    async def execute_scan(self, target: str, options: dict = None):
        # Implementation
        pass

    def parse_results(self, output: str):
        # Parse tool output
        pass
```

This documentation provides comprehensive information about all tools integrated into the LANCELOTT framework. Each tool maintains its original functionality while being enhanced with unified management, API access, and workflow integration.
