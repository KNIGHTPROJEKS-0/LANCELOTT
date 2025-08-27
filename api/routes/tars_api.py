#!/usr/bin/env python3
"""
TARS API Router
API endpoints for TARS Agent and UI integration with Firebase logging
"""

import asyncio
import logging
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from api.auth import verify_token
from core.firebase_config import get_firebase, log_to_firebase

logger = logging.getLogger(__name__)

# Router instance
router = APIRouter()

# Global process tracking
_active_processes: Dict[str, subprocess.Popen] = {}
_process_status: Dict[str, Dict[str, Any]] = {}


# Pydantic Models
class TARSStatus(BaseModel):
    """TARS status response model"""

    agent_running: bool
    ui_running: bool
    firebase_connected: bool
    processes: Dict[str, Dict[str, Any]]
    timestamp: str
    firebase_status: Optional[Dict[str, Any]] = None


class TARSCommand(BaseModel):
    """TARS command request model"""

    command: str = Field(..., description="Command to send to TARS agent")
    parameters: Optional[Dict[str, Any]] = Field(
        default=None, description="Command parameters"
    )
    timeout: Optional[int] = Field(
        default=300, description="Command timeout in seconds"
    )


class TARSResponse(BaseModel):
    """Generic TARS response model"""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    process_id: Optional[str] = None
    timestamp: str


class ProcessInfo(BaseModel):
    """Process information model"""

    pid: Optional[int]
    status: str
    command: str
    started_at: str
    cpu_percent: Optional[float] = None
    memory_percent: Optional[float] = None


# Helper Functions
def get_process_info(process_name: str) -> Optional[ProcessInfo]:
    """
    Get information about a running process

    Args:
        process_name: Name of the process to check

    Returns:
        ProcessInfo object or None if process not found
    """
    try:
        import psutil

        for proc in psutil.process_iter(
            ["pid", "name", "cmdline", "create_time", "cpu_percent", "memory_percent"]
        ):
            try:
                proc_info = proc.info
                if process_name.lower() in proc_info["name"].lower() or any(
                    process_name.lower() in arg.lower()
                    for arg in proc_info["cmdline"] or []
                ):

                    return ProcessInfo(
                        pid=proc_info["pid"],
                        status="running",
                        command=" ".join(proc_info["cmdline"] or []),
                        started_at=datetime.fromtimestamp(
                            proc_info["create_time"]
                        ).isoformat(),
                        cpu_percent=proc_info.get("cpu_percent", 0.0),
                        memory_percent=proc_info.get("memory_percent", 0.0),
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    except ImportError:
        logger.warning("psutil not available for process monitoring")
    except Exception as e:
        logger.warning(f"Error getting process info for {process_name}: {e}")

    return None


def log_tars_event(event_type: str, data: Dict[str, Any]) -> bool:
    """
    Log TARS event to Firebase

    Args:
        event_type: Type of event (start, stop, command, etc.)
        data: Event data

    Returns:
        True if logged successfully, False otherwise
    """
    event_data = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "source": "tars_api",
        **data,
    }

    return log_to_firebase("tars_events", event_data)


def start_process_background(command: List[str], process_key: str) -> bool:
    """
    Start a process in the background

    Args:
        command: Command to execute
        process_key: Key to track the process

    Returns:
        True if started successfully, False otherwise
    """
    try:
        # Kill existing process if running
        if process_key in _active_processes:
            try:
                _active_processes[process_key].terminate()
                _active_processes[process_key].wait(timeout=5)
            except subprocess.TimeoutExpired:
                _active_processes[process_key].kill()
            except Exception as e:
                logger.warning(f"Error terminating existing {process_key}: {e}")

        # Start new process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd(),
        )

        _active_processes[process_key] = process
        _process_status[process_key] = {
            "pid": process.pid,
            "command": " ".join(command),
            "started_at": datetime.utcnow().isoformat(),
            "status": "running",
        }

        logger.info(f"Started {process_key} with PID {process.pid}")
        return True

    except Exception as e:
        logger.error(f"Failed to start {process_key}: {e}")
        return False


