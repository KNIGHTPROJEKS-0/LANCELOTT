#!/usr/bin/env python3
"""
CliWrap FastAPI Router
.NET command line process wrapper endpoints
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from fastapi import APIRouter, BackgroundTasks, HTTPException
from integrations.tools.cliwrap_wrapper import get_cliwrap_wrapper

router = APIRouter()
logger = logging.getLogger(__name__)


# Pydantic models for request/response
class CliWrapRequest(BaseModel):
    target: str
    operation: Optional[str] = "build"
    options: Optional[Dict[str, Any]] = {}


class CommandWrapRequest(BaseModel):
    command: str
    arguments: Optional[List[str]] = []
    options: Optional[Dict[str, Any]] = {}


class BatchCommandRequest(BaseModel):
    commands: List[Dict[str, Any]]
    options: Optional[Dict[str, Any]] = {}


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        wrapper = get_cliwrap_wrapper()
        deps = await wrapper.check_dependencies()
        return {
            "status": "healthy" if deps["success"] else "unhealthy",
            "tool": "CliWrap",
            "dependencies": deps,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_info():
    """Get CliWrap tool information"""
    wrapper = get_cliwrap_wrapper()
    return {
        "name": wrapper.name,
        "description": wrapper.description,
        "category": wrapper.category,
        "executable_path": wrapper.executable_path,
        "config_file": wrapper.config_file,
        "port": wrapper.port,
        "capabilities": [
            "Command line wrapping",
            "Process execution",
            "Batch command execution",
            ".NET integration",
            "Cross-platform support",
        ],
    }


@router.post("/execute")
async def execute_cliwrap(request: CliWrapRequest, background_tasks: BackgroundTasks):
    """Execute CliWrap operation"""
    try:
        wrapper = get_cliwrap_wrapper()

        # Execute in background if requested
        if request.options.get("background", False):
            background_tasks.add_task(
                wrapper.execute_scan, request.target, request.options
            )
            return {
                "message": "CliWrap operation started in background",
                "target": request.target,
                "operation": request.operation,
            }

        result = await wrapper.execute_scan(request.target, request.options)
        return result

    except Exception as e:
        logger.error(f"CliWrap execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/wrap")
async def wrap_command(request: CommandWrapRequest, background_tasks: BackgroundTasks):
    """Wrap a command using CliWrap"""
    try:
        wrapper = get_cliwrap_wrapper()

        # Execute in background if requested
        if request.options.get("background", False):
            background_tasks.add_task(
                wrapper.wrap_command,
                request.command,
                request.arguments,
                request.options,
            )
            return {
                "message": "Command wrapping started in background",
                "command": request.command,
                "arguments": request.arguments,
            }

        result = await wrapper.wrap_command(
            request.command, request.arguments, request.options
        )
        return result

    except Exception as e:
        logger.error(f"Command wrapping failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch")
async def execute_batch_commands(
    request: BatchCommandRequest, background_tasks: BackgroundTasks
):
    """Execute multiple commands in batch"""
    try:
        wrapper = get_cliwrap_wrapper()

        # Always execute batch operations in background
        background_tasks.add_task(
            wrapper.execute_batch_commands, request.commands, request.options
        )

        return {
            "message": "Batch command execution started in background",
            "total_commands": len(request.commands),
        }

    except Exception as e:
        logger.error(f"Batch command execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/build")
async def build_project(background_tasks: BackgroundTasks):
    """Build the CliWrap project"""
    try:
        wrapper = get_cliwrap_wrapper()

        request = CliWrapRequest(
            target="", operation="build", options={"background": False}
        )

        result = await wrapper.execute_scan("", {"operation": "build"})
        return result

    except Exception as e:
        logger.error(f"Project build failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
async def test_project(background_tasks: BackgroundTasks):
    """Test the CliWrap project"""
    try:
        wrapper = get_cliwrap_wrapper()

        background_tasks.add_task(wrapper.execute_scan, "", {"operation": "test"})

        return {"message": "Project testing started in background"}

    except Exception as e:
        logger.error(f"Project testing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/examples")
async def get_examples():
    """Get example commands for CliWrap"""
    return {
        "examples": [
            {
                "name": "Simple command",
                "command": "echo",
                "arguments": ["Hello, World!"],
                "description": "Execute a simple echo command",
            },
            {
                "name": "List files",
                "command": "ls",
                "arguments": ["-la"],
                "description": "List files in current directory",
            },
            {
                "name": "Python script",
                "command": "python3",
                "arguments": ["-c", "print('Hello from Python')"],
                "description": "Execute Python code",
            },
            {
                "name": "Nmap scan",
                "command": "nmap",
                "arguments": ["-sV", "127.0.0.1"],
                "description": "Perform network scan using nmap",
            },
            {
                "name": "Git status",
                "command": "git",
                "arguments": ["status"],
                "description": "Check git repository status",
            },
        ]
    }


@router.get("/status")
async def get_status():
    """Get CliWrap wrapper status"""
    try:
        wrapper = get_cliwrap_wrapper()
        deps = await wrapper.check_dependencies()

        return {
            "tool": "CliWrap",
            "status": "ready" if deps["success"] else "not_ready",
            "dependencies": deps,
            "capabilities": {
                "command_wrapping": True,
                "batch_execution": True,
                "dotnet_integration": True,
                "cross_platform": True,
            },
        }

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
