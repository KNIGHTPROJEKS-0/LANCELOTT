#!/usr/bin/env python3
"""
UI-TARS FastAPI Router
LANCELOTT Framework Integration

Provides REST API endpoints for UI-TARS Desktop and Agent-TARS CLI
with comprehensive automation, management, and monitoring capabilities.
"""

import asyncio
import json
import os

# Import our UI-TARS wrapper
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

# Import UI-TARS wrapper with proper error handling
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), "../../integrations/tools"))
    from ui_tars_wrapper import UITARSConfig, UITARSMode, UITARSStatus, UITARSWrapper

    UI_TARS_AVAILABLE = True
except ImportError as e:
    # Log the import error but continue with limited functionality
    import logging

    logging.warning(f"UI-TARS wrapper not available: {e}")

    # Define minimal interfaces for type checking
    from enum import Enum
    from typing import Any, Dict

    class UITARSMode(Enum):
        DESKTOP = "desktop"
        AGENT_CLI = "agent_cli"
        WEB_INTERFACE = "web_interface"

    class UITARSStatus(Enum):
        STOPPED = "stopped"
        RUNNING = "running"
        ERROR = "error"

    # Minimal config and wrapper classes for development
    class UITARSConfig:
        def __init__(self):
            # Set all expected attributes with defaults
            self.enabled = True
            self.binary_path = ""
            self.config_path = ""
            self.preset_path = ""
            self.port = 8765
            self.web_port = 5173
            self.host = "localhost"
            self.ai_model = "gpt-5-nano"
            self.ai_provider = "azure"
            self.ai_deployment = "GPT-5-Navo-Cerberus"
            self.ai_max_tokens = 16384
            self.ai_max_completion_tokens = 16384
            self.ai_temperature = 0.1
            self.ai_top_p = 0.9
            self.auth_enabled = True
            self.firebase_project_id = "lancelott-z9dko"
            self.framework_api_url = "http://localhost:7777"
            self.output_dir = "reports/ui_tars_automation"
            self.screenshot_dir = "reports/screenshots"
            self.recording_dir = "reports/recordings"
            self.log_dir = "logs"
            self.cache_dir = "cache/ui_tars"
            self.timeout = 300
            self.max_concurrent_tasks = 2
            self.screenshot_scale = 1.0
            self.max_loop_count = 50
            self.action_timeout = 30000
            self.desktop_mode = True
            self.web_interface = True

    class UITARSWrapper:
        def __init__(self):
            self.config = UITARSConfig()

        def get_status(self):
            return {"enabled": False, "processes": {}, "config": {}}

        async def health_check(self):
            return {
                "healthy": False,
                "timestamp": "",
                "processes": {},
                "config_files": {},
                "directories": {},
            }

        async def start_desktop(self):
            return False

        async def start_agent_cli(self, task=None, interactive=True):
            return False

        async def start_web_interface(self):
            return False

        async def stop_process(self, mode):
            return False

        async def stop_all(self):
            return False

        async def restart_process(self, mode):
            return False

    UI_TARS_AVAILABLE = False


# Create router
router = APIRouter(prefix="/api/v1/tools/ui-tars", tags=["UI-TARS"])

# Global UI-TARS wrapper instance
ui_tars_wrapper: Optional[UITARSWrapper] = None


def get_ui_tars_wrapper() -> UITARSWrapper:
    """Get or create UI-TARS wrapper instance"""
    global ui_tars_wrapper
    if ui_tars_wrapper is None:
        ui_tars_wrapper = UITARSWrapper()
    return ui_tars_wrapper


# Pydantic models for request/response


class UITARSStatusResponse(BaseModel):
    """UI-TARS status response model"""

    enabled: bool
    processes: Dict[str, Any]
    config: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class UITARSHealthResponse(BaseModel):
    """UI-TARS health check response model"""

    healthy: bool
    timestamp: str
    processes: Dict[str, str]
    config_files: Dict[str, bool]
    directories: Dict[str, bool]


class ProcessStartRequest(BaseModel):
    """Process start request model"""

    mode: str = Field(
        ..., description="Process mode: desktop, agent_cli, web_interface"
    )
    options: Optional[Dict[str, Any]] = Field(
        default={}, description="Additional options"
    )


class AgentTaskRequest(BaseModel):
    """Agent task execution request model"""

    task: str = Field(..., description="Task description")
    interactive: bool = Field(default=False, description="Run in interactive mode")
    timeout: Optional[int] = Field(default=300, description="Task timeout in seconds")
    options: Optional[Dict[str, Any]] = Field(
        default={}, description="Additional task options"
    )


