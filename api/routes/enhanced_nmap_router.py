#!/usr/bin/env python3
"""
Enhanced Nmap FastAPI Router
Advanced Network Discovery and Security Auditing
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from api.auth import verify_token
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from integrations.tools.enhanced_nmap_wrapper import get_enhanced_nmap_wrapper

# Router setup
router = APIRouter()
security = HTTPBearer()
logger = logging.getLogger(__name__)


# Pydantic models
class NetworkScanRequest(BaseModel):
    target: str
    scan_type: str = "syn"
    ports: str = "1-1000"
    timing: str = "normal"
    version_detection: bool = True
    os_detection: bool = False
    scripts: Optional[List[str]] = None
    default_scripts: bool = False
    verbosity: int = 1


class VulnerabilityScanRequest(BaseModel):
    target: str
    vuln_categories: Optional[List[str]] = None


class ServiceEnumerationRequest(BaseModel):
    target: str
    ports: str = "1-10000"


class StealthScanRequest(BaseModel):
    target: str
    ports: str = "80,443,22,21,25,53,110,995,993,143"


# Health endpoint
@router.get("/health")
async def health_check():
    """Check Enhanced Nmap health status"""
    try:
        wrapper = get_enhanced_nmap_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "status": "healthy" if dependencies["success"] else "unhealthy",
            "tool": "Enhanced-Nmap",
            "dependencies": dependencies,
            "enhanced_features": dependencies.get("enhanced_features", False),
            "timestamp": wrapper._get_timestamp(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )


@router.post("/scan")
async def run_network_scan(
    request: NetworkScanRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Run enhanced Nmap network scan"""
    try:
        wrapper = get_enhanced_nmap_wrapper()

        scan_options = {
            "scan_type": request.scan_type,
            "ports": request.ports,
            "timing": request.timing,
            "version_detection": request.version_detection,
            "os_detection": request.os_detection,
            "default_scripts": request.default_scripts,
            "verbosity": request.verbosity,
        }

        if request.scripts:
            scan_options["scripts"] = request.scripts

        def run_scan():
            """Background task for network scanning"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.execute_scan(request.target, scan_options)
                )
                logger.info(f"Enhanced Nmap scan completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background network scan failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_scan)

        return {
            "success": True,
            "message": "Network scan started",
            "target": request.target,
            "scan_type": request.scan_type,
            "configuration": scan_options,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Network scan failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Network scan failed: {str(e)}",
        )


@router.post("/vulnerability-scan")
async def vulnerability_scan(
    request: VulnerabilityScanRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Perform vulnerability scanning with NSE scripts"""
    try:
        wrapper = get_enhanced_nmap_wrapper()

        def run_vuln_scan():
            """Background task for vulnerability scanning"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.vulnerability_scan(request.target, request.vuln_categories)
                )
                logger.info(f"Vulnerability scan completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background vulnerability scan failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_vuln_scan)

        return {
            "success": True,
            "message": "Vulnerability scan started",
            "target": request.target,
            "categories": request.vuln_categories,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Vulnerability scan failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vulnerability scan failed: {str(e)}",
        )


@router.post("/service-enumeration")
async def service_enumeration(
    request: ServiceEnumerationRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Perform detailed service enumeration"""
    try:
        wrapper = get_enhanced_nmap_wrapper()

        def run_service_enum():
            """Background task for service enumeration"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.service_enumeration(request.target, request.ports)
                )
                logger.info(f"Service enumeration completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background service enumeration failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_service_enum)

        return {
            "success": True,
            "message": "Service enumeration started",
            "target": request.target,
            "ports": request.ports,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Service enumeration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Service enumeration failed: {str(e)}",
        )


@router.post("/stealth-scan")
async def stealth_scan(
    request: StealthScanRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Perform stealth scan to avoid detection"""
    try:
        wrapper = get_enhanced_nmap_wrapper()

        def run_stealth_scan():
            """Background task for stealth scanning"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.stealth_scan(request.target, request.ports)
                )
                logger.info(f"Stealth scan completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background stealth scan failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_stealth_scan)

        return {
            "success": True,
            "message": "Stealth scan started",
            "target": request.target,
            "ports": request.ports,
            "status": "running",
            "warning": "Stealth scan will take longer to complete",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Stealth scan failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stealth scan failed: {str(e)}",
        )


@router.get("/scan-types")
async def get_scan_types():
    """Get available scan types"""
    try:
        scan_types = {
            "syn": "SYN Scan (default, fast and stealthy)",
            "tcp": "TCP Connect Scan (reliable but slower)",
            "udp": "UDP Scan (for UDP services)",
            "stealth": "Stealth SYN Scan with slow timing",
            "aggressive": "Aggressive scan with OS detection and scripts",
        }

        return {
            "success": True,
            "scan_types": scan_types,
            "default": "syn",
            "timestamp": get_enhanced_nmap_wrapper()._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Failed to get scan types: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get scan types: {str(e)}",
        )


@router.get("/timing-templates")
async def get_timing_templates():
    """Get available timing templates"""
    try:
        timing_templates = {
            "paranoid": "T0 - Very slow, for IDS evasion",
            "sneaky": "T1 - Slow, for IDS evasion",
            "polite": "T2 - Slow, less bandwidth usage",
            "normal": "T3 - Default timing",
            "aggressive": "T4 - Fast, for fast networks",
            "insane": "T5 - Very fast, aggressive timing",
        }

        return {
            "success": True,
            "timing_templates": timing_templates,
            "default": "normal",
            "timestamp": get_enhanced_nmap_wrapper()._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Failed to get timing templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get timing templates: {str(e)}",
        )


@router.get("/info")
async def get_tool_info():
    """Get Enhanced Nmap tool information"""
    try:
        wrapper = get_enhanced_nmap_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "name": "Enhanced-Nmap",
            "description": "Advanced Network Discovery and Security Auditing Tool",
            "category": "Network Security",
            "dependencies": dependencies,
            "features": [
                "Network Discovery",
                "Port Scanning",
                "Service Detection",
                "OS Fingerprinting",
                "Vulnerability Scanning",
                "NSE Script Engine",
                "Stealth Scanning",
                "XML Output Parsing",
                "Custom Timing Controls",
            ],
            "enhanced_features": [
                "Advanced XML Parsing",
                "Background Task Support",
                "Comprehensive Result Analysis",
                "Multiple Scan Types",
                "Stealth Capabilities",
            ],
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Failed to get tool info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get tool info: {str(e)}",
        )


@router.get("/status")
async def get_status():
    """Get Enhanced Nmap status"""
    try:
        wrapper = get_enhanced_nmap_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "tool": "Enhanced-Nmap",
            "status": "ready" if dependencies["success"] else "not_ready",
            "dependencies": dependencies,
            "enhanced_features": dependencies.get("enhanced_features", False),
            "ready_to_use": dependencies["success"],
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Status check failed: {str(e)}",
        )
