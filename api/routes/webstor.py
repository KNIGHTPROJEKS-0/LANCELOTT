"""
Webstor API Router
Web application storage and analysis tool
"""

import asyncio
import asyncio.subprocess
import json
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

from fastapi import APIRouter, BackgroundTasks, HTTPException

router = APIRouter()


class WebstorScanRequest(BaseModel):
    target_url: str
    scan_type: str = "full"  # full, quick, deep
    options: Dict[str, Any] = {}


class WebstorScanResponse(BaseModel):
    scan_id: str
    status: str
    target_url: str
    started_at: datetime
    results: Optional[Dict[str, Any]] = None


# In-memory storage for scan results (in production, use Redis or database)
scan_results = {}


@router.get("/", summary="Get Webstor information")
async def get_webstor_info():
    """Get information about the Webstor tool"""
    return {
        "name": "Webstor",
        "version": "1.0.0",
        "description": "Web application storage and analysis tool",
        "endpoints": [
            "/scan - Start a new scan",
            "/scan/{scan_id} - Get scan results",
            "/scans - List all scans",
        ],
    }


@router.post("/scan", response_model=WebstorScanResponse, summary="Start Webstor scan")
async def start_webstor_scan(
    request: WebstorScanRequest, background_tasks: BackgroundTasks
):
    """Start a new Webstor scan"""
    scan_id = str(uuid.uuid4())

    # Initialize scan result
    scan_results[scan_id] = {
        "scan_id": scan_id,
        "status": "started",
        "target_url": request.target_url,
        "started_at": datetime.now(),
        "results": None,
    }

    # Start background scan
    background_tasks.add_task(run_webstor_scan, scan_id, request)

    return WebstorScanResponse(
        scan_id=scan_id,
        status="started",
        target_url=request.target_url,
        started_at=datetime.now(),
    )


@router.get(
    "/scan/{scan_id}", response_model=WebstorScanResponse, summary="Get scan results"
)
async def get_scan_results(scan_id: str):
    """Get results for a specific scan"""
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan not found")

    result = scan_results[scan_id]
    return WebstorScanResponse(**result)


@router.get("/scans", summary="List all scans")
async def list_scans():
    """List all Webstor scans"""
    return {"scans": list(scan_results.values()), "total": len(scan_results)}


async def run_webstor_scan(scan_id: str, request: WebstorScanRequest):
    """Run Webstor scan in background"""
    try:
        scan_results[scan_id]["status"] = "running"

        # Build webstor command
        cmd = ["python", "/app/Webstor/webstor.py", "--url", request.target_url]

        if request.scan_type == "deep":
            cmd.extend(["--deep"])
        elif request.scan_type == "quick":
            cmd.extend(["--quick"])

        # Add additional options
        for key, value in request.options.items():
            cmd.extend([f"--{key}", str(value)])

        # Run the scan
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd="/app/Webstor",
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            # Parse results
            try:
                results = json.loads(stdout.decode())
            except:
                results = {"raw_output": stdout.decode()}

            scan_results[scan_id].update(
                {
                    "status": "completed",
                    "results": results,
                    "completed_at": datetime.now(),
                }
            )
        else:
            scan_results[scan_id].update(
                {
                    "status": "failed",
                    "error": stderr.decode(),
                    "completed_at": datetime.now(),
                }
            )

    except Exception as e:
        scan_results[scan_id].update(
            {"status": "failed", "error": str(e), "completed_at": datetime.now()}
        )
