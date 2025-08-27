# SpiderFoot - OSINT Automation Tool

## Port Configuration

- **Default Port**: 8085 (Standalone Web UI)
- **API Endpoint**: `/api/v1/spiderfoot`
- **Full URL**: `http://localhost:7777/api/v1/spiderfoot`
- **Standalone Web UI**: `http://localhost:8085` (when running standalone)

## Description

SpiderFoot is an open source intelligence (OSINT) automation tool that integrates with numerous data sources for reconnaissance:

- Domain and subdomain enumeration
- Email address discovery
- Social media profiling
- Dark web monitoring
- Threat intelligence gathering
- 200+ modules for comprehensive OSINT

## API Endpoints

- `GET /` - Get tool information
- `POST /scan` - Start a new OSINT scan
- `GET /scan/{scan_id}` - Get scan results
- `GET /scans` - List all scans
- `GET /modules` - List available modules

## Usage via API

```bash
# Start an OSINT scan
curl -X POST "http://localhost:7777/api/v1/spiderfoot/scan" \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "scan_type": "subdomain_enum", "modules": ["sfp_dns", "sfp_whois"]}'

# Get scan results
curl "http://localhost:7777/api/v1/spiderfoot/scan/{scan_id}"
```

## Standalone Mode

SpiderFoot can also run as a standalone web application on port 8085:

```bash
cd Spiderfoot
python sfwebui.py -l 0.0.0.0:8085
```

## Integration

This tool is integrated into the CERBERUS-FANGS LANCELOTT unified security toolkit and runs within the main FastAPI application on port 7777, with optional standalone web UI on port 8085.
