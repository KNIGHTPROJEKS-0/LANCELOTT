#!/usr/bin/env python3
"""
SuperCompat wrapper for CERBERUS-FANGS LANCELOTT
Provides Python interface to SuperCompat AI provider compatibility layer
"""

import asyncio
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.logger_config import setup_logging

logger = setup_logging()


class SuperCompatManager:
    def __init__(self, base_path: str = "./SuperCompat"):
        self.base_path = Path(base_path)
        self.package_path = self.base_path / "packages" / "supercompat"
        self.active_sessions: Dict[str, Dict] = {}

    async def is_available(self) -> bool:
        """Check if SuperCompat is available and built"""
        try:
            dist_path = self.package_path / "dist" / "index.js"
            package_json = self.package_path / "package.json"
            return dist_path.exists() and package_json.exists()
        except Exception as e:
            logger.error(f"Error checking SuperCompat availability: {e}")
            return False

    async def build_if_needed(self) -> bool:
        """Build SuperCompat if not already built"""
        try:
            if await self.is_available():
                return True

            # Build the package
            result = subprocess.run(
                ["npm", "run", "build"],
                cwd=self.package_path,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                logger.error(f"SuperCompat build failed: {result.stderr}")
                return False

            return await self.is_available()

        except Exception as e:
            logger.error(f"Error building SuperCompat: {e}")
            return False

    async def create_client_session(
        self,
        session_id: str,
        provider: str,
        api_key: str,
        model: Optional[str] = None,
        additional_config: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Create a new SuperCompat client session"""
        try:
            if not await self.build_if_needed():
                raise RuntimeError("SuperCompat is not available or failed to build")

            if session_id in self.active_sessions:
                raise ValueError(f"Session {session_id} already exists")

            config = {
                "provider": provider,
                "api_key": api_key,
                "model": model,
                "additional_config": additional_config or {},
            }

            # Validate provider
            supported_providers = ["openai", "anthropic", "groq", "mistral"]
            if provider.lower() not in supported_providers:
                raise ValueError(
                    f"Provider {provider} not supported. Supported: {supported_providers}"
                )

            self.active_sessions[session_id] = {
                "config": config,
                "created_at": asyncio.get_event_loop().time(),
                "requests_count": 0,
            }

            logger.info(
                f"Created SuperCompat session {session_id} for provider {provider}"
            )

            return {
                "session_id": session_id,
                "status": "created",
                "provider": provider,
                "model": model,
                "created_at": self.active_sessions[session_id]["created_at"],
            }

        except Exception as e:
            logger.error(f"Error creating SuperCompat session {session_id}: {e}")
            raise

    async def execute_completion(
        self,
        session_id: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """Execute a completion request using SuperCompat"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"Session {session_id} not found")

            session = self.active_sessions[session_id]
            session["requests_count"] += 1

            # Create a temporary Node.js script to execute the request
            script_content = self._generate_completion_script(
                session["config"], messages, temperature, max_tokens, stream
            )

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".mjs", delete=False
            ) as f:
                f.write(script_content)
                script_path = f.name

            try:
                # Execute the script
                result = subprocess.run(
                    ["node", script_path],
                    cwd=self.package_path,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )

                if result.returncode != 0:
                    raise RuntimeError(f"SuperCompat execution failed: {result.stderr}")

                # Parse the JSON response
                response_data = json.loads(result.stdout)

                logger.info(f"SuperCompat completion executed for session {session_id}")

                return {
                    "session_id": session_id,
                    "status": "success",
                    "response": response_data,
                    "request_count": session["requests_count"],
                }

            finally:
                # Clean up the temporary script
                os.unlink(script_path)

        except Exception as e:
            logger.error(
                f"Error executing SuperCompat completion for session {session_id}: {e}"
            )
            raise

    def _generate_completion_script(
        self,
        config: Dict,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: Optional[int],
        stream: bool,
    ) -> str:
        """Generate a Node.js script for executing the completion"""

        # Determine the appropriate adapter based on provider
        provider_adapters = {
            "openai": "openaiClientAdapter",
            "anthropic": "anthropicClientAdapter",
            "groq": "groqClientAdapter",
            "mistral": "mistralClientAdapter",
        }

        adapter = provider_adapters.get(config["provider"].lower())
        if not adapter:
            raise ValueError(f"No adapter found for provider {config['provider']}")

        # Generate the script
        script = f"""
import {{ supercompat, {adapter}, completionsRunAdapter }} from './dist/index.js';

async function main() {{
    try {{
        // Initialize the client based on provider
        let clientConfig;

        switch ('{config["provider"].lower()}') {{
            case 'openai':
                const {{ default: OpenAI }} = await import('openai');
                clientConfig = {adapter}({{
                    openai: new OpenAI({{ apiKey: '{config["api_key"]}' }})
                }});
                break;
            case 'anthropic':
                const {{ default: Anthropic }} = await import('@anthropic-ai/sdk');
                clientConfig = {adapter}({{
                    anthropic: new Anthropic({{ apiKey: '{config["api_key"]}' }})
                }});
                break;
            case 'groq':
                const {{ default: Groq }} = await import('groq-sdk');
                clientConfig = {adapter}({{
                    groq: new Groq({{ apiKey: '{config["api_key"]}' }})
                }});
                break;
            case 'mistral':
                const {{ default: MistralAI }} = await import('@mistralai/mistralai');
                clientConfig = {adapter}({{
                    mistral: new MistralAI({{ apiKey: '{config["api_key"]}' }})
                }});
                break;
            default:
                throw new Error('Unsupported provider: {config["provider"]}');
        }}

        // Create SuperCompat client
        const client = supercompat({{
            client: clientConfig,
            runAdapter: completionsRunAdapter()
        }});

        // Execute the completion
        const completion = await client.chat.completions.create({{
            model: '{config.get("model", "gpt-3.5-turbo")}',
            messages: {json.dumps(messages)},
            temperature: {temperature},
            {f'max_tokens: {max_tokens},' if max_tokens else ''}
            stream: {str(stream).lower()}
        }});

        console.log(JSON.stringify({{
            success: true,
            completion: completion
        }}));

    }} catch (error) {{
        console.log(JSON.stringify({{
            success: false,
            error: error.message,
            stack: error.stack
        }}));
        process.exit(1);
    }}
}}

main();
"""
        return script

    async def list_sessions(self) -> Dict[str, Any]:
        """List all active SuperCompat sessions"""
        return {
            "active_sessions": len(self.active_sessions),
            "sessions": {
                session_id: {
                    "provider": session["config"]["provider"],
                    "model": session["config"]["model"],
                    "created_at": session["created_at"],
                    "requests_count": session["requests_count"],
                }
                for session_id, session in self.active_sessions.items()
            },
        }

    async def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get information about a specific session"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.active_sessions[session_id]

        return {
            "session_id": session_id,
            "provider": session["config"]["provider"],
            "model": session["config"]["model"],
            "created_at": session["created_at"],
            "requests_count": session["requests_count"],
            "uptime": asyncio.get_event_loop().time() - session["created_at"],
        }

    async def delete_session(self, session_id: str) -> Dict[str, Any]:
        """Delete a SuperCompat session"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.active_sessions.pop(session_id)

        logger.info(f"Deleted SuperCompat session {session_id}")

        return {
            "session_id": session_id,
            "status": "deleted",
            "final_request_count": session["requests_count"],
        }

    async def get_supported_providers(self) -> List[str]:
        """Get list of supported AI providers"""
        return ["openai", "anthropic", "groq", "mistral"]

    async def cleanup_all(self):
        """Clean up all sessions"""
        session_ids = list(self.active_sessions.keys())
        for session_id in session_ids:
            try:
                await self.delete_session(session_id)
            except Exception as e:
                logger.error(f"Error cleaning up session {session_id}: {e}")

        logger.info("SuperCompat cleanup completed")
