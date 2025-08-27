<h1 align="center">
  🔱 Vajra - Your Weapon To Cloud 
</h1>

<p align="center">
  <em>Advanced Cloud Security Testing Platform for Azure & AWS</em>
</p>

<p align="center">
  <a href="">
    <img src="https://raw.githubusercontent.com/toolswatch/badges/b3a921c9e9084018758752aacc9bd9ec95cd11f8/arsenal/europe/2021.svg">
  </a>
  <a href="">
    <img src="https://img.shields.io/badge/License-AGPL_v3-blue.svg">
  </a>
  <a href="">
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg">
  </a>
  <a href="">
    <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg">
  </a>
</p>


<br>
<p align="center">
  <a href="https://github.com/TROUBLE-1/Vajra/">
    <img src="https://media3.giphy.com/media/pZOMvUVfVKJWP05Kww/giphy.gif"  width="750" >
  </a>
</p>



## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)
- Administrative privileges (for installation)

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TROUBLE-1/Vajra.git
   cd Vajra
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv vajra_env
   source vajra_env/bin/activate  # On Windows: vajra_env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   cd Code
   pip install -r requirements.txt
   ```

4. **Start Vajra**
   ```bash
   python app.py
   ```

5. **Access the Web Interface**
   - Open your browser and navigate to: **http://localhost:9847**
   - Default admin credentials:
     - Username: `admin`
     - Email: `admin@vajra.local`
     - Password: `admin123` (⚠️ Change after first login!)

### 🌐 Network Configuration
- **Default Port**: 9847 (chosen to avoid conflicts with common services)
- **Host**: 0.0.0.0 (accessible from any network interface)
- **Protocol**: HTTP (HTTPS configuration available in code comments)

## About Vajra

Vajra is a UI based tool with multiple techniques for attacking and enumerating in target's Azure environment. 

The term Vajra refers to the Weapon of God Indra in Indian mythology (God of Thunder &amp; Storms). Its connection to the cloud makes it a perfect name for the tool.

Vajra presently supports Azure and AWS Cloud environments, with plans to add support for Google Cloud Platform and certain OSINT in the future.

## 🔥 Features Overview

### 🔵 Azure Cloud Security Testing

#### 🎯 Attack Modules
- **OAuth Phishing (Illicit Consent Grant Attack)**
  - Data exfiltration capabilities
  - Environment enumeration
  - Backdoor deployment
  - Email manipulation and rule creation
- **Password Spray Attacks**
- **Password Brute Force Attacks**

#### 🔍 Enumeration Modules
- **User Enumeration** - Discover and analyze user accounts
- **Subdomain Discovery** - Find subdomains associated with target
- **Azure AD Enumeration** - Comprehensive Active Directory analysis
- **Azure Services Discovery** - Identify available Azure services

#### 🎯 Specific Service Testing
- **Storage Account Security Testing** - Comprehensive storage analysis

### 🟠 AWS Cloud Security Testing

#### 🔍 Enumeration Modules
- **IAM Enumeration** - Identity and Access Management analysis
- **S3 Bucket Scanner** - Security assessment of S3 storage
- **Misconfiguration Detection** - Identify security misconfigurations

#### 🎯 Attack Modules
- **Under Active Development** - Advanced attack capabilities coming soon

### 📊 Performance Tested
- Successfully tested with environments containing **300,000+ principals**
- Includes users, groups, enterprise applications, and more
- Optimized for large-scale enterprise environments

## 📊 Screenshots

![Vajra Dashboard](https://github.com/TROUBLE-1/Vajra/raw/main/images/dashboard.png)

![AWS Dashboard](https://github.com/TROUBLE-1/Vajra/raw/main/images/aws-dashboard.png)

It features an intuitive web-based user interface built with the Python Flask module for a better user experience.

## 📖 User Guide

### First Time Setup

1. **Initial Access**
   - Navigate to `http://localhost:9847` after installation
   - Use default credentials to log in (change immediately after first login)

2. **Security Recommendations**
   - Change default admin password immediately
   - Enable IP restrictions if running in production
   - Consider using HTTPS (configuration available in app.py)

3. **Target Configuration**
   - Configure your Azure/AWS credentials in the application
   - Set up proper permissions for enumeration and testing
   - Review target scope and permissions before starting tests

### 🔧 Troubleshooting

#### Common Issues

**Port Already in Use**
- If port 9847 is occupied, modify the port in `Code/app.py`
- Choose a unique port number (e.g., 9848, 8765, etc.)

**Permission Errors**
- Ensure proper file permissions on the Vajra directory
- Run with appropriate user privileges
- Check virtual environment activation

**Database Issues**
- SQLite database is created automatically in `vajra/site.db`
- Delete the database file to reset (will lose all data)
- Ensure write permissions in the vajra directory

**Module Import Errors**
- Verify virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version compatibility (3.8+)

### 🛡️ Security Considerations

- **Use in Authorized Environments Only**: Only test on systems you own or have explicit permission to test
- **Network Security**: Consider firewall rules and network segmentation
- **Credential Management**: Store credentials securely, avoid hardcoding
- **Logging**: Monitor application logs for security events
- **Updates**: Keep dependencies updated for security patches

### 🎯 Best Practices

1. **Planning Phase**
   - Define clear testing scope and objectives
   - Obtain proper authorization before testing
   - Document expected vs actual results

2. **Execution Phase**
   - Start with enumeration before attempting attacks
   - Monitor for detection and response
   - Keep detailed logs of activities

