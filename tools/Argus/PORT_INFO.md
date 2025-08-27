# Argus - Web Application Reconnaissance Tool

## Port Configuration

- **Default Port**: 8080
- **API Endpoint**: `/api/v1/argus`
- **Full URL**: `http://localhost:7777/api/v1/argus`

## Description

Argus is a comprehensive web application reconnaissance tool that performs various security assessments including:

- DNS enumeration
- SSL/TLS analysis
- HTTP header analysis
- Technology stack detection
- Vulnerability scanning
- And much more...

## API Endpoints

- `GET /` - Get tool information
- `POST /scan` - Start a new reconnaissance scan
- `GET /scan/{scan_id}` - Get scan results
- `GET /scans` - List all scans

## Usage via API

```bash
# Start a scan
curl -X POST "http://localhost:7777/api/v1/argus/scan" \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "scan_type": "full"}'

# Get scan results
curl "http://localhost:7777/api/v1/argus/scan/{scan_id}"
```

## Integration

This tool is integrated into the CERBERUS-FANGS LANCELOTT unified security toolkit and runs within the main FastAPI application on port 7777.
