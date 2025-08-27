# LANCELOTT Configuration Guide

## Overview

The CERBERUS-FANGS LANCELOTT framework uses a unified configuration system that manages all components including API settings, database connections, security parameters, tool configurations, and integrations.

## Configuration Files

### Primary Configuration

- **`config/lancelott.yaml`** - Main configuration file
- **`config/lancelott_config.py`** - Configuration management system
- **`.env`** - Environment variables
- **`.env.example`** - Environment template

### Legacy Configuration

- **`core/config.py`** - Legacy configuration (compatibility)

## Configuration Structure

### API Configuration

```yaml
api:
  host: "0.0.0.0"              # API host binding
  port: 7777                   # API port
  debug: false                 # Debug mode
  workers: 4                   # Number of workers
  cors_origins:                # CORS allowed origins
    - "http://localhost:3000"
    - "http://localhost:5678"
  auth_enabled: true           # Enable authentication
  rate_limiting: true          # Enable rate limiting
  ssl_cert: null              # SSL certificate path
  ssl_key: null               # SSL key path
```

### Database Configuration

```yaml
database:
  type: "sqlite"              # Database type: sqlite, postgresql, mysql
  host: "localhost"           # Database host
  port: 5432                  # Database port
  database: "lancelott"       # Database name
  username: "lancelott_user"  # Database username
  password: "lancelott_pass"  # Database password
  url: null                   # Direct database URL (optional)
```

### Security Configuration

```yaml
security:
  jwt_secret: "your-secret-key-change-in-production"  # JWT signing key
  jwt_expiration: 3600                                # JWT expiration (seconds)
  api_key_length: 32                                  # API key length
  password_min_length: 8                              # Minimum password length
  max_login_attempts: 5                               # Max failed login attempts
  lockout_duration: 300                               # Lockout duration (seconds)
```

### Integration Configuration

```yaml
integrations:
  n8n_url: "http://localhost:5678"              # n8n workflow URL
  n8n_auth_user: "admin"                        # n8n authentication user
  n8n_auth_password: "lancelott"                # n8n authentication password
  supergateway_url: "http://localhost:3000"     # SuperGateway URL
  supercompat_url: "http://localhost:3001"      # SuperCompat URL
  webhook_base_url: "http://localhost:7777/webhooks"  # Webhook base URL
```

### Logging Configuration

```yaml
logging:
  level: "INFO"                                           # Log level
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Log format
  file_path: "logs/lancelott.log"                         # Log file path
  max_file_size: 10                                       # Max log file size (MB)
  backup_count: 5                                         # Number of backup files
  console_output: true                                    # Enable console output
```

### Monitoring Configuration

```yaml
monitoring:
  enabled: true              # Enable monitoring
  check_interval: 30         # Health check interval (seconds)
  timeout: 10               # Request timeout (seconds)
  retry_attempts: 3         # Number of retry attempts
  alert_email: null         # Alert email address
  alert_webhook: null       # Alert webhook URL
```

## Tool Configuration

Each security tool has its own configuration section:

### Tool Configuration Structure

```yaml
tools:
  tool_name:
    name: "Tool Display Name"                    # Human-readable name
    executable_path: "tools/ToolName/tool"       # Path to executable
    wrapper_module: "integrations.tools.wrapper" # Python wrapper module
    port: 7001                                   # API port for tool
    dependencies: ["python3", "pip"]            # Build dependencies
    enabled: true                                # Enable/disable tool
    optional: false                              # Mark as optional
    build_type: "python"                         # Build type: python, go, node, shell
    build_command:                               # Build commands
      - "pip"
      - "install"
      - "-r"
      - "requirements.txt"
    environment_vars:                            # Environment variables
      TOOL_CONFIG: "/path/to/config"
```

### Tool Categories

#### Python Tools

```yaml
argus:
  name: "Argus"
  executable_path: "tools/Argus/argus.py"
  build_type: "python"
  build_command: ["pip", "install", "-r", "requirements.txt"]
  port: 7002
```

#### Go Tools

```yaml
metabigor:
  name: "Metabigor"
  executable_path: "tools/Metabigor/metabigor"
  build_type: "go"
  build_command: ["go", "build", "-o", "metabigor", "."]
  port: 7004
```

#### Node.js Tools

```yaml
web_check:
  name: "Web-Check"
  executable_path: "tools/Web-Check/server.js"
  build_type: "node"
  build_command: ["npm", "install", "&&", "npm", "run", "build"]
  port: 7017
```

#### Shell/C Tools

```yaml
thc_hydra:
  name: "THC-Hydra"
  executable_path: "tools/THC-Hydra/hydra"
  build_type: "shell"
  build_command: ["./configure", "&&", "make"]
  port: 7012
```

## Configuration Management

### Using the Configuration Manager

```python
from config.lancelott_config import get_config

# Get configuration instance
config = get_config()

# Access configuration sections
api_config = config.api
db_config = config.database
tool_configs = config.tools

# Get specific tool configuration
nmap_config = config.get_tool_config("nmap")

# Get enabled tools only
enabled_tools = config.get_enabled_tools()

# Get tools by build type
python_tools = config.get_tools_by_type("python")
```

### Configuration Validation

```python
# Validate configuration
issues = config.validate_configuration()
if issues:
    for issue in issues:
        print(f"Configuration issue: {issue}")
```

