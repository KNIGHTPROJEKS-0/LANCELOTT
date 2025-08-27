#!/usr/bin/env python3
"""
LangChain.js Integration Wrapper for LANCELOTT
Provides JavaScript/TypeScript AI integration capabilities
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.integration_manager import BaseToolWrapper, ToolConfig


class LangChainJSWrapper(BaseToolWrapper):
    """Wrapper for LangChain.js integration"""

    def __init__(self):
        # Create a ToolConfig for LangChain.js
        config = ToolConfig(
            name="LangChainJS",
            executable_path="integrations/frameworks/langchainjs",
            wrapper_module="integrations.frameworks.langchainjs_wrapper",
            port=8101,
        )
        super().__init__(config)
        self.logger = logging.getLogger(__name__)

        # Legacy attributes for backward compatibility
        self.executable_path = Path(config.executable_path)
        self.config_file = "config/langchainjs.conf"
        self.description = "JavaScript/TypeScript AI integration framework"
        self.category = "AI Framework"
        self.name = config.name
        self.port = config.port

    async def initialize(self) -> bool:
        """Initialize LangChain.js integration"""
        try:
            # Check if Node.js is available
            node_result = subprocess.run(
                ["node", "--version"], capture_output=True, text=True
            )

            if node_result.returncode != 0:
                self.logger.error("Node.js not available")
                return False

            # Check if npm is available
            npm_result = subprocess.run(
                ["npm", "--version"], capture_output=True, text=True
            )

            if npm_result.returncode != 0:
                self.logger.error("npm not available")
                return False

            # Initialize LangChain.js project if needed
            await self._setup_langchainjs_project()

            self.logger.info("LangChain.js integration initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"LangChain.js initialization failed: {e}")
            return False

    async def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute LangChain.js command"""
        try:
            operation = kwargs.get("operation", "execute")
            target = kwargs.get("target", command)
            options = kwargs.get("options", {})

            if operation == "execute":
                return await self._execute_js_script(target, options)
            elif operation == "chain":
                return await self._execute_chain(target, options)
            elif operation == "agent":
                return await self._execute_agent(target, options)
            else:
                return await self._execute_js_script(target, options)

        except Exception as e:
            self.logger.error(f"LangChain.js command execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def health_check(self) -> bool:
        """Check if LangChain.js is healthy and responsive"""
        try:
            # Check Node.js availability
            result = subprocess.run(
                ["node", "--version"], capture_output=True, text=True
            )
            return result.returncode == 0

        except Exception as e:
            self.logger.warning(f"LangChain.js health check failed: {e}")
            return False

    async def _setup_langchainjs_project(self):
        """Setup LangChain.js project structure"""
        try:
            project_dir = self.executable_path
            project_dir.mkdir(parents=True, exist_ok=True)

            # Create package.json if it doesn't exist
            package_json = project_dir / "package.json"
            if not package_json.exists():
                package_config = {
                    "name": "lancelott-langchainjs",
                    "version": "1.0.0",
                    "description": "LangChain.js integration for LANCELOTT",
                    "main": "index.js",
                    "type": "module",
                    "scripts": {
                        "start": "node index.js",
                        "dev": "node --watch index.js",
                    },
                    "dependencies": {
                        "langchain": "^0.1.0",
                        "@langchain/core": "^0.1.0",
                        "@langchain/community": "^0.0.20",
                        "@langchain/openai": "^0.0.14",
                        "@langchain/anthropic": "^0.1.0",
                        "dotenv": "^16.3.1",
                        "express": "^4.18.2",
                    },
                }

                with open(package_json, "w") as f:
                    json.dump(package_config, f, indent=2)

                self.logger.info("Created package.json for LangChain.js project")

            # Create basic index.js file
            index_js = project_dir / "index.js"
            if not index_js.exists():
                js_content = """
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";
import express from "express";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(express.json());

// Initialize LangChain components
const llm = new ChatOpenAI({
    modelName: "gpt-3.5-turbo",
    temperature: 0.1,
});

// Security analysis endpoint
app.post("/analyze", async (req, res) => {
    try {
        const { data, prompt } = req.body;

        const messages = [
            new SystemMessage("You are a cybersecurity expert analyzing security data."),
            new HumanMessage(`Analyze this security data: ${data}. ${prompt || ""}`)
        ];

        const response = await llm.invoke(messages);

        res.json({
            success: true,
            analysis: response.content,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            timestamp: new Date().toISOString()
        });
    }
});

// Chain execution endpoint
app.post("/chain", async (req, res) => {
    try {
        const { input, chainType } = req.body;

        // Basic chain implementation
        const messages = [
            new SystemMessage("You are a security automation expert."),
            new HumanMessage(`Execute this security chain: ${input}`)
        ];

        const response = await llm.invoke(messages);

        res.json({
            success: true,
            result: response.content,
            chainType,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            timestamp: new Date().toISOString()
        });
    }
});

// Health check endpoint
app.get("/health", (req, res) => {
    res.json({
        status: "healthy",
        service: "LangChain.js for LANCELOTT",
        timestamp: new Date().toISOString()
    });
});

const PORT = process.env.PORT || 8101;
app.listen(PORT, () => {
    console.log(`LangChain.js service running on port ${PORT}`);
});
"""

                with open(index_js, "w") as f:
                    f.write(js_content)

                self.logger.info("Created index.js for LangChain.js project")

        except Exception as e:
            self.logger.error(f"LangChain.js project setup failed: {e}")

    async def _execute_js_script(
        self, script: str, options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute JavaScript script using LangChain.js"""
        try:
            # Execute Node.js script
            result = subprocess.run(
                ["node", "-e", script],
                cwd=str(self.executable_path),
                capture_output=True,
                text=True,
                timeout=options.get("timeout", 30),
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "script": script,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def _execute_chain(
        self, chain_input: str, options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute LangChain.js chain"""
        try:
            # Make HTTP request to LangChain.js service
            import httpx

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://localhost:{self.port}/chain",
                    json={
                        "input": chain_input,
                        "chainType": options.get("chain_type", "basic"),
                    },
                    timeout=options.get("timeout", 30),
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "timestamp": self._get_timestamp(),
                    }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def _execute_agent(
        self, agent_input: str, options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute LangChain.js agent"""
        try:
            # Make HTTP request to LangChain.js service
            import httpx

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://localhost:{self.port}/analyze",
                    json={"data": agent_input, "prompt": options.get("prompt", "")},
                    timeout=options.get("timeout", 30),
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "timestamp": self._get_timestamp(),
                    }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime

        return datetime.now().isoformat()


# Global wrapper instance
_langchainjs_wrapper = None


def get_langchainjs_wrapper() -> LangChainJSWrapper:
    """Get global LangChain.js wrapper instance"""
    global _langchainjs_wrapper
    if _langchainjs_wrapper is None:
        _langchainjs_wrapper = LangChainJSWrapper()
    return _langchainjs_wrapper
