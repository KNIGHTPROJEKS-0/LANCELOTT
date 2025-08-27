#!/usr/bin/env python3
"""
SuperCompat API routes for CERBERUS-FANGS LANCELOTT
Provides REST API endpoints for managing SuperCompat AI provider compatibility
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from api.auth import verify_token
from core.logger_config import setup_logging
from core.supercompat_manager import SuperCompatManager
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials

logger = setup_logging()
router = APIRouter(prefix="/supercompat", tags=["SuperCompat"])

# Initialize SuperCompat manager
compat_manager = SuperCompatManager()


# Pydantic models
class CreateSessionRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for this session")
    provider: str = Field(
        ..., description="AI provider (openai, anthropic, groq, mistral)"
    )
    api_key: str = Field(..., description="API key for the provider")
    model: Optional[str] = Field(None, description="Model name (provider-specific)")
    additional_config: Optional[Dict] = Field(
        None, description="Additional provider configuration"
    )


class CompletionMessage(BaseModel):
    role: str = Field(..., description="Message role (system, user, assistant)")
    content: str = Field(..., description="Message content")


class CompletionRequest(BaseModel):
    session_id: str = Field(..., description="Session ID to use")
    messages: List[CompletionMessage] = Field(..., description="Conversation messages")
    temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="Sampling temperature"
    )
    max_tokens: Optional[int] = Field(
        None, gt=0, description="Maximum tokens to generate"
    )
    stream: bool = Field(default=False, description="Enable streaming response")


class SessionResponse(BaseModel):
    session_id: str
    status: str
    provider: str
    model: Optional[str]
    created_at: float


class CompletionResponse(BaseModel):
    session_id: str
    status: str
    response: Dict[str, Any]
    request_count: int


class SessionListResponse(BaseModel):
    active_sessions: int
    sessions: Dict[str, Dict[str, Any]]


# Routes
@router.get("/status")
async def get_supercompat_status(
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Get SuperCompat service status"""
    try:
        is_available = await compat_manager.is_available()
        sessions = await compat_manager.list_sessions()
        supported_providers = await compat_manager.get_supported_providers()

        return {
            "service": "SuperCompat",
            "status": "available" if is_available else "unavailable",
            "version": "3.0.0",
            "description": "AI provider compatibility layer - use any provider with OpenAI-compatible API",
            "active_sessions": sessions["active_sessions"],
            "supported_providers": supported_providers,
            "features": [
                "Multi-provider AI compatibility",
                "OpenAI-compatible API",
                "Session management",
                "Provider abstraction",
                "Streaming support",
                "Custom model configuration",
            ],
        }
    except Exception as e:
        logger.error(f"Error getting SuperCompat status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers")
async def get_supported_providers(
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Get list of supported AI providers"""
    try:
        providers = await compat_manager.get_supported_providers()

        provider_details = {
            "openai": {
                "name": "OpenAI",
                "description": "GPT models and more",
                "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o"],
            },
            "anthropic": {
                "name": "Anthropic",
                "description": "Claude models",
                "models": [
                    "claude-3-opus",
                    "claude-3-sonnet",
                    "claude-3-haiku",
                    "claude-2",
                ],
            },
            "groq": {
                "name": "Groq",
                "description": "High-speed inference",
                "models": ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"],
            },
            "mistral": {
                "name": "Mistral AI",
                "description": "Mistral models",
                "models": ["mistral-medium", "mistral-small", "mistral-tiny"],
            },
        }

        return {
            "supported_providers": providers,
            "provider_details": {
                provider: details
                for provider, details in provider_details.items()
                if provider in providers
            },
        }

    except Exception as e:
        logger.error(f"Error getting supported providers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session", response_model=SessionResponse)
async def create_session(
    request: CreateSessionRequest,
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Create a new SuperCompat session for an AI provider"""
    try:
        # Build if needed
        if not await compat_manager.build_if_needed():
            raise HTTPException(
                status_code=503,
                detail="SuperCompat is not available or failed to build",
            )

        result = await compat_manager.create_client_session(
            session_id=request.session_id,
            provider=request.provider,
            api_key=request.api_key,
            model=request.model,
            additional_config=request.additional_config,
        )

        return SessionResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating SuperCompat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/completion", response_model=CompletionResponse)
async def create_completion(
    request: CompletionRequest,
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Execute a completion request using SuperCompat"""
    try:
        # Convert Pydantic models to dict for the manager
        messages = [msg.dict() for msg in request.messages]

        result = await compat_manager.execute_completion(
            session_id=request.session_id,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream,
        )

        return CompletionResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing completion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """List all active SuperCompat sessions"""
    try:
        result = await compat_manager.list_sessions()
        return SessionListResponse(**result)

    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session_info(
    session_id: str, credentials: HTTPAuthorizationCredentials = Security(verify_token)
):
    """Get information about a specific session"""
    try:
        result = await compat_manager.get_session_info(session_id)
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/session/{session_id}")
async def delete_session(
    session_id: str, credentials: HTTPAuthorizationCredentials = Security(verify_token)
):
    """Delete a SuperCompat session"""
    try:
        result = await compat_manager.delete_session(session_id)
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/cleanup")
async def cleanup_all_sessions(
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Clean up all SuperCompat sessions"""
    try:
        await compat_manager.cleanup_all()
        return {"status": "success", "message": "All sessions cleaned up"}

    except Exception as e:
        logger.error(f"Error during session cleanup: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/examples")
async def get_usage_examples(
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Get usage examples for different providers"""
    return {
        "examples": {
            "openai_session": {
                "session_id": "openai-session-1",
                "provider": "openai",
                "api_key": "your-openai-api-key",
                "model": "gpt-4",
                "description": "Standard OpenAI GPT-4 session",
            },
            "anthropic_session": {
                "session_id": "claude-session-1",
                "provider": "anthropic",
                "api_key": "your-anthropic-api-key",
                "model": "claude-3-sonnet",
                "description": "Anthropic Claude session",
            },
            "groq_session": {
                "session_id": "groq-session-1",
                "provider": "groq",
                "api_key": "your-groq-api-key",
                "model": "llama2-70b-4096",
                "description": "High-speed Groq inference",
            },
            "mistral_session": {
                "session_id": "mistral-session-1",
                "provider": "mistral",
                "api_key": "your-mistral-api-key",
                "model": "mistral-medium",
                "description": "Mistral AI session",
            },
        },
        "completion_example": {
            "messages": [
                {"role": "system", "content": "You are a helpful security analyst."},
                {"role": "user", "content": "Explain what an SQL injection attack is."},
            ],
            "temperature": 0.7,
            "max_tokens": 500,
            "stream": False,
        },
        "use_cases": [
            "Security analysis and recommendations",
            "Threat intelligence research",
            "Automated report generation",
            "Multi-provider AI comparison",
            "Failover between providers",
            "Cost optimization across providers",
        ],
    }
