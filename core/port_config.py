# CERBERUS-FANGS LANCELOTT - Port Configuration

# Main FastAPI Application
MAIN_API_PORT = 7777

# Tool-specific ports for standalone services
# Note: 8080 is reserved for Jenkins, so Argus moved to 8092
TOOL_PORTS = {
    "argus": 8092,  # Moved from 8080 (Jenkins conflict)
    "kraken": 8081,
    "metabigor": 8082,
    "dismap": 8083,
    "osmedeus": 8084,
    "spiderfoot": 8085,
    "social-analyzer": 8086,
    "storm-breaker": 8087,
    "phonesploit": 8088,
    "redteam-toolkit": 8089,
    "webstor": 8090,
    "thc-hydra": 8091,
    "sherlock": 8093,
    "web-check": 8094,
}

# Tool descriptions and endpoints
TOOL_INFO = {
    "argus": {
        "name": "Argus",
        "description": "Comprehensive web application reconnaissance tool",
        "port": 8092,  # Updated port to avoid Jenkins conflict
        "endpoint": "/api/v1/argus",
        "requires_standalone": False,
    },
    "kraken": {
        "name": "Kraken",
        "description": "Advanced brute force attack framework",
        "port": 8081,
        "endpoint": "/api/v1/kraken",
        "requires_standalone": False,
    },
    "metabigor": {
        "name": "Metabigor",
        "description": "Intelligence gathering tool for OSINT",
        "port": 8082,
        "endpoint": "/api/v1/metabigor",
        "requires_standalone": False,
    },
    "dismap": {
        "name": "Dismap",
        "description": "Asset discovery and fingerprinting tool",
        "port": 8083,
        "endpoint": "/api/v1/dismap",
        "requires_standalone": False,
    },
    "osmedeus": {
        "name": "Osmedeus",
        "description": "Automated reconnaissance and vulnerability scanning",
        "port": 8084,
        "endpoint": "/api/v1/osmedeus",
        "requires_standalone": False,
    },
    "spiderfoot": {
        "name": "SpiderFoot",
        "description": "Open source intelligence automation tool",
        "port": 8085,
        "endpoint": "/api/v1/spiderfoot",
        "requires_standalone": True,
        "web_ui": True,
    },
    "social-analyzer": {
        "name": "Social Analyzer",
        "description": "Social media OSINT analysis tool",
        "port": 8086,
        "endpoint": "/api/v1/social-analyzer",
        "requires_standalone": True,
        "web_ui": True,
    },
    "storm-breaker": {
        "name": "Storm Breaker",
        "description": "Social engineering and phishing toolkit",
        "port": 8087,
        "endpoint": "/api/v1/storm-breaker",
        "requires_standalone": True,
        "web_ui": True,
    },
    "phonesploit": {
        "name": "PhoneSploit Pro",
        "description": "Android device exploitation framework",
        "port": 8088,
        "endpoint": "/api/v1/phonesploit",
        "requires_standalone": False,
    },
    "redteam-toolkit": {
        "name": "RedTeam ToolKit",
        "description": "Django-based red team web application",
        "port": 8089,
        "endpoint": "/api/v1/redteam-toolkit",
        "requires_standalone": True,
        "web_ui": True,
    },
    "webstor": {
        "name": "Webstor",
        "description": "Web application storage and analysis tool",
        "port": 8090,
        "endpoint": "/api/v1/webstor",
        "requires_standalone": False,
    },
    "thc-hydra": {
        "name": "THC Hydra",
        "description": "Fast network login cracker",
        "port": 8091,
        "endpoint": "/api/v1/hydra",
        "requires_standalone": False,
    },
    "sherlock": {
        "name": "Sherlock",
        "description": "Social media username OSINT investigation tool",
        "port": 8093,
        "endpoint": "/api/v1/sherlock",
        "requires_standalone": False,
    },
    "web-check": {
        "name": "Web-Check",
        "description": "Comprehensive website analysis and security checker",
        "port": 8094,
        "endpoint": "/api/v1/web-check",
        "requires_standalone": True,
        "web_ui": True,
    },
}
