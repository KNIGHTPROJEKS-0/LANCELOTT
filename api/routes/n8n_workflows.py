#!/usr/bin/env python3
"""
N8N Integration API Routes for LANCELOTT
Provides workflow automation and orchestration
"""

import asyncio
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field

from api.auth import verify_token
from core.logger_config import get_logger

logger = get_logger(__name__)

# Router configuration
n8n_router = APIRouter(
    prefix="/n8n",
    tags=["N8N Workflow Automation"],
    dependencies=[Depends(verify_token)],
)

# N8N Configuration
N8N_DIR = Path(__file__).parent.parent.parent / "n8n"
N8N_BINARY = N8N_DIR / "packages" / "cli" / "bin" / "n8n"


# Data Models
class WorkflowTrigger(BaseModel):
    """Workflow trigger configuration"""

    workflow_id: str = Field(..., description="N8N workflow ID")
    trigger_type: str = Field(
        default="manual", description="Trigger type (manual, webhook, cron)"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Trigger parameters"
    )


class WorkflowExecution(BaseModel):
    """Workflow execution request"""

    workflow_name: str = Field(..., description="Workflow name or ID")
    input_data: Dict[str, Any] = Field(
        default_factory=dict, description="Input data for workflow"
    )
    wait_till_done: bool = Field(default=True, description="Wait for completion")


class ToolWorkflow(BaseModel):
    """Security tool workflow definition"""

    name: str = Field(..., description="Workflow name")
    description: str = Field(..., description="Workflow description")
    tools: List[str] = Field(..., description="List of tools to execute")
    target: str = Field(..., description="Target for security testing")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Tool parameters"
    )


