# MCP Workspace Setup for LANCELOTT Framework

## Overview

This document provides instructions for setting up the Model Context Protocol (MCP) workspace for the LANCELOTT Framework with Agent-TARS and UI-TARS integration.

## Prerequisites

- Node.js and npm installed
- Redis server running on localhost:6379
- LANCELOTT Framework installed

## MCP Server Integration

The LANCELOTT Framework integrates with the following MCP servers:

1. **Redis MCP Server** - For caching and session management
2. **Chart MCP Server** - For data visualization capabilities
3. **File MCP Server** - For file system access and manipulation
4. **PostgreSQL MCP Server** - For database operations

## Configuration Files

### Agent-TARS Configuration (`agent-tars.config.ts`)

Located at: `tools/UI-TARS/multimodal/agent-tars.config.ts`

```typescript
import { defineConfig } from '@agent-tars/interface';

export default defineConfig({
  name: 'LANCELOTT-Agent-TARS',
  version: '2.1.0',

  // MCP Server configuration
  mcpServers: {
    'mcp-server-chart': {
      command: 'npx',
      args: ['-y', '@antv/mcp-server-chart'],
    },

    'mcp-server-redis': {
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-redis', 'redis://localhost:6379/0'],
      env: {
        REDIS_URL: 'redis://localhost:6379/0',
        DEBUG: 'mcp:*',
      },
    },

    'mcp-server-postgres': {
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-postgres'],
    },

    'mcp-server-file': {
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-file'],
    },
  },

  // Workspace configuration
  workspace: {
    path: './agent-tars-workspace',
    createIfMissing: true,
    toolsPath: './agent-tars-workspace/tools'
  },

  // ... other configuration
});
```

### MCP Configuration (`mcp-config.json`)

Located at: `tools/UI-TARS/multimodal/mcp-config.json`

```json
{
  "name": "LANCELOTT-MCP-Redis",
  "version": "2.1.0",
  "description": "MCP Server for Redis integration with LANCELOTT Framework",
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
    },
    {
      "id": "chart-server",
      "name": "MCP Chart Server",
      "command": "npx",
      "args": ["-y", "@antv/mcp-server-chart"]
    },
    {
      "id": "file-server",
      "name": "MCP File Server",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-file"]
    }
  ],
  "workspace": {
    "path": "./agent-tars-workspace",
    "toolsPath": "./agent-tars-workspace/tools"
  },
  "logging": {
    "level": "info",
    "file": "./logs/mcp-servers.log"
  }
}
```

## Manual Workspace Setup

If the automated setup script doesn't work, you can manually set up the workspace:

1. Navigate to the multimodal directory:

   ```bash
   cd tools/UI-TARS/multimodal
   ```

2. Create the workspace directory structure:

   ```bash
   mkdir -p agent-tars-workspace/tools
   ```

3. Create symbolic links for all LANCELOTT tools:

   ```bash
   cd agent-tars-workspace/tools
   ln -s ../../../../Argus Argus
   ln -s ../../../../Kraken Kraken
   ln -s ../../../../nmap nmap
   ln -s ../../../../feroxbuster feroxbuster
   ln -s ../../../../Spiderfoot Spiderfoot
   ln -s ../../../../Social-Analyzer Social-Analyzer
   ln -s ../../../../THC-Hydra THC-Hydra
   ln -s ../../../../PhoneSploit-Pro PhoneSploit-Pro
   ln -s ../../../../Vajra Vajra
   # ... create links for all other tools
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

## Usage

To start Agent-TARS with MCP integration:

```bash
cd /path/to/LANCELOTT
./lance --interactive
```

The Agent-TARS interface should now have access to all MCP servers and LANCELOTT tools through the workspace integration.