### Updating Configuration

```python
# Update tool configuration
config.update_tool_config("nmap", enabled=True, port=7001)

# Save configuration
config.save_configuration()
```

## Environment Variables

### Setting Environment Variables

Create a `.env` file in the project root:

```bash
# API Configuration
LANCELOTT_HOST=0.0.0.0
LANCELOTT_PORT=7777
LANCELOTT_DEBUG=false

# Database Configuration
DATABASE_TYPE=sqlite
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Security
JWT_SECRET=your-super-secret-key-change-this
JWT_EXPIRATION=3600

# Integration URLs
N8N_URL=http://localhost:5678
SUPERGATEWAY_URL=http://localhost:3000
SUPERCOMPAT_URL=http://localhost:3001

# Tool Ports
NMAP_PORT=7001
ARGUS_PORT=7002
KRAKEN_PORT=7003
```

### Generate Environment File

```bash
# Generate .env file from configuration
python config/lancelott_config.py env --output .env.generated

# Or use the CLI
python lancelott.py config --env
```

## CLI Configuration Commands

### View Configuration

```bash
# Show configuration summary
python lancelott.py config --summary

# Show full configuration
python lancelott.py config --show

# Show specific tool configuration
python lancelott.py config --tool nmap
```

### Validate Configuration

```bash
# Validate configuration
python lancelott.py config --validate

# Check for issues
python config/lancelott_config.py validate
```

### Modify Configuration

```bash
# Enable/disable tools
python lancelott.py config --enable-tool nmap
python lancelott.py config --disable-tool phonesploit

# Set API configuration
python lancelott.py config --set api.port=8080
python lancelott.py config --set api.debug=true

# Set tool ports
python lancelott.py config --set tools.nmap.port=7001
```

## Advanced Configuration

### Custom Tool Addition

1. **Add tool configuration to `lancelott.yaml`**:

```yaml
tools:
  custom_tool:
    name: "Custom Security Tool"
    executable_path: "tools/CustomTool/custom"
    wrapper_module: "integrations.tools.custom_wrapper"
    port: 7020
    dependencies: ["python3"]
    enabled: true
    optional: false
    build_type: "python"
    build_command: ["pip", "install", "-r", "requirements.txt"]
```

2. **Create tool wrapper**:

```python
# integrations/tools/custom_wrapper.py
from integrations.base_tool_wrapper import BaseToolWrapper

class CustomToolWrapper(BaseToolWrapper):
    def __init__(self):
        super().__init__(
            name="CustomTool",
            executable_path="tools/CustomTool/custom",
            config_file="config/custom.conf"
        )
```

3. **Update build manager** (if needed):

```python
# Add to build_manager.py _define_build_targets method
"custom_tool": {
    "path": self.project_root / "tools" / "CustomTool",
    "build_type": "python",
    "commands": ["pip", "install", "-r", "requirements.txt"],
    "executable": "custom",
    "optional": False
}
```

### Custom Integration

Add custom integrations to the configuration:

```yaml
integrations:
  custom_service_url: "http://localhost:9000"
  custom_api_key: "your-api-key"
  custom_webhook: "http://localhost:7777/webhooks/custom"
```

### Production Configuration

For production deployments:

```yaml
api:
  host: "0.0.0.0"
  port: 443
  debug: false
  workers: 8
  ssl_cert: "/path/to/cert.pem"
  ssl_key: "/path/to/key.pem"
  auth_enabled: true
  rate_limiting: true

database:
  type: "postgresql"
  host: "db.example.com"
  port: 5432
  database: "lancelott_prod"
  username: "lancelott_user"
  password: "secure_password"

security:
  jwt_secret: "very-long-random-secret-key"
  jwt_expiration: 1800
  max_login_attempts: 3
  lockout_duration: 600

logging:
  level: "WARNING"
  file_path: "/var/log/lancelott/app.log"
  console_output: false
```

## Configuration Backup and Restore

### Backup Configuration

```bash
# Backup current configuration
cp config/lancelott.yaml config/lancelott.yaml.backup

# Export configuration with timestamp
python lancelott.py config --export config/backup-$(date +%Y%m%d).yaml
```

### Restore Configuration

```bash
# Restore from backup
cp config/lancelott.yaml.backup config/lancelott.yaml

# Reload configuration
python lancelott.py config --reload
```

## Troubleshooting

### Common Configuration Issues

1. **Port Conflicts**:
   - Check for duplicate port assignments
   - Use `python lancelott.py config --validate`

2. **Path Issues**:
   - Ensure tool paths are relative to project root
   - Verify executable files exist

3. **Permission Issues**:
   - Check file permissions for configuration files
   - Ensure write access to logs directory

4. **Database Connection**:
   - Verify database credentials
   - Test database connectivity

### Debug Configuration

```bash
# Enable debug mode
python lancelott.py config --set api.debug=true

# Check configuration loading
python -c "from config.lancelott_config import get_config; print(get_config().get_configuration_summary())"

# Validate all components
python lancelott.py config --validate --verbose
```

### Configuration Reset

```bash
# Reset to default configuration
python lancelott.py config --reset

# Reset specific section
python lancelott.py config --reset-section tools

# Generate new configuration
python config/lancelott_config.py save
```

This configuration guide provides comprehensive information for setting up, managing, and troubleshooting the LANCELOTT framework configuration system.