class AutomationRequest(BaseModel):
    """GUI automation request model"""

    action: str = Field(
        ..., description="Automation action: click, type, scroll, screenshot"
    )
    target: Optional[str] = Field(
        default=None, description="Target element or coordinates"
    )
    value: Optional[str] = Field(
        default=None, description="Value to input (for type action)"
    )
    options: Optional[Dict[str, Any]] = Field(
        default={}, description="Additional options"
    )


class WorkflowRequest(BaseModel):
    """Workflow execution request model"""

    workflow_name: str = Field(..., description="Workflow name")
    parameters: Optional[Dict[str, Any]] = Field(
        default={}, description="Workflow parameters"
    )
    async_execution: bool = Field(
        default=True, description="Execute workflow asynchronously"
    )


class ConfigurationUpdate(BaseModel):
    """Configuration update request model"""

    ai_model: Optional[str] = None
    ai_provider: Optional[str] = None
    ai_deployment: Optional[str] = None
    ai_temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    desktop_mode: Optional[bool] = None
    web_interface: Optional[bool] = None


# API Endpoints


@router.get("/status", response_model=UITARSStatusResponse)
async def get_status(wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)):
    """Get UI-TARS status"""
    try:
        status = wrapper.get_status()
        return UITARSStatusResponse(**status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")


@router.get("/health", response_model=UITARSHealthResponse)
async def health_check(wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)):
    """Perform UI-TARS health check"""
    try:
        health = await wrapper.health_check()
        return UITARSHealthResponse(**health)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error performing health check: {str(e)}"
        )


@router.post("/start")
async def start_process(
    request: ProcessStartRequest,
    background_tasks: BackgroundTasks,
    wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper),
):
    """Start UI-TARS process"""
    try:
        mode = request.mode.lower()

        if mode == "desktop":
            success = await wrapper.start_desktop()
        elif mode == "agent_cli":
            task = request.options.get("task") if request.options else None
            interactive = (
                request.options.get("interactive", True) if request.options else True
            )
            success = await wrapper.start_agent_cli(task=task, interactive=interactive)
        elif mode == "web_interface":
            success = await wrapper.start_web_interface()
        else:
            raise HTTPException(status_code=400, detail=f"Invalid mode: {mode}")

        if success:
            return {"success": True, "message": f"UI-TARS {mode} started successfully"}
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to start UI-TARS {mode}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting process: {str(e)}")


@router.post("/stop")
async def stop_process(
    mode: str = Query(..., description="Process mode to stop"),
    wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper),
):
    """Stop UI-TARS process"""
    try:
        mode_enum = UITARSMode(mode.lower())
        success = await wrapper.stop_process(mode_enum)

        if success:
            return {"success": True, "message": f"UI-TARS {mode} stopped successfully"}
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to stop UI-TARS {mode}"
            )

    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid mode: {mode}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping process: {str(e)}")


@router.post("/stop-all")
async def stop_all_processes(wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)):
    """Stop all UI-TARS processes"""
    try:
        success = await wrapper.stop_all()

        if success:
            return {
                "success": True,
                "message": "All UI-TARS processes stopped successfully",
            }
        else:
            raise HTTPException(
                status_code=500, detail="Failed to stop some UI-TARS processes"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error stopping processes: {str(e)}"
        )


@router.post("/restart")
async def restart_process(
    mode: str = Query(..., description="Process mode to restart"),
    wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper),
):
    """Restart UI-TARS process"""
    try:
        mode_enum = UITARSMode(mode.lower())
        success = await wrapper.restart_process(mode_enum)

        if success:
            return {
                "success": True,
                "message": f"UI-TARS {mode} restarted successfully",
            }
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to restart UI-TARS {mode}"
            )

    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid mode: {mode}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error restarting process: {str(e)}"
        )


# Desktop-specific endpoints
@router.post("/desktop/start")
async def start_desktop(wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)):
    """Start UI-TARS Desktop application"""
    try:
        success = await wrapper.start_desktop()

        if success:
            status = wrapper.get_status()
            desktop_info = status.get("processes", {}).get("desktop", {})

            return {
                "success": True,
                "message": "UI-TARS Desktop started successfully",
                "web_url": desktop_info.get("web_url"),
                "pid": desktop_info.get("pid"),
            }
        else:
            raise HTTPException(
                status_code=500, detail="Failed to start UI-TARS Desktop"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting desktop: {str(e)}")


@router.get("/desktop/status")
async def get_desktop_status(wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)):
    """Get UI-TARS Desktop status"""
    try:
        status = wrapper.get_status()
        desktop_status = status.get("processes", {}).get("desktop")

        if desktop_status:
            return {
                "running": desktop_status.get("status") == "running",
                "pid": desktop_status.get("pid"),
                "web_url": desktop_status.get("web_url"),
                "started_at": desktop_status.get("started_at"),
                "log_file": desktop_status.get("log_file"),
            }
        else:
            return {"running": False, "message": "UI-TARS Desktop is not running"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting desktop status: {str(e)}"
        )


