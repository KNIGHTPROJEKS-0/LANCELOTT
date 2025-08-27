#!/usr/bin/env python3
"""
LangChain.js FastAPI Router
JavaScript/TypeScript AI integration endpoints
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from fastapi import APIRouter, BackgroundTasks, HTTPException
from integrations.frameworks.langchainjs_wrapper import get_langchainjs_wrapper

router = APIRouter()
logger = logging.getLogger(__name__)


# Pydantic models for request/response
class LangChainJSRequest(BaseModel):
    script: str
    operation: Optional[str] = "execute"
    options: Optional[Dict[str, Any]] = {}


class ChainExecutionRequest(BaseModel):
    input: str
    chain_type: Optional[str] = "basic"
    parameters: Optional[Dict[str, Any]] = {}


class AgentExecutionRequest(BaseModel):
    input: str
    agent_type: Optional[str] = "security"
    prompt: Optional[str] = ""


class JSScriptRequest(BaseModel):
    script_content: str
    timeout: Optional[int] = 30
    environment: Optional[Dict[str, str]] = {}


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        wrapper = get_langchainjs_wrapper()
        health_status = await wrapper.health_check()
        return {
            "status": "healthy" if health_status else "unhealthy",
            "tool": "LangChain.js",
            "service_port": wrapper.port,
            "node_available": health_status,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_info():
    """Get LangChain.js tool information"""
    wrapper = get_langchainjs_wrapper()
    return {
        "name": wrapper.name,
        "description": wrapper.description,
        "category": wrapper.category,
        "executable_path": str(wrapper.executable_path),
        "port": wrapper.port,
        "capabilities": [
            "JavaScript/TypeScript AI integration",
            "Cross-platform chain execution",
            "Node.js agent processing",
            "Real-time AI interactions",
            "Express.js API service",
            "Multi-language AI workflows",
        ],
    }


@router.post("/execute-script")
async def execute_javascript(
    request: JSScriptRequest, background_tasks: BackgroundTasks
):
    """Execute JavaScript code using LangChain.js"""
    try:
        wrapper = get_langchainjs_wrapper()

        options = {"timeout": request.timeout, "environment": request.environment}

        result = await wrapper.execute_command(
            request.script_content, operation="execute", options=options
        )

        return result

    except Exception as e:
        logger.error(f"JavaScript execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute-chain")
async def execute_chain(
    request: ChainExecutionRequest, background_tasks: BackgroundTasks
):
    """Execute LangChain.js chain"""
    try:
        wrapper = get_langchainjs_wrapper()

        options = {"chain_type": request.chain_type, "parameters": request.parameters}

        result = await wrapper.execute_command(
            request.input, operation="chain", options=options
        )

        return result

    except Exception as e:
        logger.error(f"Chain execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute-agent")
async def execute_agent(
    request: AgentExecutionRequest, background_tasks: BackgroundTasks
):
    """Execute LangChain.js agent"""
    try:
        wrapper = get_langchainjs_wrapper()

        options = {"agent_type": request.agent_type, "prompt": request.prompt}

        result = await wrapper.execute_command(
            request.input, operation="agent", options=options
        )

        return result

    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start-service")
async def start_langchainjs_service(background_tasks: BackgroundTasks):
    """Start the LangChain.js service"""
    try:
        wrapper = get_langchainjs_wrapper()

        # Start the Node.js service in background
        background_tasks.add_task(wrapper._start_service)

        return {
            "message": "LangChain.js service starting in background",
            "port": wrapper.port,
            "endpoints": [
                f"http://localhost:{wrapper.port}/health",
                f"http://localhost:{wrapper.port}/analyze",
                f"http://localhost:{wrapper.port}/chain",
            ],
        }

    except Exception as e:
        logger.error(f"Service start failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/install-dependencies")
async def install_dependencies(background_tasks: BackgroundTasks):
    """Install LangChain.js dependencies"""
    try:
        wrapper = get_langchainjs_wrapper()

        # Install npm dependencies in background
        background_tasks.add_task(wrapper._install_dependencies)

        return {
            "message": "Installing LangChain.js dependencies in background",
            "project_path": str(wrapper.executable_path),
        }

    except Exception as e:
        logger.error(f"Dependency installation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/service-status")
async def get_service_status():
    """Get LangChain.js service status"""
    try:
        wrapper = get_langchainjs_wrapper()

        # Check if service is running
        import httpx

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://localhost:{wrapper.port}/health", timeout=5
                )
                service_running = response.status_code == 200
        except:
            service_running = False

        return {
            "service_running": service_running,
            "port": wrapper.port,
            "project_path": str(wrapper.executable_path),
            "health_endpoint": f"http://localhost:{wrapper.port}/health",
        }

    except Exception as e:
        logger.error(f"Service status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute")
async def execute_langchainjs_command(
    request: LangChainJSRequest, background_tasks: BackgroundTasks
):
    """Execute general LangChain.js command"""
    try:
        wrapper = get_langchainjs_wrapper()

        # Execute the command in background if specified
        if request.options.get("background", False):
            background_tasks.add_task(
                wrapper.execute_command,
                request.script,
                operation=request.operation,
                options=request.options,
            )
            return {
                "message": "LangChain.js command started in background",
                "operation": request.operation,
                "script_length": len(request.script),
            }

        result = await wrapper.execute_command(
            request.script, operation=request.operation, options=request.options
        )
        return result

    except Exception as e:
        logger.error(f"LangChain.js execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project-info")
async def get_project_info():
    """Get LangChain.js project information"""
    try:
        wrapper = get_langchainjs_wrapper()
        project_dir = wrapper.executable_path

        # Check if package.json exists
        package_json = project_dir / "package.json"
        package_exists = package_json.exists()

        # Check if node_modules exists
        node_modules = project_dir / "node_modules"
        dependencies_installed = node_modules.exists()

        # Check if index.js exists
        index_js = project_dir / "index.js"
        main_script_exists = index_js.exists()

        return {
            "project_path": str(project_dir),
            "package_json_exists": package_exists,
            "dependencies_installed": dependencies_installed,
            "main_script_exists": main_script_exists,
            "ready_to_run": package_exists
            and dependencies_installed
            and main_script_exists,
        }

    except Exception as e:
        logger.error(f"Project info failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """Get LangChain.js integration status"""
    try:
        wrapper = get_langchainjs_wrapper()
        health_status = await wrapper.health_check()

        return {
            "tool": "LangChain.js",
            "status": "ready" if health_status else "not_ready",
            "node_available": health_status,
            "project_path": str(wrapper.executable_path),
            "service_port": wrapper.port,
            "capabilities": {
                "javascript_execution": True,
                "typescript_support": True,
                "chain_processing": True,
                "agent_execution": True,
                "express_api": True,
            },
        }

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