class WorkflowStatus(BaseModel):
    """Workflow execution status"""

    execution_id: str
    status: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class N8NManager:
    """N8N workflow management"""

    def __init__(self):
        self.n8n_dir = N8N_DIR
        self.n8n_binary = N8N_BINARY
        self.executions = {}
        self.is_running = False

    async def start_n8n_server(self, port: int = 5678) -> Dict[str, Any]:
        """Start N8N server"""
        try:
            if self.is_running:
                return {
                    "success": True,
                    "message": "N8N server already running",
                    "port": port,
                }

            # Start N8N in background
            env = os.environ.copy()
            env.update(
                {
                    "N8N_PORT": str(port),
                    "N8N_HOST": "0.0.0.0",
                    "N8N_PROTOCOL": "http",
                    "WEBHOOK_URL": f"http://localhost:{port}",
                    "NODE_ENV": "production",
                }
            )

            cmd = [str(self.n8n_binary), "start"]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(self.n8n_dir),
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            self.n8n_process = process
            self.is_running = True

            logger.info(f"N8N server started on port {port}")

            return {
                "success": True,
                "message": f"N8N server started on port {port}",
                "port": port,
                "url": f"http://localhost:{port}",
                "pid": process.pid,
            }

        except Exception as e:
            logger.error(f"Failed to start N8N server: {e}")
            return {"success": False, "error": str(e)}

    async def stop_n8n_server(self) -> Dict[str, Any]:
        """Stop N8N server"""
        try:
            if not self.is_running or not hasattr(self, "n8n_process"):
                return {"success": True, "message": "N8N server not running"}

            self.n8n_process.terminate()
            await self.n8n_process.wait()

            self.is_running = False
            delattr(self, "n8n_process")

            logger.info("N8N server stopped")

            return {"success": True, "message": "N8N server stopped"}

        except Exception as e:
            logger.error(f"Failed to stop N8N server: {e}")
            return {"success": False, "error": str(e)}

    async def execute_workflow(
        self, workflow_name: str, input_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute N8N workflow"""
        try:
            cmd = [str(self.n8n_binary), "execute", "--name", workflow_name]

            if input_data:
                # Save input data to temp file
                import tempfile

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".json", delete=False
                ) as f:
                    json.dump(input_data, f)
                    input_file = f.name

                cmd.extend(["--input", input_file])

            # Execute workflow
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(self.n8n_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            # Clean up temp file
            if input_data:
                os.unlink(input_file)

            if process.returncode == 0:
                result = {
                    "success": True,
                    "output": stdout.decode(),
                    "execution_id": f"exec_{datetime.now().timestamp()}",
                }

                # Try to parse JSON output
                try:
                    result["data"] = json.loads(stdout.decode())
                except:
                    pass

                return result
            else:
                return {
                    "success": False,
                    "error": stderr.decode(),
                    "returncode": process.returncode,
                }

        except Exception as e:
            logger.error(f"Failed to execute workflow: {e}")
            return {"success": False, "error": str(e)}

    async def create_security_workflow(
        self, workflow_config: ToolWorkflow
    ) -> Dict[str, Any]:
        """Create a security testing workflow"""
        try:
            # Define the workflow in N8N format
            workflow_definition = {
                "name": workflow_config.name,
                "nodes": [],
                "connections": {},
                "active": False,
                "settings": {},
                "staticData": {},
            }

            # Add start node
            start_node = {
                "parameters": {},
                "id": "start-node",
                "name": "Start",
                "type": "n8n-nodes-base.start",
                "typeVersion": 1,
                "position": [250, 300],
            }
            workflow_definition["nodes"].append(start_node)

            # Add tool nodes based on configuration
            node_id = 1
            prev_node = "Start"

            for tool in workflow_config.tools:
                # Create HTTP request node for each tool
                tool_node = {
                    "parameters": {
                        "url": f"http://localhost:8000/api/{tool.lower()}/scan",
                        "options": {"headers": {"Content-Type": "application/json"}},
                        "method": "POST",
                        "bodyParameters": {
                            "target": workflow_config.target,
                            **workflow_config.parameters.get(tool, {}),
                        },
                    },
                    "id": f"tool-node-{node_id}",
                    "name": f"{tool} Scan",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 1,
                    "position": [250 + (node_id * 200), 300],
                }

                workflow_definition["nodes"].append(tool_node)

                # Add connection from previous node
                if prev_node not in workflow_definition["connections"]:
                    workflow_definition["connections"][prev_node] = {"main": [[]]}

                workflow_definition["connections"][prev_node]["main"][0].append(
                    {"node": f"{tool} Scan", "type": "main", "index": 0}
                )

                prev_node = f"{tool} Scan"
                node_id += 1

            # Save workflow to file
            workflows_dir = self.n8n_dir / "workflows"
            workflows_dir.mkdir(exist_ok=True)

            workflow_file = (
                workflows_dir / f"{workflow_config.name.replace(' ', '_').lower()}.json"
            )

            with open(workflow_file, "w") as f:
                json.dump(workflow_definition, f, indent=2)

            logger.info(f"Created security workflow: {workflow_config.name}")

            return {
                "success": True,
                "workflow_id": workflow_config.name,
                "workflow_file": str(workflow_file),
                "nodes_count": len(workflow_definition["nodes"]),
            }

        except Exception as e:
            logger.error(f"Failed to create security workflow: {e}")
            return {"success": False, "error": str(e)}

    def get_workflow_status(self, execution_id: str) -> Dict[str, Any]:
        """Get workflow execution status"""
        if execution_id in self.executions:
            return self.executions[execution_id]
        else:
            return {"success": False, "error": "Execution not found"}


# Initialize N8N manager
n8n_manager = N8NManager()


# API Endpoints
@n8n_router.post("/start", summary="Start N8N Server")
async def start_n8n(port: int = 5678) -> Dict[str, Any]:
    """Start N8N workflow server"""
    return await n8n_manager.start_n8n_server(port)


@n8n_router.post("/stop", summary="Stop N8N Server")
async def stop_n8n() -> Dict[str, Any]:
    """Stop N8N workflow server"""
    return await n8n_manager.stop_n8n_server()


@n8n_router.get("/status", summary="Get N8N Server Status")
async def get_n8n_status() -> Dict[str, Any]:
    """Get N8N server status"""
    return {"running": n8n_manager.is_running, "timestamp": datetime.now().isoformat()}


@n8n_router.post("/workflow/execute", summary="Execute Workflow")
async def execute_workflow(execution: WorkflowExecution) -> Dict[str, Any]:
    """Execute an N8N workflow"""
    return await n8n_manager.execute_workflow(
        execution.workflow_name, execution.input_data
    )


@n8n_router.post("/workflow/create/security", summary="Create Security Workflow")
async def create_security_workflow(workflow: ToolWorkflow) -> Dict[str, Any]:
    """Create a security testing workflow combining multiple tools"""
    return await n8n_manager.create_security_workflow(workflow)


@n8n_router.get("/workflow/status/{execution_id}", summary="Get Workflow Status")
async def get_workflow_status(execution_id: str) -> Dict[str, Any]:
    """Get the status of a workflow execution"""
    return n8n_manager.get_workflow_status(execution_id)


@n8n_router.post("/workflow/lancelott", summary="Execute LANCELOTT Workflow")
async def execute_cerberus_workflow(
    target: str,
    tools: List[str] = ["metabigor", "nmap", "metasploit"],
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> Dict[str, Any]:
    """Execute a comprehensive LANCELOTT security workflow"""

    workflow_config = ToolWorkflow(
        name=f"LANCELOTT-{target}-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        description=f"Comprehensive security assessment for {target}",
        tools=tools,
        target=target,
        parameters={
            "metabigor": {"scan_type": "full"},
            "nmap": {"scan_type": "comprehensive", "ports": "1-65535"},
            "metasploit": {"search_exploits": True},
        },
    )

    # Create the workflow
    creation_result = await n8n_manager.create_security_workflow(workflow_config)

    if creation_result["success"]:
        # Execute the workflow
        execution_result = await n8n_manager.execute_workflow(
            workflow_config.name,
            {"target": target, "timestamp": datetime.now().isoformat()},
        )

        return {
            "success": True,
            "workflow_created": creation_result,
            "execution_started": execution_result,
            "workflow_name": workflow_config.name,
        }
    else:
        return creation_result


@n8n_router.get("/workflows/list", summary="List Available Workflows")
async def list_workflows() -> Dict[str, Any]:
    """List all available N8N workflows"""
    try:
        workflows_dir = n8n_manager.n8n_dir / "workflows"

        if not workflows_dir.exists():
            return {"success": True, "workflows": []}

        workflows = []
        for workflow_file in workflows_dir.glob("*.json"):
            try:
                with open(workflow_file, "r") as f:
                    workflow_data = json.load(f)

                workflows.append(
                    {
                        "name": workflow_data.get("name", workflow_file.stem),
                        "file": workflow_file.name,
                        "nodes": len(workflow_data.get("nodes", [])),
                        "active": workflow_data.get("active", False),
                    }
                )
            except Exception as e:
                logger.warning(f"Failed to read workflow file {workflow_file}: {e}")

        return {"success": True, "workflows": workflows}

    except Exception as e:
        logger.error(f"Failed to list workflows: {e}")
        return {"success": False, "error": str(e)}


@n8n_router.post(
    "/workflow/template/pentest", summary="Create Penetration Testing Template"
)
async def create_pentest_template(
    target: str,
    scope: List[str] = ["reconnaissance", "scanning", "exploitation"],
    aggressive: bool = False,
) -> Dict[str, Any]:
    """Create a pre-configured penetration testing workflow template"""

    # Define tool combinations based on scope
    tool_mapping = {
        "reconnaissance": ["metabigor", "sherlock", "social_analyzer"],
        "scanning": ["nmap", "argus", "kraken"],
        "exploitation": ["metasploit", "hydra", "vajra"],
        "web_testing": ["webstor", "storm_breaker", "web_check"],
        "osint": ["spiderfoot", "osmedeus", "phonesploit"],
    }

    # Build tool list based on scope
    tools = []
    for scope_item in scope:
        if scope_item in tool_mapping:
            tools.extend(tool_mapping[scope_item])

    # Remove duplicates while preserving order
    tools = list(dict.fromkeys(tools))

    # Configure parameters based on aggressiveness
    parameters = {}
    if aggressive:
        parameters.update(
            {
                "nmap": {"scan_type": "aggressive", "ports": "1-65535"},
                "metasploit": {"enable_exploits": True, "auto_exploit": True},
                "hydra": {"enable_brute_force": True},
            }
        )
    else:
        parameters.update(
            {
                "nmap": {"scan_type": "stealth", "ports": "1-1000"},
                "metasploit": {"search_only": True},
                "hydra": {"test_common_passwords": True},
            }
        )

    workflow_config = ToolWorkflow(
        name=f"PenTest-{target}-{'-'.join(scope)}-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        description=f"Penetration testing workflow for {target} - Scope: {', '.join(scope)}",
        tools=tools,
        target=target,
        parameters=parameters,
    )

    return await n8n_manager.create_security_workflow(workflow_config)
