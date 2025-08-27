# Kraken - Advanced Brute Force Framework

## Port Configuration

- **Default Port**: 8081
- **API Endpoint**: `/api/v1/kraken`
- **Full URL**: `http://localhost:7777/api/v1/kraken`

## Description

Kraken is an advanced brute force attack framework supporting multiple protocols and services including:

- SSH brute force
- FTP brute force
- RDP brute force
- WordPress brute force
- Directory enumeration
- Admin panel discovery
- And many more protocols...

## API Endpoints

- `GET /` - Get tool information
- `POST /attack` - Start a brute force attack
- `GET /attack/{attack_id}` - Get attack results
- `GET /attacks` - List all attacks

## Usage via API

```bash
# Start an SSH brute force attack
curl -X POST "http://localhost:7777/api/v1/kraken/attack" \
  -H "Content-Type: application/json" \
  -d '{"target": "192.168.1.1", "attack_type": "ssh", "userlist": "users.txt", "passlist": "passwords.txt"}'

# Get attack results
curl "http://localhost:7777/api/v1/kraken/attack/{attack_id}"
```

## Integration

This tool is integrated into the CERBERUS-FANGS LANCELOTT unified security toolkit and runs within the main FastAPI application on port 7777.