# API Endpoints
@router.post("/agent/start", response_model=TARSResponse)
async def start_agent(
    background_tasks: BackgroundTasks, current_user: dict = Depends(verify_token)
):
    """
    Start the TARS agent service

    This endpoint initiates the agent-tars service and logs the event to Firebase.
    """
    logger.info(
        f"Starting TARS agent - requested by user: {current_user.get('email', 'unknown')}"
    )

    # Check if agent script exists
    agent_script = Path("scripts/launch_agent_tars.sh")
    if not agent_script.exists():
        # Try alternative locations
        agent_script = Path("agent-tars")
        if not agent_script.exists():
            error_msg = "TARS agent script not found"
            logger.error(error_msg)

            # Log error to Firebase
            log_tars_event(
                "agent_start_error",
                {"error": error_msg, "user": current_user.get("email", "unknown")},
            )

            raise HTTPException(status_code=404, detail=error_msg)

    # Start agent process
    command = ["bash", str(agent_script)]
    success = start_process_background(command, "agent-tars")

    if success:
        response_data = {
            "process_id": "agent-tars",
            "pid": _process_status.get("agent-tars", {}).get("pid"),
            "command": " ".join(command),
        }

        # Log successful start to Firebase
        log_tars_event(
            "agent_started",
            {
                "user": current_user.get("email", "unknown"),
                "pid": response_data["pid"],
                "command": response_data["command"],
            },
        )

        return TARSResponse(
            success=True,
            message="TARS agent started successfully",
            data=response_data,
            process_id="agent-tars",
            timestamp=datetime.utcnow().isoformat(),
        )
    else:
        error_msg = "Failed to start TARS agent"

        # Log error to Firebase
        log_tars_event(
            "agent_start_error",
            {"error": error_msg, "user": current_user.get("email", "unknown")},
        )

        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/ui/start", response_model=TARSResponse)
async def start_ui(
    background_tasks: BackgroundTasks, current_user: dict = Depends(verify_token)
):
    """
    Launch the TARS UI desktop application

    This endpoint starts the ui-tars desktop application and logs the event to Firebase.
    """
    logger.info(
        f"Starting TARS UI - requested by user: {current_user.get('email', 'unknown')}"
    )

    # Check if UI script exists
    ui_script = Path("scripts/launch_ui_tars.sh")
    if not ui_script.exists():
        # Try alternative locations
        ui_script = Path("ui-tars")
        if not ui_script.exists():
            error_msg = "TARS UI script not found"
            logger.error(error_msg)

            # Log error to Firebase
            log_tars_event(
                "ui_start_error",
                {"error": error_msg, "user": current_user.get("email", "unknown")},
            )

            raise HTTPException(status_code=404, detail=error_msg)

    # Start UI process
    command = ["bash", str(ui_script)]
    success = start_process_background(command, "ui-tars")

    if success:
        response_data = {
            "process_id": "ui-tars",
            "pid": _process_status.get("ui-tars", {}).get("pid"),
            "command": " ".join(command),
        }

        # Log successful start to Firebase
        log_tars_event(
            "ui_started",
            {
                "user": current_user.get("email", "unknown"),
                "pid": response_data["pid"],
                "command": response_data["command"],
            },
        )

        return TARSResponse(
            success=True,
            message="TARS UI started successfully",
            data=response_data,
            process_id="ui-tars",
            timestamp=datetime.utcnow().isoformat(),
        )
    else:
        error_msg = "Failed to start TARS UI"

        # Log error to Firebase
        log_tars_event(
            "ui_start_error",
            {"error": error_msg, "user": current_user.get("email", "unknown")},
        )

        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/status", response_model=TARSStatus)
