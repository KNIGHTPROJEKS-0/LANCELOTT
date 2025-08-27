# RedTeam-ToolKit - Django Offensive Web Application

## Port Configuration

- **Default Port**: 8089 (Standalone Django Web UI)
- **API Endpoint**: `/api/v1/redteam-toolkit`
- **Full URL**: `http://localhost:7777/api/v1/redteam-toolkit`
- **Standalone Web UI**: `http://localhost:8089` (when running standalone)

## Description

RedTeam-ToolKit is a Django-based offensive web application for red team operations:

- Full network scanning with PDF reports
- Directory scanning and enumeration
- CVE vulnerability scanning
- SSH and RDP brute force attacks
- Web application testing tools
- Automated XSS detection
- Subdomain enumeration

## API Endpoints

- `GET /` - Get tool information
- `POST /scan` - Start a comprehensive scan
- `GET /scan/{scan_id}` - Get scan results
- `POST /bruteforce` - Start brute force attack
- `GET /reports` - List generated reports

## Usage via API

```bash
# Start a full network scan
curl -X POST "http://localhost:7777/api/v1/redteam-toolkit/scan" \
  -H "Content-Type: application/json" \
  -d '{"target": "192.168.1.0/24", "scan_type": "fullscan"}'

# Start SSH brute force
curl -X POST "http://localhost:7777/api/v1/redteam-toolkit/bruteforce" \
  -H "Content-Type: application/json" \
  -d '{"target": "192.168.1.1", "service": "ssh", "userlist": "users.txt"}'
```

## Standalone Mode

RedTeam-ToolKit can run as a standalone Django web application:

```bash
cd RedTeam-ToolKit
python manage.py runserver 0.0.0.0:8089
```

Default credentials for standalone mode:

- Username: admin
- Password: Create via `python manage.py createsuperuser`

## Integration

This tool is integrated into the CERBERUS-FANGS LANCELOTT unified security toolkit and runs within the main FastAPI application on port 7777, with optional standalone Django web interface on port 8089.
