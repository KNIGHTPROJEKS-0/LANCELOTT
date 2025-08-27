"""
THC-Hydra API Router
Fast network login cracker
"""

import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

from fastapi import APIRouter, BackgroundTasks, HTTPException

router = APIRouter()


class HydraAttackRequest(BaseModel):
    target: str
    service: str  # ssh, ftp, http-get, etc.
    username: Optional[str] = None
    userlist: Optional[str] = None
    password: Optional[str] = None
    passlist: Optional[str] = None
    port: Optional[int] = None
    threads: int = 16
    options: Dict[str, Any] = {}


class HydraAttackResponse(BaseModel):
    attack_id: str
    status: str
    target: str
    service: str
    started_at: datetime
    results: Optional[Dict[str, Any]] = None


# In-memory storage for attack results
attack_results: Dict[str, Dict[str, Any]] = {}


@router.get("/", summary="Get THC-Hydra information")
async def get_hydra_info():
    """Get information about the THC-Hydra tool"""
    return {
        "name": "THC-Hydra",
        "version": "9.5",
        "description": "Fast network login cracker supporting many protocols",
        "supported_services": [
            "ssh",
            "ftp",
            "http-get",
            "http-post",
            "https-get",
            "https-post",
            "telnet",
            "mysql",
            "postgres",
            "smtp",
            "pop3",
            "imap",
            "vnc",
            "rdp",
            "smb",
            "ldap",
            "oracle",
            "mssql",
            "redis",
        ],
        "endpoints": [
            "/attack - Start a new brute force attack",
            "/attack/{attack_id} - Get attack results",
            "/attacks - List all attacks",
        ],
    }


@router.post(
    "/attack", response_model=HydraAttackResponse, summary="Start brute force attack"
)
async def start_hydra_attack(
    request: HydraAttackRequest, background_tasks: BackgroundTasks
):
    """Start a new THC-Hydra brute force attack"""
    attack_id = str(uuid.uuid4())

    # Validate request
    if not request.username and not request.userlist:
        raise HTTPException(
            status_code=400, detail="Either username or userlist must be provided"
        )
    if not request.password and not request.passlist:
        raise HTTPException(
            status_code=400, detail="Either password or passlist must be provided"
        )

    # Initialize attack result
    attack_results[attack_id] = {
        "attack_id": attack_id,
        "status": "started",
        "target": request.target,
        "service": request.service,
        "started_at": datetime.now(),
        "results": None,
    }

    # Start background attack
    background_tasks.add_task(run_hydra_attack, attack_id, request)

    return HydraAttackResponse(
        attack_id=attack_id,
        status="started",
        target=request.target,
        service=request.service,
        started_at=datetime.now(),
    )


@router.get(
    "/attack/{attack_id}",
    response_model=HydraAttackResponse,
    summary="Get attack results",
)
async def get_attack_results(attack_id: str):
    """Get results for a specific attack"""
    if attack_id not in attack_results:
        raise HTTPException(status_code=404, detail="Attack not found")

    result = attack_results[attack_id]
    return HydraAttackResponse(**result)


@router.get("/attacks", summary="List all attacks")
async def list_attacks():
    """List all THC-Hydra attacks"""
    return {"attacks": list(attack_results.values()), "total": len(attack_results)}


async def run_hydra_attack(attack_id: str, request: HydraAttackRequest):
    """Run THC-Hydra attack in background"""
    try:
        attack_results[attack_id]["status"] = "running"

        # Build hydra command
        cmd = ["hydra"]

        # Add username/userlist
        if request.username:
            cmd.extend(["-l", request.username])
        elif request.userlist:
            cmd.extend(["-L", request.userlist])

        # Add password/passlist
        if request.password:
            cmd.extend(["-p", request.password])
        elif request.passlist:
            cmd.extend(["-P", request.passlist])

        # Add port if specified
        if request.port:
            cmd.extend(["-s", str(request.port)])

        # Add threads
        cmd.extend(["-t", str(request.threads)])

        # Add additional options
        for key, value in request.options.items():
            cmd.extend([f"-{key}", str(value)])

        # Add target and service
        cmd.extend([request.target, request.service])

        # Run the attack
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd="/app/THC-Hydra",
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            # Parse results
            output = stdout.decode()
            results = parse_hydra_output(output)

            attack_results[attack_id].update(
                {
                    "status": "completed",
                    "results": results,
                    "completed_at": datetime.now(),
                }
            )
        else:
            attack_results[attack_id].update(
                {
                    "status": "failed",
                    "error": stderr.decode(),
                    "completed_at": datetime.now(),
                }
            )

    except Exception as e:
        attack_results[attack_id].update(
            {"status": "failed", "error": str(e), "completed_at": datetime.now()}
        )


def parse_hydra_output(output: str) -> Dict[str, Any]:
    """Parse THC-Hydra output"""
    results = {"raw_output": output, "found_credentials": [], "summary": {}}

    lines = output.split("\n")
    for line in lines:
        # Look for successful login attempts
        if "[" in line and "]" in line and "login:" in line:
            # Parse credential line
            parts = line.split()
            if len(parts) >= 6:
                host = parts[2]
                service = parts[3]
                login = parts[5]
                password = parts[7] if len(parts) > 7 else ""

                results["found_credentials"].append(
                    {
                        "host": host,
                        "service": service,
                        "username": login,
                        "password": password,
                    }
                )

    results["summary"]["total_found"] = len(results["found_credentials"])
    return results
