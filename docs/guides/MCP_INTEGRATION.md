# MCP Server Integration with LANCELOTT Framework

## Overview

This document describes the integration of Model Context Protocol (MCP) servers with the LANCELOTT security framework. MCP enables Agent-TARS and UI-TARS to interact with various tools and services through a standardized protocol.

## Integrated MCP Servers

### 1. Redis MCP Server

- **Purpose**: Provides access to Redis for caching and session management
- **Package**: `@modelcontextprotocol/server-redis`
- **Connection**: `redis://localhost:6379/0`
- **Configuration**: Uses the Redis URL from the LANCELOTT environment

### 2. Chart MCP Server

- **Purpose**: Enables data visualization capabilities
- **Package**: `@antvis/mcp-server-chart`
- **Features**: Bar charts, line charts, maps, and other visualizations

### 3. File MCP Server

- **Purpose**: Provides file system access and manipulation
- **Package**: `@modelcontextprotocol/server-file`
- **Features**: Read, write, and manage files in the workspace

## Configuration Files

### Agent-TARS Configuration (`agent-tars.config.ts`)

```typescript
import { defineConfig } from '@agent-tars/interface';

export default defineConfig({
  mcpServers: {
    'mcp-server-redis': {
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-redis', 'redis://localhost:6379/0'],
      env: {
        REDIS_URL: 'redis://localhost:6379/0',
        DEBUG: 'mcp:*'
      }
    },
    'mcp-server-chart': {
      command: 'npx',
      args: ['-y', '@antvis/mcp-server-chart'],
    },
    'mcp-server-file': {
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-file'],
    }
  },
  // ... other configuration
});
```

### MCP Configuration (`mcp-config.json`)

```json
{
  "name": "LANCELOTT-MCP-Redis",
  "version": "2.1.0",
  "servers": [
    {
      "id": "redis-server",
      "name": "LANCELOTT Redis Server",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-redis", "redis://localhost:6379/0"],
      "env": {
        "REDIS_URL": "redis://localhost:6379/0",
        "DEBUG": "mcp:*"
      }
    }
  ]
}
```

## Workspace Integration

The LANCELOTT tools are integrated with the Agent-TARS workspace through symbolic links:

```
LANCELOTT/
└── tools/
    └── UI-TARS/
        └── agent-tars-workspace/
            └── tools/ → Symbolic links to LANCELOTT tools
```

## Troubleshooting

### Redis URL Parsing Error

**Problem**: `TypeError: Invalid URL` when starting MCP Redis server

**Solution**:

1. Ensure the Redis URL includes the database number: `redis://localhost:6379/0`
2. Set the `REDIS_URL` environment variable explicitly
3. Use proper URL encoding if special characters are present

### Server Not Starting

**Problem**: MCP servers fail to start or connect

**Solutions**:

1. Verify the required services are running (Redis, etc.)
2. Check network connectivity to the services
3. Ensure Node.js and npx are properly installed
4. Verify package names and versions

## Usage Examples

### Starting Agent-TARS with MCP Servers

```bash
# From the LANCELOTT root directory
./agent-tars --interactive
```

### Testing MCP Server Connectivity

```bash
# Test Redis MCP server
npx -y @modelcontextprotocol/server-redis redis://localhost:6379/0

# Test Chart MCP server
npx -y @antvis/mcp-server-chart
```

## Tools Integration

The following LANCELOTT tools are accessible through the MCP integration:

- Network reconnaissance: nmap, dismap
- Web application testing: Kraken, feroxbuster, Argus
- OSINT gathering: Metabigor, Spiderfoot, Social-Analyzer
- Brute force testing: THC-Hydra
- Mobile security: PhoneSploit-Pro
- Cloud security: Vajra
- And many more...

## Future Enhancements

1. **Dynamic Tool Discovery**: Automatically discover and integrate new tools
2. **Enhanced Security**: Implement authentication for MCP server connections
3. **Performance Monitoring**: Add metrics and monitoring for MCP servers
4. **Error Handling**: Improve error reporting and recovery mechanisms
