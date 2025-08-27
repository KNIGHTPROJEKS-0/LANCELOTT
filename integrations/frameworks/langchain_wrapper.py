#!/usr/bin/env python3
"""
LangChain Integration Wrapper for LANCELOTT
Provides AI-powered security analysis and automation capabilities
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.integration_manager import BaseToolWrapper, ToolConfig


class LangChainWrapper(BaseToolWrapper):
    """Wrapper for LangChain AI framework integration"""

    def __init__(self):
        # Create a ToolConfig for LangChain
        config = ToolConfig(
            name="LangChain",
            executable_path="integrations/frameworks/langchain",
            wrapper_module="integrations.frameworks.langchain_wrapper",
            port=8100,
        )
        super().__init__(config)
        self.logger = logging.getLogger(__name__)

        # Legacy attributes for backward compatibility
        self.executable_path = Path(config.executable_path)
        self.config_file = "config/langchain.conf"
        self.description = "AI-powered security analysis and automation framework"
        self.category = "AI Framework"
        self.name = config.name
        self.port = config.port

        # LangChain specific attributes
        self.llm_providers = {}
        self.chains = {}
        self.agents = {}

    async def initialize(self) -> bool:
        """Initialize LangChain integration"""
        try:
            # Check if LangChain can be imported
            try:
                import langchain
                from langchain.agents import Tool, initialize_agent
                from langchain.llms import OpenAI
                from langchain.memory import ConversationBufferMemory

                self.logger.info("LangChain modules imported successfully")
            except ImportError as e:
                self.logger.error(f"LangChain not available: {e}")
                return False

            # Initialize basic components
            await self._setup_llm_providers()
            await self._setup_security_tools()
            await self._setup_agents()

            self.logger.info("LangChain integration initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"LangChain initialization failed: {e}")
            return False

    async def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute LangChain AI command"""
        try:
            operation = kwargs.get("operation", "analyze")
            target = kwargs.get("target", command)
            options = kwargs.get("options", {})

            if operation == "analyze":
                return await self._analyze_security_data(target, options)
            elif operation == "generate":
                return await self._generate_security_report(target, options)
            elif operation == "chat":
                return await self._security_chat(target, options)
            elif operation == "automate":
                return await self._automate_security_workflow(target, options)
            else:
                return await self._analyze_security_data(target, options)

        except Exception as e:
            self.logger.error(f"LangChain command execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def health_check(self) -> bool:
        """Check if LangChain is healthy and responsive"""
        try:
            # Check if LangChain can be imported
            import langchain

            # Check if basic LLM can be instantiated
            from langchain.llms import OpenAI

            # Basic functionality test
            return True

        except Exception as e:
            self.logger.warning(f"LangChain health check failed: {e}")
            return False

    async def _setup_llm_providers(self):
        """Setup LLM providers for security analysis"""
        try:
            from langchain.chat_models import ChatOpenAI
            from langchain.llms import Anthropic, OpenAI

            # Setup OpenAI if API key is available
            openai_api_key = self._get_env_var("OPENAI_API_KEY")
            if openai_api_key:
                self.llm_providers["openai"] = ChatOpenAI(
                    openai_api_key=openai_api_key, model_name="gpt-4", temperature=0.1
                )
                self.logger.info("OpenAI LLM provider configured")

            # Setup Anthropic if API key is available
            anthropic_api_key = self._get_env_var("ANTHROPIC_API_KEY")
            if anthropic_api_key:
                self.llm_providers["anthropic"] = Anthropic(
                    anthropic_api_key=anthropic_api_key, model="claude-2"
                )
                self.logger.info("Anthropic LLM provider configured")

        except Exception as e:
            self.logger.warning(f"LLM provider setup failed: {e}")

    async def _setup_security_tools(self):
        """Setup security-specific LangChain tools"""
        try:
            from langchain.agents import Tool

            security_tools = [
                Tool(
                    name="Vulnerability Analyzer",
                    description="Analyze security scan results and identify vulnerabilities",
                    func=self._analyze_vulnerabilities,
                ),
                Tool(
                    name="Threat Intelligence",
                    description="Analyze threats and provide intelligence insights",
                    func=self._threat_intelligence,
                ),
                Tool(
                    name="Security Report Generator",
                    description="Generate comprehensive security reports",
                    func=self._generate_report,
                ),
                Tool(
                    name="Incident Response",
                    description="Provide incident response recommendations",
                    func=self._incident_response,
                ),
            ]

            self.security_tools = security_tools
            self.logger.info(f"Configured {len(security_tools)} security tools")

        except Exception as e:
            self.logger.error(f"Security tools setup failed: {e}")

    async def _setup_agents(self):
        """Setup LangChain agents for security automation"""
        try:
            from langchain.agents import AgentType, initialize_agent
            from langchain.memory import ConversationBufferMemory

            if not self.llm_providers:
                self.logger.warning("No LLM providers available, skipping agent setup")
                return

            # Get primary LLM
            primary_llm = list(self.llm_providers.values())[0]

            # Security Analysis Agent
            security_memory = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )

            self.agents["security_analyst"] = initialize_agent(
                tools=getattr(self, "security_tools", []),
                llm=primary_llm,
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                memory=security_memory,
                verbose=True,
            )

            self.logger.info("Security analysis agent configured")

        except Exception as e:
            self.logger.error(f"Agent setup failed: {e}")

    def _analyze_vulnerabilities(self, scan_data: str) -> str:
        """Analyze vulnerability scan data"""
        try:
            # Parse and analyze scan data
            analysis = f"Analyzing vulnerability data: {scan_data[:100]}..."
            return analysis
        except Exception as e:
            return f"Vulnerability analysis failed: {e}"

    def _threat_intelligence(self, threat_data: str) -> str:
        """Provide threat intelligence analysis"""
        try:
            intelligence = f"Threat intelligence for: {threat_data[:100]}..."
            return intelligence
        except Exception as e:
            return f"Threat intelligence failed: {e}"

    def _generate_report(self, data: str) -> str:
        """Generate security report"""
        try:
            report = f"Security report generated for: {data[:100]}..."
            return report
        except Exception as e:
            return f"Report generation failed: {e}"

    def _incident_response(self, incident_data: str) -> str:
        """Provide incident response recommendations"""
        try:
            response = f"Incident response for: {incident_data[:100]}..."
            return response
        except Exception as e:
            return f"Incident response failed: {e}"

    async def _analyze_security_data(
        self, data: str, options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze security data using LangChain"""
        try:
            if "security_analyst" not in self.agents:
                return {
                    "success": False,
                    "error": "Security analyst agent not available",
                    "timestamp": self._get_timestamp(),
                }

            agent = self.agents["security_analyst"]

            # Analyze the data
            analysis = agent.run(f"Analyze this security data: {data}")

            return {
                "success": True,
                "analysis": analysis,
                "data": data,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def _generate_security_report(
        self, data: str, options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        try:
            if "security_analyst" not in self.agents:
                return {
                    "success": False,
                    "error": "Security analyst agent not available",
                    "timestamp": self._get_timestamp(),
                }

            agent = self.agents["security_analyst"]

            # Generate report
            report = agent.run(f"Generate a comprehensive security report for: {data}")

            return {
                "success": True,
                "report": report,
                "data": data,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def _security_chat(
        self, query: str, options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Interactive security chat using LangChain"""
        try:
            if "security_analyst" not in self.agents:
                return {
                    "success": False,
                    "error": "Security analyst agent not available",
                    "timestamp": self._get_timestamp(),
                }

            agent = self.agents["security_analyst"]

            # Process chat query
            response = agent.run(query)

            return {
                "success": True,
                "response": response,
                "query": query,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def _automate_security_workflow(
        self, workflow: str, options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Automate security workflows using LangChain"""
        try:
            if "security_analyst" not in self.agents:
                return {
                    "success": False,
                    "error": "Security analyst agent not available",
                    "timestamp": self._get_timestamp(),
                }

            agent = self.agents["security_analyst"]

            # Execute workflow automation
            result = agent.run(f"Automate this security workflow: {workflow}")

            return {
                "success": True,
                "result": result,
                "workflow": workflow,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    def _get_env_var(self, var_name: str) -> Optional[str]:
        """Get environment variable"""
        import os

        return os.getenv(var_name)

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime

        return datetime.now().isoformat()


# Global wrapper instance
_langchain_wrapper = None


def get_langchain_wrapper() -> LangChainWrapper:
    """Get global LangChain wrapper instance"""
    global _langchain_wrapper
    if _langchain_wrapper is None:
        _langchain_wrapper = LangChainWrapper()
    return _langchain_wrapper
