import { defineConfig } from '@agent-tars/interface';

export default defineConfig({
  // Agent-TARS configuration for LANCELOTT Framework
  name: 'LANCELOTT-Agent-TARS',
  version: '2.1.0',

  // MCP Server configuration
  mcpServers: {
    'mcp-server-chart': {
      command: 'npx',
      args: ['-y', '@antv/mcp-server-chart'],
    },

    // Additional MCP servers that might be useful for LANCELOTT
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
    toolsPath: './agent-tars-workspace/tools',
  },

  // AI Configuration
  ai: {
    model: 'gpt-5-nano',
    provider: 'azure',
    deployment: 'GPT-5-Navo-Cerberus',
    endpoint:
      'https://gujil-mensn3og-eastus2.cognitiveservices.azure.com/openai/responses?api-version=2025-04-01-preview',
  },

  // Tools configuration
  tools: {
    enabled: true,
    timeout: 300,
    maxConcurrent: 5,
  },

  // Logging configuration
  logging: {
    level: 'info',
    format: 'json',
    output: './logs/agent-tars.log',
  },
});