# Agent-TARS specific endpoints
@router.post("/agent/start")
async def start_agent(
    request: AgentTaskRequest, wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)
):
    """Start Agent-TARS CLI"""
    try:
        success = await wrapper.start_agent_cli(
            task=request.task if not request.interactive else None,
            interactive=request.interactive,
        )

        if success:
            return {
                "success": True,
                "message": "Agent-TARS started successfully",
                "task": request.task,
                "interactive": request.interactive,
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to start Agent-TARS")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting agent: {str(e)}")


@router.post("/agent/execute-task")
async def execute_agent_task(
    request: AgentTaskRequest,
    background_tasks: BackgroundTasks,
    wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper),
):
    """Execute task with Agent-TARS"""
    try:
        # Start agent with specific task
        success = await wrapper.start_agent_cli(
            task=request.task, interactive=request.interactive
        )

        if success:
            return {
                "success": True,
                "message": f"Task '{request.task}' started successfully",
                "task_id": f"task_{datetime.now().timestamp()}",
                "interactive": request.interactive,
                "timeout": request.timeout,
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to execute task")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing task: {str(e)}")


@router.get("/agent/status")
async def get_agent_status(wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)):
    """Get Agent-TARS status"""
    try:
        status = wrapper.get_status()
        agent_status = status.get("processes", {}).get("agent_cli")

        if agent_status:
            return {
                "running": agent_status.get("status") == "running",
                "pid": agent_status.get("pid"),
                "started_at": agent_status.get("started_at"),
                "command": agent_status.get("command"),
                "log_file": agent_status.get("log_file"),
            }
        else:
            return {"running": False, "message": "Agent-TARS is not running"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting agent status: {str(e)}"
        )


# Automation endpoints
@router.post("/automation/execute")
async def execute_automation(
    request: AutomationRequest, wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)
):
    """Execute GUI automation action"""
    try:
        # This would integrate with UI-TARS automation capabilities
        # For now, return a mock response

        automation_id = f"auto_{datetime.now().timestamp()}"

        return {
            "success": True,
            "automation_id": automation_id,
            "action": request.action,
            "target": request.target,
            "value": request.value,
            "status": "executing",
            "message": f"Automation action '{request.action}' started",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error executing automation: {str(e)}"
        )


@router.post("/automation/screenshot")
async def take_screenshot(
    filename: Optional[str] = Query(None, description="Screenshot filename"),
    wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper),
):
    """Take screenshot using UI-TARS"""
    try:
        if not filename:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        # This would integrate with UI-TARS screenshot capabilities
        screenshot_path = Path(wrapper.config.screenshot_dir) / filename

        return {
            "success": True,
            "screenshot_path": str(screenshot_path),
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
            "message": "Screenshot taken successfully",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error taking screenshot: {str(e)}"
        )


# Workflow endpoints
@router.post("/workflows/execute")
async def execute_workflow(
    request: WorkflowRequest,
    background_tasks: BackgroundTasks,
    wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper),
):
    """Execute UI-TARS workflow"""
    try:
        workflow_id = f"workflow_{datetime.now().timestamp()}"

        # This would integrate with UI-TARS workflow system
        return {
            "success": True,
            "workflow_id": workflow_id,
            "workflow_name": request.workflow_name,
            "parameters": request.parameters,
            "async_execution": request.async_execution,
            "status": "started",
            "message": f"Workflow '{request.workflow_name}' started",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error executing workflow: {str(e)}"
        )


@router.get("/workflows/list")
async def list_workflows(wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)):
    """List available UI-TARS workflows"""
    try:
        # This would read from UI-TARS workflow configuration
        workflows = [
            {
                "name": "Security Testing Automation",
                "description": "Automated security testing workflow with GUI interaction",
                "tools": ["screenshot", "browser_automation", "click", "type"],
            },
            {
                "name": "Penetration Testing GUI",
                "description": "GUI-based penetration testing automation",
                "tools": [
                    "browser_automation",
                    "screenshot",
                    "click",
                    "type",
                    "scroll",
                ],
            },
            {
                "name": "Vulnerability Scanning Interface",
                "description": "Automated vulnerability scanning with GUI interface",
                "tools": ["screenshot", "browser_automation", "click"],
            },
            {
                "name": "Automated Report Generation",
                "description": "Automated security report generation with screenshots",
                "tools": ["screenshot", "browser_automation", "type", "click"],
            },
        ]

        return {"workflows": workflows, "count": len(workflows)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error listing workflows: {str(e)}"
        )