3. **Reporting Phase**
   - Document all findings with evidence
   - Provide clear remediation recommendations
   - Follow responsible disclosure practices

# **About Author**

Raunak Parmar is an information security professional whose areas of interest include web penetration testing, Azure/AWS security, source code review, scripting, and development. He has 3+ years of experience in information security. Raunak holds OSWE certification and likes to research new attack methodologies and create open-source tools that can be used during Cloud Security assessments. He has worked extensively on Azure and AWS.

He is the author of [Vajra](https://github.com/TROUBLE-1/Vajra) an offensive cloud security tool and has spoken at multiple conferences like NullCon, Defcon, Blackhat, and local meetups.

<a target="_blank"><img alt="readme-stats" src="https://github-readme-stats.vercel.app/api?username=trouble-1&show_icons=true&theme=vue-dark"/></a>

### **Social Media Links**

- Twitter: [https://twitter.com/trouble1\_raunak](https://twitter.com/trouble1_raunak)
- YouTube: [https://www.youtube.com/channel/UCkJ\_sEF8iUDXPCI3UL0DAcg](https://www.youtube.com/channel/UCkJ_sEF8iUDXPCI3UL0DAcg)
- Linkedin: [https://www.linkedin.com/in/trouble1raunak/](https://www.linkedin.com/in/trouble1raunak/)
- GitHub: [https://github.com/TROUBLE-1/](https://github.com/TROUBLE-1/)




# Installation & Usage

## 🚀 Automated Setup (Recommended)

For the quickest setup, use the installation script:

```bash
# Clone and setup in one command
git clone https://github.com/TROUBLE-1/Vajra.git && cd Vajra && python -m venv vajra_env && source vajra_env/bin/activate && cd Code && pip install -r requirements.txt && python app.py
```

## 📋 Manual Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/TROUBLE-1/Vajra.git
cd Vajra
```

### Step 2: Create Virtual Environment
```bash
python -m venv vajra_env
source vajra_env/bin/activate  # On Windows: vajra_env\Scripts\activate
```

### Step 3: Install Dependencies
```bash
cd Code
pip install -r requirements.txt
```

### Step 4: Launch Application
```bash
python app.py
```

### Step 5: Access Web Interface
Open your browser and navigate to: **http://localhost:9847**

## 🔄 Alternative Installation Methods

### Using Docker (Community Contribution)
```bash
# Pull and run (if available)
docker pull tr0uble1/vajra   
docker run -p 9847:9847 -d tr0uble1/vajra
```

### System-wide Installation (Not Recommended)
```bash
cd Code
pip install -r requirements.txt  # Install globally
python app.py
```

## ⚙️ Configuration Options

### Port Configuration
To change the default port (9847), edit `Code/app.py`:
```python
# Change port 9847 to your preferred port
socketio.run(app, host='0.0.0.0', port=YOUR_PORT, debug=False)
```

### HTTPS Configuration
Uncomment and configure the HTTPS section in `Code/app.py`:
```python
# For HTTPS (requires SSL certificates)
app.run(port=443, host="0.0.0.0", debug=True, ssl_context=context)
```


## How to use Vajra?

A detailed usage guide is available on [Documentation](https://github.com/TROUBLE-1/Vajra/wiki/Documentation) section of the Wiki.

### 🎯 Quick Start Guide

1. **Initial Setup**: Follow installation instructions above
2. **First Login**: Access http://localhost:9847 with default credentials
3. **Security Setup**: Change default password and configure security settings
4. **Target Configuration**: Set up your Azure/AWS credentials and permissions
5. **Start Testing**: Begin with enumeration modules before attempting attacks

### 📚 Recommended Learning Path

1. **Azure Fundamentals**: Understand Azure AD, IAM, and service architecture
2. **AWS Basics**: Learn IAM, S3, and core AWS security concepts  
3. **Reconnaissance**: Master enumeration techniques before attacks
4. **Attack Methodology**: Follow a structured approach to testing
5. **Documentation**: Always document findings and create reports

## 🚨 Important Recommendations

### ⚠️ Legal and Ethical Use
- **Authorization Required**: Only test systems you own or have explicit written permission to test
- **Responsible Disclosure**: Report vulnerabilities responsibly to affected organizations
- **Compliance**: Ensure testing complies with local laws and regulations
- **Documentation**: Maintain detailed logs for accountability and reporting

### 🔒 Security Best Practices
- **Isolated Environment**: Run Vajra in isolated/sandboxed environments when possible
- **Credential Security**: Never store credentials in plain text or code
- **Network Segmentation**: Use proper network controls and monitoring
- **Regular Updates**: Keep Vajra and dependencies updated for security patches

### 🎯 Effective Testing Tips
- **Scope Definition**: Clearly define testing scope and boundaries
- **Incremental Approach**: Start with passive reconnaissance, then active testing
- **Rate Limiting**: Implement delays to avoid triggering security controls
- **Evidence Collection**: Screenshot and document all findings thoroughly

### 🚀 Performance Optimization
- **Resource Management**: Monitor system resources during large scans
- **Concurrent Operations**: Limit concurrent threads based on target capacity
- **Result Storage**: Regularly export and backup test results
- **Clean Environment**: Use fresh virtual environments for different engagements

## Bugs and Feature Requests

Please raise an issue if you encounter a bug or have a feature request.

## Contributing

If you want to contribute to a project and make it better, your help is very welcome.