async def get_status(current_user: dict = Depends(verify_token)):
    """
    Check the status of TARS services and Firebase connection

    Returns comprehensive status information for TARS agent, UI, and Firebase connectivity.
    """
    logger.debug(
        f"TARS status check - requested by user: {current_user.get('email', 'unknown')}"
    )

    # Check process status
    agent_info = get_process_info("agent-tars")
    ui_info = get_process_info("ui-tars")

    # Update process status
    processes = {}

    if agent_info:
        processes["agent-tars"] = {
            "pid": agent_info.pid,
            "status": agent_info.status,
            "started_at": agent_info.started_at,
            "cpu_percent": agent_info.cpu_percent,
            "memory_percent": agent_info.memory_percent,
        }
    elif "agent-tars" in _process_status:
        # Check if tracked process is still running
        try:
            process = _active_processes.get("agent-tars")
            if process and process.poll() is None:
                processes["agent-tars"] = _process_status["agent-tars"]
                processes["agent-tars"]["status"] = "running"
            else:
                processes["agent-tars"] = _process_status["agent-tars"]
                processes["agent-tars"]["status"] = "stopped"
        except Exception:
            processes["agent-tars"] = _process_status["agent-tars"]
            processes["agent-tars"]["status"] = "unknown"

    if ui_info:
        processes["ui-tars"] = {
            "pid": ui_info.pid,
            "status": ui_info.status,
            "started_at": ui_info.started_at,
            "cpu_percent": ui_info.cpu_percent,
            "memory_percent": ui_info.memory_percent,
        }
    elif "ui-tars" in _process_status:
        # Check if tracked process is still running
        try:
            process = _active_processes.get("ui-tars")
            if process and process.poll() is None:
                processes["ui-tars"] = _process_status["ui-tars"]
                processes["ui-tars"]["status"] = "running"
            else:
                processes["ui-tars"] = _process_status["ui-tars"]
                processes["ui-tars"]["status"] = "stopped"
        except Exception:
            processes["ui-tars"] = _process_status["ui-tars"]
            processes["ui-tars"]["status"] = "unknown"

    # Check Firebase connection
    firebase_config = get_firebase()
    firebase_status = firebase_config.verify_connection()

    # Log status check to Firebase (if connected)
    if firebase_status.get("initialized"):
        log_tars_event(
            "status_check",
            {
                "user": current_user.get("email", "unknown"),
                "agent_running": bool(agent_info),
                "ui_running": bool(ui_info),
                "firebase_connected": firebase_status.get("firestore", False),
            },
        )

    return TARSStatus(
        agent_running=bool(agent_info),
        ui_running=bool(ui_info),
        firebase_connected=firebase_status.get("initialized", False),
        processes=processes,
        timestamp=datetime.utcnow().isoformat(),
        firebase_status=firebase_status,
    )


@router.post("/agent/command", response_model=TARSResponse)
async def send_command(
    command_request: TARSCommand, current_user: dict = Depends(verify_token)
):
    """
    Send a command to the TARS agent

    This is a placeholder endpoint for sending commands to the running TARS agent.
    Implementation depends on the specific communication protocol used by TARS.
    """
    logger.info(
        f"TARS command received: {command_request.command} - from user: {current_user.get('email', 'unknown')}"
    )

    # Log command to Firebase
    log_tars_event(
        "command_sent",
        {
            "user": current_user.get("email", "unknown"),
            "command": command_request.command,
            "parameters": command_request.parameters,
            "timeout": command_request.timeout,
        },
    )

    # Check if agent is running
    agent_info = get_process_info("agent-tars")
    if not agent_info:
        error_msg = "TARS agent is not running"

        # Log error to Firebase
        log_tars_event(
            "command_error",
            {
                "error": error_msg,
                "user": current_user.get("email", "unknown"),
                "command": command_request.command,
            },
        )

        raise HTTPException(status_code=400, detail=error_msg)

    # TODO: Implement actual command communication
    # This would depend on how TARS agent accepts commands
    # Could be through:
    # - File-based communication
    # - Socket communication
    # - REST API calls to agent
    # - Message queue

    # For now, return a placeholder response
    response_data = {
        "command": command_request.command,
        "parameters": command_request.parameters,
        "agent_pid": agent_info.pid,
        "status": "queued",  # Would be updated based on actual implementation
    }

    return TARSResponse(
        success=True,
        message=f"Command '{command_request.command}' sent to TARS agent",
        data=response_data,
        timestamp=datetime.utcnow().isoformat(),
    )


