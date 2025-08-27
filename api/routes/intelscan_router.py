#!/usr/bin/env python3
"""
Intel-Scan FastAPI Router
Intelligence Gathering and Reconnaissance Tool
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from api.auth import verify_token
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from integrations.tools.intelscan_wrapper import get_intelscan_wrapper

# Router setup
router = APIRouter()
security = HTTPBearer()
logger = logging.getLogger(__name__)


# Pydantic models
class ScanRequest(BaseModel):
    target: str
    scan_type: str = "comprehensive"
    threads: int = 10
    timeout: int = 30
    wordlist: Optional[str] = None
    output_format: str = "json"


class SubdomainScanRequest(BaseModel):
    domain: str
    wordlist: Optional[str] = None
    dns_servers: Optional[List[str]] = None


class PortScanRequest(BaseModel):
    target: str
    port_range: str = "1-1000"


class TechDetectionRequest(BaseModel):
    target: str


# Health endpoint
@router.get("/health")
async def health_check():
    """Check Intel-Scan health status"""
    try:
        wrapper = get_intelscan_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "status": "healthy" if dependencies["success"] else "unhealthy",
            "tool": "Intel-Scan",
            "dependencies": dependencies,
            "timestamp": wrapper._get_timestamp(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )


@router.post("/scan")
async def run_scan(
    request: ScanRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Run Intel-Scan intelligence gathering"""
    try:
        wrapper = get_intelscan_wrapper()

        scan_options = {
            "scan_type": request.scan_type,
            "threads": request.threads,
            "timeout": request.timeout,
            "output_format": request.output_format,
        }

        if request.wordlist:
            scan_options["wordlist"] = request.wordlist

        def run_intelligence_scan():
            """Background task for intelligence gathering"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.execute_scan(request.target, scan_options)
                )
                logger.info(f"Intel-Scan completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background intelligence scan failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_intelligence_scan)

        return {
            "success": True,
            "message": "Intelligence gathering started",
            "target": request.target,
            "scan_type": request.scan_type,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Intelligence scan failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Intelligence scan failed: {str(e)}",
        )


@router.post("/subdomain-enum")
async def subdomain_enumeration(
    request: SubdomainScanRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Perform subdomain enumeration"""
    try:
        wrapper = get_intelscan_wrapper()

        enum_options = {}
        if request.wordlist:
            enum_options["wordlist"] = request.wordlist
        if request.dns_servers:
            enum_options["dns_servers"] = request.dns_servers

        def run_subdomain_enum():
            """Background task for subdomain enumeration"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.subdomain_enumeration(request.domain, enum_options)
                )
                logger.info(f"Subdomain enumeration completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background subdomain enumeration failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_subdomain_enum)

        return {
            "success": True,
            "message": "Subdomain enumeration started",
            "domain": request.domain,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Subdomain enumeration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Subdomain enumeration failed: {str(e)}",
        )


@router.post("/port-discovery")
async def port_discovery(
    request: PortScanRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Perform port discovery"""
    try:
        wrapper = get_intelscan_wrapper()

        def run_port_discovery():
            """Background task for port discovery"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.port_discovery(request.target, request.port_range)
                )
                logger.info(f"Port discovery completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background port discovery failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_port_discovery)

        return {
            "success": True,
            "message": "Port discovery started",
            "target": request.target,
            "port_range": request.port_range,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Port discovery failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Port discovery failed: {str(e)}",
        )


@router.post("/tech-detection")
async def technology_detection(
    request: TechDetectionRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Detect technologies used by target"""
    try:
        wrapper = get_intelscan_wrapper()

        def run_tech_detection():
            """Background task for technology detection"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.technology_detection(request.target)
                )
                logger.info(f"Technology detection completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background technology detection failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_tech_detection)

        return {
            "success": True,
            "message": "Technology detection started",
            "target": request.target,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Technology detection failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Technology detection failed: {str(e)}",
        )


@router.get("/scan-types")
async def get_scan_types():
    """Get available scan types"""
    try:
        wrapper = get_intelscan_wrapper()
        scan_types = await wrapper.get_scan_types()

        return {
            "success": True,
            "scan_types": scan_types,
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Failed to get scan types: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get scan types: {str(e)}",
        )


@router.get("/info")
async def get_tool_info():
    """Get Intel-Scan tool information"""
    try:
        wrapper = get_intelscan_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "name": "Intel-Scan",
            "description": "Intelligence Gathering and Reconnaissance Tool",
            "category": "OSINT",
            "dependencies": dependencies,
            "features": [
                "Subdomain Enumeration",
                "Port Discovery",
                "Technology Detection",
                "Comprehensive Reconnaissance",
                "Custom Wordlists",
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
    """Get Intel-Scan status"""
    try:
        wrapper = get_intelscan_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "tool": "Intel-Scan",
            "status": "ready" if dependencies["success"] else "not_ready",
            "dependencies": dependencies,
            "ready_to_use": dependencies["success"],
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Status check failed: {str(e)}",
        )
