#!/usr/bin/env python3
"""
Crush CLI File Manager FastAPI Router
Main tool orchestrator and file manager endpoints
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from fastapi import APIRouter, BackgroundTasks, HTTPException
from integrations.tools.crush_wrapper import get_crush_wrapper

router = APIRouter()
logger = logging.getLogger(__name__)


# Pydantic models for request/response
class CrushRequest(BaseModel):
    target: str
    operation: Optional[str] = "browse"
    options: Optional[Dict[str, Any]] = {}


class OrchestrationRequest(BaseModel):
    tools: List[str]
    target: str
    options: Optional[Dict[str, Any]] = {}


class WorkflowRequest(BaseModel):
    workflow_name: str
    tools: List[str]
    target: str


class WorkflowExecuteRequest(BaseModel):
    workflow_path: str


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        wrapper = get_crush_wrapper()
        deps = await wrapper.check_dependencies()
        return {
            "status": "healthy" if deps["success"] else "unhealthy",
            "tool": "Crush",
            "dependencies": deps,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_info():
    """Get Crush tool information"""
    wrapper = get_crush_wrapper()
    return {
        "name": wrapper.name,
        "description": wrapper.description,
        "category": wrapper.category,
        "executable_path": wrapper.executable_path,
        "config_file": wrapper.config_file,
        "port": wrapper.port,
        "capabilities": [
            "File management",
            "Tool orchestration",
            "Workflow creation",
            "Command execution",
            "Security tool coordination",
        ],
    }


@router.post("/execute")
async def execute_crush(request: CrushRequest, background_tasks: BackgroundTasks):
    """Execute Crush file manager operation"""
    try:
        wrapper = get_crush_wrapper()

        # Execute the scan in background if it's a long operation
        if request.options.get("background", False):
            background_tasks.add_task(
                wrapper.execute_scan, request.target, request.options
            )
            return {
                "message": "Crush operation started in background",
                "target": request.target,
                "operation": request.operation,
            }

        result = await wrapper.execute_scan(request.target, request.options)
        return result

    except Exception as e:
        logger.error(f"Crush execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/orchestrate")
async def orchestrate_tools(
    request: OrchestrationRequest, background_tasks: BackgroundTasks
):
    """Orchestrate multiple security tools"""
    try:
        wrapper = get_crush_wrapper()

        # Execute orchestration in background if requested
        if request.options.get("background", False):
            background_tasks.add_task(
                wrapper.orchestrate_tools,
                request.tools,
                request.target,
                request.options,
            )
            return {
                "message": "Tool orchestration started in background",
                "tools": request.tools,
                "target": request.target,
            }

        result = await wrapper.orchestrate_tools(
            request.tools, request.target, request.options
        )
        return result

    except Exception as e:
        logger.error(f"Tool orchestration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflow/create")
async def create_workflow(request: WorkflowRequest):
    """Create a new security testing workflow"""
    try:
        wrapper = get_crush_wrapper()
        result = await wrapper.create_workflow(
            request.workflow_name, request.tools, request.target
        )
        return result

    except Exception as e:
        logger.error(f"Workflow creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflow/execute")
async def execute_workflow(
    request: WorkflowExecuteRequest, background_tasks: BackgroundTasks
):
    """Execute a saved workflow"""
    try:
        wrapper = get_crush_wrapper()

        # Execute workflow in background
        background_tasks.add_task(wrapper.execute_workflow, request.workflow_path)

        return {
            "message": "Workflow execution started in background",
            "workflow_path": request.workflow_path,
        }

    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tools/available")
async def get_available_tools():
    """Get list of available security tools for orchestration"""
    return {
        "tools": [
            {"name": "nmap", "description": "Network scanner", "category": "Network"},
            {
                "name": "feroxbuster",
                "description": "Content discovery",
                "category": "Web",
            },
            {
                "name": "intel-scan",
                "description": "Intelligence gathering",
                "category": "OSINT",
            },
            {
                "name": "redeye",
                "description": "Red team analysis",
                "category": "Red Team",
            },
            {
                "name": "mhddos",
                "description": "DDoS testing",
                "category": "Stress Testing",
            },
            {
                "name": "argus",
                "description": "Web application scanner",
                "category": "Web",
            },
            {
                "name": "sherlock",
                "description": "Username investigation",
                "category": "OSINT",
            },
            {"name": "web-check", "description": "Website analysis", "category": "Web"},
        ]
    }


@router.get("/workflows/list")
async def list_workflows():
    """List available workflows"""
    try:
        import json
        from pathlib import Path

        workflows_dir = Path("workflows")
        if not workflows_dir.exists():
            return {"workflows": []}

        workflows = []
        for workflow_file in workflows_dir.glob("*.json"):
            try:
                with open(workflow_file, "r") as f:
                    workflow_data = json.load(f)
                    workflows.append(
                        {
                            "name": workflow_data.get("name"),
                            "path": str(workflow_file),
                            "tools": workflow_data.get("tools", []),
                            "created": workflow_data.get("created"),
                            "status": workflow_data.get("status"),
                        }
                    )
            except Exception as e:
                logger.warning(f"Failed to read workflow {workflow_file}: {e}")

        return {"workflows": workflows}

    except Exception as e:
        logger.error(f"Failed to list workflows: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """Get Crush orchestrator status"""
    try:
        wrapper = get_crush_wrapper()
        deps = await wrapper.check_dependencies()

        return {
            "tool": "Crush",
            "status": "ready" if deps["success"] else "not_ready",
            "dependencies": deps,
            "capabilities": {
                "file_management": True,
                "tool_orchestration": True,
                "workflow_creation": True,
                "background_execution": True,
            },
        }

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
