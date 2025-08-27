# Dismap Usage Guide

## What is Dismap?

Dismap is an asset discovery and identification tool that can quickly identify protocols and fingerprint information such as web/tcp/udp. It's perfect for red team reconnaissance and blue team asset inventory.

## Key Features

- **4500+ web fingerprint rules** - Comprehensive detection capabilities
- **Multiple protocols** - TCP, UDP, TLS support
- **Fast scanning** - Multi-threaded scanning with customizable speed
- **Flexible output** - Text and JSON format results
- **Network range support** - CIDR notation and IP ranges

## Quick Start Examples

### Basic URL Scanning

```bash
# Scan a single website
./dismap -u https://example.com

# Scan with custom output
./dismap -u https://example.com -o results.txt -j results.json
```

### Network Scanning

```bash
# Scan a network range
./dismap -i 192.168.1.0/24

# Scan specific IP range
./dismap -i 192.168.1.1-50

# Scan with custom ports
./dismap -i 192.168.1.0/24 -p 80,443,8080,8443

# Full port scan
./dismap -i 192.168.1.0/24 -p 1-65535
```

### Advanced Options

```bash
# Increase threads for faster scanning
./dismap -i 192.168.1.0/24 -t 1000

# Skip ping detection
./dismap -i 192.168.1.0/24 --np

# Custom timeout
./dismap -i 192.168.1.0/24 --timeout 10

# Specific protocol mode
./dismap -i 192.168.1.0/24 -m http
./dismap -u mysql://192.168.1.1:3306 -m mysql
```

### Using Proxy

```bash
# HTTP proxy
./dismap -i 192.168.1.0/24 --proxy http://127.0.0.1:8080

# SOCKS5 proxy
./dismap -i 192.168.1.0/24 --proxy socks5://127.0.0.1:1080
```

### Batch Scanning

```bash
# Create a target file
echo "https://example1.com" > targets.txt
echo "https://example2.com" >> targets.txt
echo "192.168.1.100" >> targets.txt

# Scan from file
./dismap -f targets.txt
```

## Configuration Notes

### Binary Location

- The dismap binary is located at: `/Users/ORDEROFCODE/KNIGHTPROJEKS/CERBERUS-FANGS/LANCELOTT/dismap/dismap`
- Version: 0.4 (darwin-arm64)
- Updated from bin/dismap-0.4-darwin-arm64

### Output Files

- Default text output: `output.txt`
- JSON output: Use `-j filename.json`
- Custom text output: `-o filename.txt`

### Performance Tuning

- Default threads: 500
- Recommended for large networks: 1000-2000 threads
- Default timeout: 5 seconds
- Increase timeout for slow networks: 10-15 seconds

### Log Levels

- 0: Fatal
- 1: Error
- 2: Info
- 3: Warning (default)
- 4: Debug
- 5: Verbose

## Security Considerations

- Only scan networks you own or have permission to test
- Be mindful of scan intensity on production networks
- Use appropriate delays and thread counts
- Monitor for detection by security systems
- Follow responsible disclosure for any findings

## Integration with Other Tools

- Results can be parsed and integrated with other security tools
- JSON output format makes automation easier
- Compatible with vulnerability scanners for follow-up testing
