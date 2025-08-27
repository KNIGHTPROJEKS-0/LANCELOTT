"""
Nmap API routes for CERBERUS-FANGS LANCELOTT
"""

import uuid
from datetime import datetime
from typing import List

from api.auth import verify_token
from api.models import BaseResponse, NmapScanRequest, ScanResult
from core.logger_config import get_tool_logger
from core.tool_manager import ToolManager
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

router = APIRouter()
logger = get_tool_logger("nmap")
tool_manager = ToolManager()


@router.post("/scan", response_model=ScanResult)
async def create_nmap_scan(
    scan_request: NmapScanRequest,
    background_tasks: BackgroundTasks,
    username: str = Depends(verify_token),
):
    """Create a new Nmap scan"""

    scan_id = str(uuid.uuid4())
    logger.info(f"Creating Nmap scan {scan_id} for user {username}")

    # Build nmap command
    command = ["nmap"]

    # Add scan type specific flags
    if scan_request.scan_type == "stealth":
        command.extend(["-sS", "-f", "-T2"])
    elif scan_request.scan_type == "comprehensive":
        command.extend(["-A", "-sC", "-sV", "-O"])
    elif scan_request.scan_type == "basic":
        command.extend(["-sT"])

    # Add port specification
    if scan_request.ports:
        command.extend(["-p", scan_request.ports])

    # Add timing template
    if scan_request.timing:
        command.extend([f"-T{scan_request.timing}"])

    # Add output format
    output_file = f"/tmp/nmap_scan_{scan_id}"
    if scan_request.output_format == "xml":
        command.extend(["-oX", f"{output_file}.xml"])
    elif scan_request.output_format == "grepable":
        command.extend(["-oG", f"{output_file}.gnmap"])
    elif scan_request.output_format == "json":
        command.extend(["-oX", f"{output_file}.xml"])  # Convert XML to JSON later

    # Add additional flags
    if scan_request.additional_flags:
        command.extend(scan_request.additional_flags)

    # Add target
    command.append(scan_request.target)

    # Execute scan in background
    background_tasks.add_task(execute_nmap_scan, scan_id, command, username)

    # Return initial scan result
    scan_result = ScanResult(
        scan_id=scan_id,
        tool="nmap",
        target=scan_request.target,
        status="pending",
        started_at=datetime.utcnow(),
        results={"command": " ".join(command)},
    )

    return scan_result


async def execute_nmap_scan(scan_id: str, command: List[str], username: str):
    """Execute Nmap scan in background"""
    logger.info(f"Executing Nmap scan {scan_id} with command: {' '.join(command)}")

    try:
        result = await tool_manager.execute_tool("nmap", command)

        # Store result somewhere (database, file, etc.)
        # For now, just log it
        logger.info(f"Nmap scan {scan_id} completed with result: {result}")

    except Exception as e:
        logger.error(f"Error executing Nmap scan {scan_id}: {str(e)}")


@router.get("/scan/{scan_id}", response_model=ScanResult)
async def get_nmap_scan(scan_id: str, username: str = Depends(verify_token)):
    """Get Nmap scan results"""
    # This would typically fetch from a database
    # For now, return a placeholder
    raise HTTPException(status_code=404, detail="Scan not found")


@router.get("/scans", response_model=List[ScanResult])
async def list_nmap_scans(
    username: str = Depends(verify_token), limit: int = 50, offset: int = 0
):
    """List Nmap scans"""
    # This would typically fetch from a database
    return []


@router.delete("/scan/{scan_id}", response_model=BaseResponse)
async def cancel_nmap_scan(scan_id: str, username: str = Depends(verify_token)):
    """Cancel a running Nmap scan"""
    # Implementation would cancel the running process
    return BaseResponse(success=True, message="Scan cancelled")


@router.get("/presets")
async def get_nmap_presets(username: str = Depends(verify_token)):
    """Get predefined Nmap scan presets"""
    presets = {
        "quick_scan": {
            "name": "Quick TCP Scan",
            "description": "Fast TCP port scan of common ports",
            "flags": ["-sT", "--top-ports", "1000", "-T4"],
        },
        "stealth_scan": {
            "name": "Stealth SYN Scan",
            "description": "Stealthy SYN scan with fragmentation",
            "flags": ["-sS", "-f", "-T2", "--randomize-hosts"],
        },
        "comprehensive_scan": {
            "name": "Comprehensive Scan",
            "description": "Full scan with OS detection and service enumeration",
            "flags": ["-A", "-sC", "-sV", "-O", "-T3"],
        },
        "udp_scan": {
            "name": "UDP Port Scan",
            "description": "UDP port scan of common services",
            "flags": ["-sU", "--top-ports", "1000"],
        },
        "vulnerability_scan": {
            "name": "Vulnerability Scan",
            "description": "NSE vulnerability detection scripts",
            "flags": ["-sV", "--script", "vuln", "-T3"],
        },
    }
    return presets
