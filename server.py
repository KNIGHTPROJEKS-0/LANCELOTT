#!/usr/bin/env python3
"""
Standard HTTP server for CERBERUS-FANGS LANCELOTT
Run this directly for a simple web interface without FastAPI dependencies
"""

import json
import os
import subprocess
import sys
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class CerberusHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
<!DOCTYPE html>
<html>
<head>
    <title>🛡️ CERBERUS-FANGS LANCELOTT</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { color: #00ff88; font-size: 2.5em; }
        .tool-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .tool-card { background: #333; padding: 20px; border-radius: 10px; border: 2px solid #00ff88; }
        .tool-card h3 { color: #00ff88; margin-top: 0; }
        .status { font-weight: bold; }
        .available { color: #00ff88; }
        .unavailable { color: #ff4444; }
        .api-section { margin-top: 40px; padding: 20px; background: #2a2a2a; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ CERBERUS-FANGS LANCELOTT</h1>
        <p>Professional Penetration Testing Suite</p>
        <p><strong>Status:</strong> <span class="status available">Operational</span></p>
    </div>

    <div class="tool-grid">
        <div class="tool-card">
            <h3>🔍 Nmap</h3>
            <p>Network discovery and security auditing</p>
            <p class="status">Status: <span id="nmap-status">Checking...</span></p>
        </div>
        <div class="tool-card">
            <h3>👁️ Argus</h3>
            <p>Network monitoring and flow analysis</p>
            <p class="status">Status: <span id="argus-status">Available</span></p>
        </div>
        <div class="tool-card">
            <h3>🐙 Kraken</h3>
            <p>Multi-tool security framework</p>
            <p class="status">Status: <span id="kraken-status">Available</span></p>
        </div>
        <div class="tool-card">
            <h3>🌐 Metabigor</h3>
            <p>Intelligence gathering and OSINT</p>
            <p class="status">Status: <span id="metabigor-status">Available</span></p>
        </div>
        <div class="tool-card">
            <h3>🗺️ Dismap</h3>
            <p>Asset discovery and mapping</p>
            <p class="status">Status: <span id="dismap-status">Available</span></p>
        </div>
        <div class="tool-card">
            <h3>🔬 Osmedeus</h3>
            <p>Automated reconnaissance framework</p>
            <p class="status">Status: <span id="osmedeus-status">Available</span></p>
        </div>
        <div class="tool-card">
            <h3>🌉 SuperGateway</h3>
            <p>MCP stdio server gateway (SSE/WebSocket)</p>
            <p class="status">Status: <span id="supergateway-status">Available</span></p>
        </div>
        <div class="tool-card">
            <h3>🤖 SuperCompat</h3>
            <p>Multi-provider AI compatibility layer</p>
            <p class="status">Status: <span id="supercompat-status">Available</span></p>
        </div>
    </div>

    <div class="api-section">
        <h2>🚀 Quick Start</h2>
        <p>The FastAPI server will be available once dependencies are installed.</p>
        <p><strong>Installation Status:</strong> Setting up dependencies...</p>
        <p><strong>Next Steps:</strong></p>
        <ol>
            <li>Wait for dependency installation to complete</li>
            <li>Configure .env file</li>
            <li>Run: <code>python main.py</code></li>
        </ol>
        <p><strong>Default API Endpoints:</strong></p>
        <ul>
            <li><code>GET /api/v1/health</code> - Health check</li>
            <li><code>GET /api/v1/tools</code> - List all tools</li>
            <li><code>POST /api/v1/nmap/scan</code> - Create Nmap scan</li>
        </ul>
    </div>

    <script>
        // Check nmap status
        fetch('/api/status/nmap')
            .then(response => response.json())
            .then(data => {
                document.getElementById('nmap-status').textContent = data.status;
                document.getElementById('nmap-status').className = data.available ? 'available' : 'unavailable';
            })
            .catch(() => {
                document.getElementById('nmap-status').textContent = 'Unknown';
            });
    </script>
</body>
</html>
            """
            self.wfile.write(html.encode())

        elif self.path == "/api/status/nmap":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            try:
                result = subprocess.run(
                    ["nmap", "--version"], capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    version = result.stdout.split("\n")[0]
                    response = {
                        "status": "Available",
                        "available": True,
                        "version": version,
                    }
                else:
                    response = {"status": "Error", "available": False}
            except:
                response = {"status": "Not Found", "available": False}

            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()


def main():
    print("🛡️ CERBERUS-FANGS LANCELOTT - Web Interface")
    print("=" * 60)

    # Check Python version
    print(f"Python Version: {sys.version}")

    # Check basic tool availability
    tools_status = {}

    # Check nmap
    try:
        result = subprocess.run(
            ["nmap", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.split("\n")[0]
            tools_status["nmap"] = f"✓ {version}"
        else:
            tools_status["nmap"] = "✗ Error running nmap"
    except:
        tools_status["nmap"] = "✗ Nmap not found"

    # Check tool directories
    tools = ["Argus", "Kraken", "Metabigor", "dismap", "Osmedeus", "Spiderfoot"]
    for tool in tools:
        if Path(tool).exists():
            tools_status[tool] = f"✓ {tool} directory found"
        else:
            tools_status[tool] = f"✗ {tool} directory not found"

    print("\nTool Status:")
    for tool, status in tools_status.items():
        print(f"  {status}")

    print(f"\n🌐 Starting web server on http://localhost:9999")
    print("📖 This will serve a basic interface while FastAPI dependencies install")
    print("🔧 To start the full FastAPI server, run: python main.py")
    print("\nPress Ctrl+C to stop the server")

    try:
        server = HTTPServer(("localhost", 9999), CerberusHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")


if __name__ == "__main__":
    main()