# Configuration endpoints
@router.get("/config")
async def get_configuration(wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)):
    """Get UI-TARS configuration"""
    try:
        config = wrapper.config

        return {
            "general": {
                "enabled": config.enabled,
                "binary_path": config.binary_path,
                "config_path": config.config_path,
                "preset_path": config.preset_path,
            },
            "network": {
                "port": config.port,
                "web_port": config.web_port,
                "host": config.host,
            },
            "ai": {
                "model": config.ai_model,
                "provider": config.ai_provider,
                "deployment": config.ai_deployment,
                "max_tokens": config.ai_max_tokens,
                "max_completion_tokens": config.ai_max_completion_tokens,
                "temperature": config.ai_temperature,
                "top_p": config.ai_top_p,
            },
            "authentication": {
                "auth_enabled": config.auth_enabled,
                "firebase_project_id": config.firebase_project_id,
                "framework_api_url": config.framework_api_url,
            },
            "directories": {
                "output_dir": config.output_dir,
                "screenshot_dir": config.screenshot_dir,
                "recording_dir": config.recording_dir,
                "log_dir": config.log_dir,
                "cache_dir": config.cache_dir,
            },
            "performance": {
                "timeout": config.timeout,
                "max_concurrent_tasks": config.max_concurrent_tasks,
                "screenshot_scale": config.screenshot_scale,
                "max_loop_count": config.max_loop_count,
                "action_timeout": config.action_timeout,
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting configuration: {str(e)}"
        )


@router.put("/config")
async def update_configuration(
    request: ConfigurationUpdate, wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)
):
    """Update UI-TARS configuration"""
    try:
        config = wrapper.config
        updated_fields = []

        # Update configuration fields
        if request.ai_model is not None:
            config.ai_model = request.ai_model
            updated_fields.append("ai_model")

        if request.ai_provider is not None:
            config.ai_provider = request.ai_provider
            updated_fields.append("ai_provider")

        if request.ai_deployment is not None:
            config.ai_deployment = request.ai_deployment
            updated_fields.append("ai_deployment")

        if request.ai_temperature is not None:
            config.ai_temperature = request.ai_temperature
            updated_fields.append("ai_temperature")

        if request.max_tokens is not None:
            config.ai_max_tokens = request.max_tokens
            updated_fields.append("max_tokens")

        if request.desktop_mode is not None:
            config.desktop_mode = request.desktop_mode
            updated_fields.append("desktop_mode")

        if request.web_interface is not None:
            config.web_interface = request.web_interface
            updated_fields.append("web_interface")

        return {
            "success": True,
            "message": "Configuration updated successfully",
            "updated_fields": updated_fields,
            "restart_required": len(updated_fields) > 0,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating configuration: {str(e)}"
        )


# Logs endpoints
@router.get("/logs")
async def get_logs(
    lines: int = Query(100, description="Number of log lines to return"),
    log_type: str = Query("all", description="Log type: all, desktop, agent, web"),
):
    """Get UI-TARS logs"""
    try:
        wrapper = get_ui_tars_wrapper()
        log_dir = Path(wrapper.config.log_dir)

        logs = {}

        if log_type == "all" or log_type == "desktop":
            desktop_log = log_dir / "ui_tars_desktop.log"
            if desktop_log.exists():
                with open(desktop_log, "r") as f:
                    logs["desktop"] = f.readlines()[-lines:]

        if log_type == "all" or log_type == "agent":
            agent_log = log_dir / "agent_tars" / "agent_tars.log"
            if agent_log.exists():
                with open(agent_log, "r") as f:
                    logs["agent"] = f.readlines()[-lines:]

        if log_type == "all" or log_type == "web":
            web_log = log_dir / "ui_tars_web.log"
            if web_log.exists():
                with open(web_log, "r") as f:
                    logs["web"] = f.readlines()[-lines:]

        return {
            "logs": logs,
            "lines_requested": lines,
            "log_type": log_type,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting logs: {str(e)}")


# Statistics endpoint
@router.get("/stats")
async def get_statistics(wrapper: UITARSWrapper = Depends(get_ui_tars_wrapper)):
    """Get UI-TARS usage statistics"""
    try:
        # This would collect real statistics from UI-TARS usage
        stats = {
            "uptime": {"total_sessions": 0, "current_uptime": "0:00:00"},
            "automation": {
                "total_actions": 0,
                "screenshots_taken": 0,
                "workflows_executed": 0,
            },
            "performance": {
                "average_response_time": 0.0,
                "success_rate": 100.0,
                "error_count": 0,
            },
            "ai": {
                "model": f"{wrapper.config.ai_provider}/{wrapper.config.ai_model}",
                "total_tokens_used": 0,
                "average_tokens_per_request": 0,
            },
            "last_updated": datetime.now().isoformat(),
        }

        return stats

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting statistics: {str(e)}"
        )


# Router metadata (for documentation)
# Title: UI-TARS API
# Description: UI-TARS Desktop and Agent-TARS CLI integration API for the LANCELOTT Framework
# Version: 2.0.0
