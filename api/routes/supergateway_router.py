#!/usr/bin/env python3
"""
SuperGateway Router - MCP Gateway API Endpoints
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from api.auth import verify_token
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import StreamingResponse
from integrations.ai.supergateway_manager import get_supergateway_manager

router = APIRouter()


class MCPConnectionRequest(BaseModel):
    """Request model for MCP connection"""

    name: str
    command: List[str]
    args: Optional[List[str]] = None
    env: Optional[Dict[str, str]] = None
    timeout: Optional[int] = 30


class MCPToolExecuteRequest(BaseModel):
    """Request model for MCP tool execution"""

    connection_id: str
    tool_name: str
    arguments: Dict[str, Any]


class MCPStreamRequest(BaseModel):
    """Request model for MCP streaming"""

    connection_id: str
    messages: List[Dict[str, Any]]


@router.get("/health")
async def supergateway_health():
    """Check SuperGateway health"""
    try:
        manager = get_supergateway_manager()
        is_healthy = await manager.health_check()
        status = manager.get_status()

        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "service_info": status,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start")
async def start_supergateway(
    port: int = 3000,
    background_tasks: BackgroundTasks = None,
    token: str = Depends(verify_token),
):
    """Start SuperGateway MCP service"""
    try:
        manager = get_supergateway_manager()
        success = await manager.start_gateway(port)

        if success:
            return {
                "status": "started",
                "port": port,
                "base_url": manager.base_url,
                "timestamp": datetime.utcnow().isoformat(),
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to start SuperGateway")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_supergateway(token: str = Depends(verify_token)):
    """Stop SuperGateway MCP service"""
    try:
        manager = get_supergateway_manager()
        success = await manager.stop_gateway()

        return {
            "status": "stopped" if success else "error",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_supergateway_status():
    """Get SuperGateway status and information"""
    try:
        manager = get_supergateway_manager()
        status = manager.get_status()
        info = await manager.get_gateway_info()

        return {
            "status": status,
            "info": info,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mcp/connect")
async def create_mcp_connection(
    request: MCPConnectionRequest, token: str = Depends(verify_token)
):
    """Create MCP server connection"""
    try:
        manager = get_supergateway_manager()

        server_config = {
            "name": request.name,
            "command": request.command,
            "args": request.args or [],
            "env": request.env or {},
            "timeout": request.timeout,
        }

        result = await manager.create_mcp_connection(server_config)

        return {
            "connection": result,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mcp/tools/{connection_id}")
async def list_mcp_tools(connection_id: str, token: str = Depends(verify_token)):
    """List available MCP tools for a connection"""
    try:
        manager = get_supergateway_manager()
        tools = await manager.list_mcp_tools(connection_id)

        return {
            "connection_id": connection_id,
            "tools": tools,
            "count": len(tools),
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mcp/execute")
async def execute_mcp_tool(
    request: MCPToolExecuteRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Execute an MCP tool"""
    try:
        manager = get_supergateway_manager()

        result = await manager.execute_mcp_tool(
            request.connection_id, request.tool_name, request.arguments
        )

        # Log the execution
        background_tasks.add_task(
            log_mcp_execution,
            request.connection_id,
            request.tool_name,
            result.get("success", False),
        )

        return {
            "execution": result,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mcp/stream")
async def stream_mcp_interaction(
    request: MCPStreamRequest, token: str = Depends(verify_token)
):
    """Stream MCP interaction"""
    try:
        manager = get_supergateway_manager()

        async def generate_stream():
            async for data in manager.stream_mcp_interaction(
                request.connection_id, request.messages
            ):
                yield f"data: {data}\n\n"

        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache"},
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_gateway_info():
    """Get SuperGateway service information"""
    try:
        manager = get_supergateway_manager()
        info = await manager.get_gateway_info()

        return {
            "service": "SuperGateway",
            "version": "1.0.0",
            "description": "MCP Gateway for LANCELOTT Framework",
            "features": [
                "MCP Protocol Support",
                "Tool Execution Bridge",
                "Streaming Interactions",
                "Connection Management",
            ],
            "info": info,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def log_mcp_execution(connection_id: str, tool_name: str, success: bool):
    """Background task to log MCP tool executions"""
    import logging

    logger = logging.getLogger(__name__)
    status = "SUCCESS" if success else "FAILED"
    logger.info(
        f"MCP Tool Execution - Connection: {connection_id}, Tool: {tool_name}, Status: {status}"
    )


# Include health check at router level
@router.get("/")
async def supergateway_root():
    """SuperGateway service root endpoint"""
    return {
        "service": "SuperGateway",
        "description": "MCP Gateway for LANCELOTT Framework",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/start",
            "/stop",
            "/status",
            "/mcp/connect",
            "/mcp/tools/{connection_id}",
            "/mcp/execute",
            "/mcp/stream",
            "/info",
        ],
        "timestamp": datetime.utcnow().isoformat(),
    }
