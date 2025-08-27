#!/usr/bin/env python3
"""
SuperGateway API routes for CERBERUS-FANGS LANCELOTT
Provides REST API endpoints for managing SuperGateway MCP services
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from api.auth import verify_token
from core.logger_config import setup_logging
from core.supergateway_manager import SuperGatewayManager
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials

logger = setup_logging()
router = APIRouter(prefix="/supergateway", tags=["SuperGateway"])

# Initialize SuperGateway manager
gateway_manager = SuperGatewayManager()


# Pydantic models
class StdioToSseGatewayRequest(BaseModel):
    gateway_id: str = Field(..., description="Unique identifier for this gateway")
    stdio_command: str = Field(..., description="Command to run the MCP stdio server")
    port: int = Field(default=8000, description="Port to listen on")
    base_url: Optional[str] = Field(None, description="Base URL for the gateway")
    sse_path: str = Field(default="/sse", description="Path for SSE subscriptions")
    message_path: str = Field(
        default="/message", description="Path for message posting"
    )
    cors: bool = Field(default=True, description="Enable CORS")
    headers: Optional[List[str]] = Field(None, description="Additional headers")


class SseToStdioGatewayRequest(BaseModel):
    gateway_id: str = Field(..., description="Unique identifier for this gateway")
    sse_url: str = Field(..., description="SSE URL to connect to")
    headers: Optional[List[str]] = Field(None, description="Additional headers")


class GatewayResponse(BaseModel):
    gateway_id: str
    status: str
    config: Dict[str, Any]
    endpoints: Optional[Dict[str, str]] = None


class GatewayListResponse(BaseModel):
    active_gateways: int
    gateways: Dict[str, Dict[str, Any]]


# Routes
@router.get("/status")
async def get_supergateway_status(
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Get SuperGateway service status"""
    try:
        is_available = await gateway_manager.is_available()
        gateways = await gateway_manager.list_gateways()

        return {
            "service": "SuperGateway",
            "status": "available" if is_available else "unavailable",
            "version": "3.4.0",
            "description": "MCP stdio server gateway for SSE and WebSocket connections",
            "active_gateways": gateways["active_gateways"],
            "features": [
                "stdio → SSE gateway",
                "SSE → stdio gateway",
                "stdio → WebSocket gateway",
                "Streamable HTTP support",
                "CORS support",
                "Custom headers support",
            ],
        }
    except Exception as e:
        logger.error(f"Error getting SuperGateway status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gateway/stdio-to-sse", response_model=GatewayResponse)
async def create_stdio_to_sse_gateway(
    request: StdioToSseGatewayRequest,
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Create a stdio → SSE gateway"""
    try:
        if not await gateway_manager.is_available():
            raise HTTPException(status_code=503, detail="SuperGateway is not available")

        result = await gateway_manager.start_stdio_to_sse_gateway(
            gateway_id=request.gateway_id,
            stdio_command=request.stdio_command,
            port=request.port,
            base_url=request.base_url,
            sse_path=request.sse_path,
            message_path=request.message_path,
            cors=request.cors,
            headers=request.headers,
        )

        return GatewayResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating stdio→SSE gateway: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gateway/sse-to-stdio", response_model=GatewayResponse)
async def create_sse_to_stdio_gateway(
    request: SseToStdioGatewayRequest,
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Create an SSE → stdio gateway"""
    try:
        if not await gateway_manager.is_available():
            raise HTTPException(status_code=503, detail="SuperGateway is not available")

        result = await gateway_manager.start_sse_to_stdio_gateway(
            gateway_id=request.gateway_id,
            sse_url=request.sse_url,
            headers=request.headers,
        )

        return GatewayResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating SSE→stdio gateway: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gateways", response_model=GatewayListResponse)
async def list_gateways(
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """List all active gateways"""
    try:
        result = await gateway_manager.list_gateways()
        return GatewayListResponse(**result)

    except Exception as e:
        logger.error(f"Error listing gateways: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gateway/{gateway_id}")
async def get_gateway_status(
    gateway_id: str, credentials: HTTPAuthorizationCredentials = Security(verify_token)
):
    """Get status of a specific gateway"""
    try:
        result = await gateway_manager.get_gateway_status(gateway_id)
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting gateway status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/gateway/{gateway_id}")
async def stop_gateway(
    gateway_id: str, credentials: HTTPAuthorizationCredentials = Security(verify_token)
):
    """Stop a running gateway"""
    try:
        result = await gateway_manager.stop_gateway(gateway_id)
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error stopping gateway: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/gateways/cleanup")
async def cleanup_all_gateways(
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Stop all running gateways"""
    try:
        await gateway_manager.cleanup_all()
        return {"status": "success", "message": "All gateways stopped and cleaned up"}

    except Exception as e:
        logger.error(f"Error during gateway cleanup: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/examples")
async def get_gateway_examples(
    credentials: HTTPAuthorizationCredentials = Security(verify_token),
):
    """Get example configurations for common use cases"""
    return {
        "examples": {
            "filesystem_server": {
                "description": "Expose filesystem MCP server over SSE",
                "stdio_command": "npx -y @modelcontextprotocol/server-filesystem ./my-folder",
                "port": 8001,
                "use_case": "File system access for AI agents",
            },
            "git_server": {
                "description": "Expose Git MCP server over SSE",
                "stdio_command": "uvx mcp-server-git",
                "port": 8002,
                "use_case": "Git repository management for AI agents",
            },
            "custom_mcp": {
                "description": "Custom MCP server",
                "stdio_command": "python custom_mcp_server.py",
                "port": 8003,
                "use_case": "Custom functionality through MCP protocol",
            },
        },
        "common_configurations": {
            "cors_enabled": {
                "cors": True,
                "description": "Enable CORS for web browser access",
            },
            "with_auth_header": {
                "headers": ["Authorization: Bearer your-token-here"],
                "description": "Add authentication header",
            },
            "custom_paths": {
                "sse_path": "/events",
                "message_path": "/send",
                "description": "Custom endpoint paths",
            },
        },
    }
