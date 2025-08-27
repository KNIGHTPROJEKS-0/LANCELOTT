# 🚀 CERBERUS-FANGS LANCELOTT - Deployment Guide

## ✅ System Status: READY FOR DEPLOYMENT

The CERBERUS-FANGS LANCELOTT unified security toolkit has been successfully configured with:

- ✅ **Single Virtual Environment**: All tools consolidated
- ✅ **Unified Requirements**: One requirements.txt with all dependencies
- ✅ **Docker Integration**: Multi-stage Dockerfile ready
- ✅ **Port Configuration**: 12 tools mapped to unique ports
- ✅ **FastAPI Integration**: Unified API endpoints
- ✅ **System Tests**: All tests passed

## 🐳 Docker Deployment (Recommended)

### Quick Start

```bash
# Build and start the entire stack
docker-compose up -d --build

# Check container status
docker-compose ps

# View logs
docker-compose logs -f cerberus-fangs

# Access the API
curl http://localhost:7777/api/v1/health
```

### Available Services

- **Main API**: <http://localhost:7777>
- **API Documentation**: <http://localhost:7777/docs>
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 🖥️ Manual Deployment

### Prerequisites

```bash
# System requirements
- Python 3.11+
- Node.js 18+
- Go 1.19+
- Docker (optional)
- 8GB RAM minimum
- 20GB disk space
```

### Installation Steps

```bash
# 1. Clone and enter directory
git clone <repository-url>
cd CERBERUS-FANGS-LANCELOTT

# 2. Run unified setup
./startup.sh

# 3. Access the application
curl http://localhost:7777/api/v1/health
```

## 📊 Tool Access Points

| Tool | Port | API Endpoint | Status |
|------|------|--------------|--------|
| **Main API** | 7777 | `/api/v1/` | ✅ Active |
| **Argus** | 8080 | `/api/v1/argus` | ✅ Integrated |
| **Kraken** | 8081 | `/api/v1/kraken` | ✅ Integrated |
| **Metabigor** | 8082 | `/api/v1/metabigor` | ✅ Integrated |
| **Dismap** | 8083 | `/api/v1/dismap` | ✅ Integrated |
| **Osmedeus** | 8084 | `/api/v1/osmedeus` | ✅ Integrated |
| **SpiderFoot** | 8085 | `/api/v1/spiderfoot` | ✅ Integrated |
| **Social-Analyzer** | 8086 | `/api/v1/social-analyzer` | ✅ Integrated |
| **Storm-Breaker** | 8087 | `/api/v1/storm-breaker` | ✅ Integrated |
| **PhoneSploit Pro** | 8088 | `/api/v1/phonesploit` | ✅ Integrated |
| **RedTeam-ToolKit** | 8089 | `/api/v1/redteam-toolkit` | ✅ Integrated |
| **Webstor** | 8090 | `/api/v1/webstor` | ✅ Integrated |
| **THC-Hydra** | 8091 | `/api/v1/hydra` | ✅ Integrated |

## 🔧 Configuration Files

### Unified Requirements

- **File**: `requirements.txt`
- **Contents**: All tool dependencies consolidated
- **Status**: ✅ Complete

### Docker Configuration

- **Dockerfile**: Multi-stage build with all tools
- **docker-compose.yml**: Full stack orchestration
- **Status**: ✅ Ready

### Port Mapping

- **File**: `core/port_config.py`
- **Configuration**: All 12 tools mapped
- **Status**: ✅ Configured

## 🌐 API Usage Examples

### Health Check

```bash
curl http://localhost:7777/api/v1/health
```

### Start Security Scans

```bash
# Argus web reconnaissance
curl -X POST "http://localhost:7777/api/v1/argus/scan" \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "scan_type": "full"}'

# Kraken brute force
curl -X POST "http://localhost:7777/api/v1/kraken/attack" \
  -H "Content-Type: application/json" \
  -d '{"target": "192.168.1.1", "attack_type": "ssh"}'

# SpiderFoot OSINT
curl -X POST "http://localhost:7777/api/v1/spiderfoot/scan" \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com"}'
```

## 📁 Directory Structure

```
CERBERUS-FANGS-LANCELOTT/
├── 📄 requirements.txt        # ✅ Unified dependencies
├── 🐳 Dockerfile             # ✅ Multi-tool container
├── 🔧 docker-compose.yml     # ✅ Full stack
├── 🚀 startup.sh             # ✅ Unified launcher
├── 🧪 test_system.py         # ✅ System validation
├── 📊 api/                   # ✅ FastAPI routes
├── 🛠️  core/                 # ✅ Framework core
├── 🔧 Argus/                 # ✅ Web reconnaissance
├── 🔧 Kraken/                # ✅ Brute force framework
├── 🔧 Spiderfoot/            # ✅ OSINT automation
├── 🔧 Social-Analyzer/       # ✅ Social media OSINT
├── 🔧 RedTeam-ToolKit/       # ✅ Django red team app
├── 🔧 Storm-Breaker/         # ✅ Social engineering
├── 🔧 PhoneSploit-Pro/       # ✅ Android exploitation
└── 🔧 [other tools]/         # ✅ Additional tools
```

## 🔒 Security Features

- **JWT Authentication**: Secure API access
- **Input Validation**: Comprehensive request validation
- **Rate Limiting**: API abuse prevention
- **Containerization**: Isolated execution
- **Audit Logging**: Complete operation tracking

## 📊 Performance Optimization

### Single Environment Benefits

- **Reduced Memory**: Shared Python environment
- **Faster Startup**: No multiple environments
- **Unified Dependencies**: No conflicts
- **Resource Sharing**: Common libraries

### Container Optimization

- **Multi-stage Build**: Optimized image size
- **Shared Dependencies**: Efficient caching
- **Resource Limits**: Controlled resource usage

## 🚦 Health Monitoring

### Health Endpoints

```bash
# Main health check
curl http://localhost:7777/api/v1/health

# Tool-specific health
curl http://localhost:7777/api/v1/argus/
curl http://localhost:7777/api/v1/kraken/
```

### Logging

- **Application Logs**: `logs/cerberus_fangs.log`
- **Tool Logs**: Individual tool log directories
- **Container Logs**: `docker-compose logs`

## 🔄 Development Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --host 0.0.0.0 --port 7777 --reload

# Access API docs
open http://localhost:7777/docs
```

## ⚠️ Important Notes

1. **Legal Usage**: Only use for authorized security testing
2. **Resource Requirements**: Minimum 8GB RAM recommended
3. **Port Availability**: Ensure ports 7777-8091 are available
4. **API Keys**: Configure any required API keys in environment variables
5. **Firewall**: Configure firewall rules if needed

## 🎯 Next Steps

1. **Deploy the system** using Docker or manual installation
2. **Access the API documentation** at <http://localhost:7777/docs>
3. **Configure API authentication** if needed
4. **Start security scans** using the unified API
5. **Monitor logs** for operation status

---

**🐺 CERBERUS-FANGS LANCELOTT is now ready for deployment! 🐺**

All tools are unified in one environment, accessible through one API, running in one container. Maximum security, minimum complexity.