@router.post("/agent/stop", response_model=TARSResponse)
async def stop_agent(current_user: dict = Depends(verify_token)):
    """
    Stop the TARS agent service
    """
    logger.info(
        f"Stopping TARS agent - requested by user: {current_user.get('email', 'unknown')}"
    )

    try:
        # Stop tracked process
        if "agent-tars" in _active_processes:
            process = _active_processes["agent-tars"]
            process.terminate()

            # Wait for graceful shutdown
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

            del _active_processes["agent-tars"]

            if "agent-tars" in _process_status:
                _process_status["agent-tars"]["status"] = "stopped"

        # Log stop event to Firebase
        log_tars_event("agent_stopped", {"user": current_user.get("email", "unknown")})

        return TARSResponse(
            success=True,
            message="TARS agent stopped successfully",
            timestamp=datetime.utcnow().isoformat(),
        )

    except Exception as e:
        error_msg = f"Failed to stop TARS agent: {str(e)}"
        logger.error(error_msg)

        # Log error to Firebase
        log_tars_event(
            "agent_stop_error",
            {"error": error_msg, "user": current_user.get("email", "unknown")},
        )

        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/ui/stop", response_model=TARSResponse)
async def stop_ui(current_user: dict = Depends(verify_token)):
    """
    Stop the TARS UI application
    """
    logger.info(
        f"Stopping TARS UI - requested by user: {current_user.get('email', 'unknown')}"
    )

    try:
        # Stop tracked process
        if "ui-tars" in _active_processes:
            process = _active_processes["ui-tars"]
            process.terminate()

            # Wait for graceful shutdown
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

            del _active_processes["ui-tars"]

            if "ui-tars" in _process_status:
                _process_status["ui-tars"]["status"] = "stopped"

        # Log stop event to Firebase
        log_tars_event("ui_stopped", {"user": current_user.get("email", "unknown")})

        return TARSResponse(
            success=True,
            message="TARS UI stopped successfully",
            timestamp=datetime.utcnow().isoformat(),
        )

    except Exception as e:
        error_msg = f"Failed to stop TARS UI: {str(e)}"
        logger.error(error_msg)

        # Log error to Firebase
        log_tars_event(
            "ui_stop_error",
            {"error": error_msg, "user": current_user.get("email", "unknown")},
        )

        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/logs", response_model=Dict[str, List[Dict[str, Any]]])
async def get_logs(
    limit: int = 50,
    event_type: Optional[str] = None,
    current_user: dict = Depends(verify_token),
):
    """
    Get TARS event logs from Firebase

    Args:
        limit: Maximum number of logs to return
        event_type: Filter by event type

    Returns:
        Dictionary containing event logs
    """
    logger.debug(f"TARS logs requested - user: {current_user.get('email', 'unknown')}")

    firebase_config = get_firebase()
    db = firebase_config.get_firestore_client()

    if not db:
        raise HTTPException(status_code=503, detail="Firebase not available")

    try:
        # Query logs from Firebase
        collection_ref = db.collection("tars_events")
        query = collection_ref.order_by("timestamp", direction="DESCENDING").limit(
            limit
        )

        if event_type:
            query = query.where("event_type", "==", event_type)

        docs = query.stream()

        logs = []
        for doc in docs:
            log_data = doc.to_dict()
            log_data["id"] = doc.id
            logs.append(log_data)

        return {"events": logs}

    except Exception as e:
        logger.error(f"Failed to retrieve logs: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve logs: {str(e)}"
        )
