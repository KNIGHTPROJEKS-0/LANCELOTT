#!/usr/bin/env python3
"""
LangChain FastAPI Router
AI-powered security analysis endpoints
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from fastapi import APIRouter, BackgroundTasks, HTTPException
from integrations.frameworks.langchain_wrapper import get_langchain_wrapper

router = APIRouter()
logger = logging.getLogger(__name__)


# Pydantic models for request/response
class LangChainRequest(BaseModel):
    data: str
    operation: Optional[str] = "analyze"
    options: Optional[Dict[str, Any]] = {}


class SecurityAnalysisRequest(BaseModel):
    scan_data: str
    analysis_type: Optional[str] = "vulnerability"
    provider: Optional[str] = "openai"


class ReportGenerationRequest(BaseModel):
    data: str
    report_type: Optional[str] = "comprehensive"
    format: Optional[str] = "markdown"


class ChatRequest(BaseModel):
    query: str
    context: Optional[str] = ""
    session_id: Optional[str] = None


class WorkflowAutomationRequest(BaseModel):
    workflow_description: str
    target_tools: Optional[List[str]] = []
    parameters: Optional[Dict[str, Any]] = {}


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        wrapper = get_langchain_wrapper()
        health_status = await wrapper.health_check()
        return {
            "status": "healthy" if health_status else "unhealthy",
            "tool": "LangChain",
            "ai_providers": len(wrapper.llm_providers),
            "agents_available": len(wrapper.agents),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_info():
    """Get LangChain tool information"""
    wrapper = get_langchain_wrapper()
    return {
        "name": wrapper.name,
        "description": wrapper.description,
        "category": wrapper.category,
        "port": wrapper.port,
        "capabilities": [
            "Security data analysis",
            "Vulnerability assessment",
            "Threat intelligence",
            "Report generation",
            "Interactive security chat",
            "Workflow automation",
            "Multi-provider LLM support",
        ],
        "supported_providers": (
            list(wrapper.llm_providers.keys())
            if hasattr(wrapper, "llm_providers")
            else []
        ),
    }


@router.post("/analyze")
async def analyze_security_data(
    request: SecurityAnalysisRequest, background_tasks: BackgroundTasks
):
    """Analyze security data using AI"""
    try:
        wrapper = get_langchain_wrapper()

        options = {"analysis_type": request.analysis_type, "provider": request.provider}

        result = await wrapper.execute_command(
            request.scan_data, operation="analyze", options=options
        )

        return result

    except Exception as e:
        logger.error(f"Security analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-report")
async def generate_security_report(
    request: ReportGenerationRequest, background_tasks: BackgroundTasks
):
    """Generate comprehensive security report using AI"""
    try:
        wrapper = get_langchain_wrapper()

        options = {"report_type": request.report_type, "format": request.format}

        result = await wrapper.execute_command(
            request.data, operation="generate", options=options
        )

        return result

    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def security_chat(request: ChatRequest):
    """Interactive security chat with AI"""
    try:
        wrapper = get_langchain_wrapper()

        options = {"context": request.context, "session_id": request.session_id}

        result = await wrapper.execute_command(
            request.query, operation="chat", options=options
        )

        return result

    except Exception as e:
        logger.error(f"Security chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/automate-workflow")
async def automate_security_workflow(
    request: WorkflowAutomationRequest, background_tasks: BackgroundTasks
):
    """Automate security workflows using AI"""
    try:
        wrapper = get_langchain_wrapper()

        options = {
            "target_tools": request.target_tools,
            "parameters": request.parameters,
        }

        # Execute automation in background
        background_tasks.add_task(
            wrapper.execute_command,
            request.workflow_description,
            operation="automate",
            options=options,
        )

        return {
            "message": "Workflow automation started in background",
            "workflow": request.workflow_description,
            "target_tools": request.target_tools,
        }

    except Exception as e:
        logger.error(f"Workflow automation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers")
async def get_ai_providers():
    """Get available AI providers"""
    try:
        wrapper = get_langchain_wrapper()

        providers = []
        if hasattr(wrapper, "llm_providers"):
            for name, provider in wrapper.llm_providers.items():
                providers.append(
                    {"name": name, "type": type(provider).__name__, "available": True}
                )

        return {"providers": providers, "total": len(providers)}

    except Exception as e:
        logger.error(f"Failed to get providers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents")
async def get_available_agents():
    """Get available AI agents"""
    try:
        wrapper = get_langchain_wrapper()

        agents = []
        if hasattr(wrapper, "agents"):
            for name, agent in wrapper.agents.items():
                agents.append(
                    {
                        "name": name,
                        "type": type(agent).__name__,
                        "available": True,
                        "description": f"AI agent for {name.replace('_', ' ').title()}",
                    }
                )

        return {"agents": agents, "total": len(agents)}

    except Exception as e:
        logger.error(f"Failed to get agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute")
async def execute_langchain_command(
    request: LangChainRequest, background_tasks: BackgroundTasks
):
    """Execute general LangChain command"""
    try:
        wrapper = get_langchain_wrapper()

        # Execute the command in background if specified
        if request.options.get("background", False):
            background_tasks.add_task(
                wrapper.execute_command,
                request.data,
                operation=request.operation,
                options=request.options,
            )
            return {
                "message": "LangChain command started in background",
                "operation": request.operation,
                "data": (
                    request.data[:100] + "..."
                    if len(request.data) > 100
                    else request.data
                ),
            }

        result = await wrapper.execute_command(
            request.data, operation=request.operation, options=request.options
        )
        return result

    except Exception as e:
        logger.error(f"LangChain execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """Get LangChain integration status"""
    try:
        wrapper = get_langchain_wrapper()
        health_status = await wrapper.health_check()

        return {
            "tool": "LangChain",
            "status": "ready" if health_status else "not_ready",
            "providers_configured": (
                len(wrapper.llm_providers) if hasattr(wrapper, "llm_providers") else 0
            ),
            "agents_available": (
                len(wrapper.agents) if hasattr(wrapper, "agents") else 0
            ),
            "capabilities": {
                "security_analysis": True,
                "report_generation": True,
                "interactive_chat": True,
                "workflow_automation": True,
                "multi_provider_support": True,
            },
        }

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
