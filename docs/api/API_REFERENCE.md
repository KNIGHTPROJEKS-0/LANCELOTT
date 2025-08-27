# LANCELOTT API Reference

## Overview

The CERBERUS-FANGS LANCELOTT framework provides a comprehensive RESTful API for managing security tools, workflows, and integrations. The API is built with FastAPI and provides automatic OpenAPI documentation.

## Base URL

```
http://localhost:7777/api/v1
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Core Endpoints

### Health & Status

#### GET `/health`

Check system health status

- **Response**: System health information including tools and integrations status

#### GET `/status/dashboard`

Get comprehensive status dashboard

- **Response**: Detailed system status report with component health

#### GET `/integrations/status`

Get status of all tool integrations

- **Response**: Tool status with health information and summary

### Tool Management

#### POST `/integrations/{tool_name}/execute`

Execute a command with a specific tool

- **Parameters**:
  - `tool_name`: Name of the tool to execute
  - `command`: Command to execute
- **Authentication**: Required
- **Response**: Execution result with success status

### Workflow Management

#### GET `/workflows/n8n/health`

Check n8n workflow system health

- **Response**: n8n system health status

#### POST `/workflows/n8n/setup`

Setup n8n workflows for LANCELOTT

- **Authentication**: Required
- **Response**: Setup results for all workflows

### Reports

#### POST `/status/report/generate`

Generate comprehensive status report

- **Parameters**:
  - `format`: Report format (json, text)
  - `save_to_file`: Whether to save to file
- **Authentication**: Required
- **Response**: Generated report or file path

## Tool-Specific Endpoints

### Network Reconnaissance

#### Nmap - `/tools/nmap`

- `POST /scan` - Start network scan
- `GET /scan/{scan_id}/status` - Get scan status
- `GET /scan/{scan_id}/results` - Get scan results

#### Dismap - `/tools/dismap`

- `POST /scan` - Start asset discovery
- `GET /scan/{scan_id}/status` - Get scan status
- `GET /scan/{scan_id}/results` - Get discovery results

### Web Application Testing

#### Argus - `/tools/argus`

- `POST /scan` - Start web application scan
- `GET /scan/{scan_id}/status` - Get scan status
- `GET /scan/{scan_id}/results` - Get vulnerability report

#### Kraken - `/tools/kraken`

- `POST /scan` - Start advanced web scan
- `GET /scan/{scan_id}/status` - Get scan progress
- `GET /scan/{scan_id}/results` - Get detailed results

#### Web-Check - `/tools/web-check`

- `POST /scan` - Start website analysis
- `GET /scan/{scan_id}/status` - Get analysis status
- `GET /scan/{scan_id}/results` - Get website report

### OSINT & Intelligence

#### Metabigor - `/tools/metabigor`

- `POST /recon` - Start reconnaissance
- `GET /recon/{recon_id}/status` - Get recon status
- `GET /recon/{recon_id}/results` - Get OSINT data

#### SpiderFoot - `/tools/spiderfoot`

- `POST /scan` - Start OSINT scan
- `GET /scan/{scan_id}/status` - Get scan status
- `GET /scan/{scan_id}/results` - Get intelligence report

#### SHERLOCK - `/tools/sherlock`

- `POST /search` - Start username investigation
- `GET /search/{search_id}/status` - Get search status
- `GET /search/{search_id}/results` - Get username report

#### Social-Analyzer - `/tools/social-analyzer`

- `POST /analyze` - Start social media analysis
- `GET /analyze/{analysis_id}/status` - Get analysis status
- `GET /analyze/{analysis_id}/results` - Get social intelligence

### Penetration Testing

#### Osmedeus - `/tools/osmedeus`

- `POST /scan` - Start comprehensive pentest
- `GET /scan/{scan_id}/status` - Get scan status
- `GET /scan/{scan_id}/results` - Get pentest report

#### Vajra - `/tools/vajra`

- `POST /scan` - Start automated security testing
- `GET /scan/{scan_id}/status` - Get testing status
- `GET /scan/{scan_id}/results` - Get security report

#### THC-Hydra - `/tools/hydra`

- `POST /attack` - Start brute force attack
- `GET /attack/{attack_id}/status` - Get attack status
- `GET /attack/{attack_id}/results` - Get attack results

#### RedTeam-ToolKit - `/tools/redteam-toolkit`

- `POST /operation` - Start red team operation
- `GET /operation/{op_id}/status` - Get operation status
- `GET /operation/{op_id}/results` - Get operation report

### Mobile & IoT Security

#### PhoneSploit-Pro - `/tools/phonesploit`

- `POST /exploit` - Start mobile exploitation
- `GET /exploit/{exploit_id}/status` - Get exploit status
- `GET /exploit/{exploit_id}/results` - Get exploitation results

## Advanced Orchestration

### Multi-Tool Scans - `/advanced`

#### POST `/orchestrate/scan`

Execute multi-tool security scan

- **Parameters**: Target and tool selection
- **Authentication**: Required
- **Response**: Orchestration results

#### POST `/batch/execute`

Execute batch operations

- **Parameters**: Batch job configuration
- **Authentication**: Required
- **Response**: Batch execution status

#### GET `/analytics/summary`

Get analytics summary

- **Response**: Comprehensive analytics data

#### GET `/health/comprehensive`

Get comprehensive health check

- **Response**: Detailed system health analysis

## Integration Endpoints

### SuperGateway - `/integrations/supergateway`

- `POST /connect` - Connect to AI gateway
- `GET /status` - Get gateway status
- `POST /request` - Make AI request

### SuperCompat - `/integrations/supercompat`

- `POST /translate` - Translate between AI formats
- `GET /models` - Get available models
- `POST /execute` - Execute AI compatibility request

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable

Error response format:

```json
{
  "detail": "Error description",
  "timestamp": "2024-01-01T00:00:00Z",
  "error_code": "LANCELOTT_ERROR_CODE"
}
```

## Rate Limiting

API requests are rate-limited to prevent abuse:

- Standard endpoints: 100 requests/minute
- Tool execution endpoints: 10 requests/minute
- Heavy operations: 5 requests/minute

## WebSocket Endpoints

Real-time updates are available via WebSocket:

- `/ws/status` - Real-time status updates
- `/ws/scans/{scan_id}` - Real-time scan progress
- `/ws/tools/{tool_name}` - Real-time tool output

## OpenAPI Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:7777/docs`
- ReDoc: `http://localhost:7777/redoc`
- OpenAPI JSON: `http://localhost:7777/openapi.json`

## SDK & Client Libraries

Official client libraries are available for:

- Python: `pip install lancelott-client`
- JavaScript/TypeScript: `npm install lancelott-client`
- Go: `go get github.com/lancelott/client-go`

## Examples

### Python Client Example

```python
import asyncio
from lancelott_client import LancelottClient

async def main():
    client = LancelottClient("http://localhost:7777")

    # Authenticate
    await client.authenticate("your_token")

    # Start a scan
    scan = await client.tools.nmap.scan({
        "target": "192.168.1.0/24",
        "scan_type": "comprehensive"
    })

    # Monitor progress
    while not scan.is_complete():
        status = await scan.get_status()
        print(f"Progress: {status.progress}%")
        await asyncio.sleep(5)

    # Get results
    results = await scan.get_results()
    print(f"Found {len(results.hosts)} hosts")

if __name__ == "__main__":
    asyncio.run(main())
```

### cURL Examples

```bash
# Health check
curl -X GET "http://localhost:7777/api/v1/health"

# Start Nmap scan
curl -X POST "http://localhost:7777/api/v1/tools/nmap/scan" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target": "192.168.1.1", "scan_type": "fast"}'

# Get scan results
curl -X GET "http://localhost:7777/api/v1/tools/nmap/scan/nmap_20240101_120000/results" \
  -H "Authorization: Bearer $TOKEN"
```

## Support

For API support and questions:

- Documentation: [LANCELOTT Docs](http://localhost:7777/docs)
- Issues: Create an issue in the project repository
- Community: Join our Discord server
