#!/usr/bin/env python3
"""
Feroxbuster FastAPI Router
Fast Content Discovery Tool
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from api.auth import verify_token
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from integrations.tools.feroxbuster_wrapper import get_feroxbuster_wrapper

# Router setup
router = APIRouter()
security = HTTPBearer()
logger = logging.getLogger(__name__)


# Pydantic models
class ContentDiscoveryRequest(BaseModel):
    target: str
    wordlist: Optional[str] = None
    threads: int = 50
    depth: int = 4
    extensions: Optional[List[str]] = None
    status_codes: Optional[List[int]] = None
    timeout: int = 7
    user_agent: str = "Feroxbuster/2.7.1"


class DirectoryBruteForceRequest(BaseModel):
    target: str
    wordlist: Optional[str] = None


class FileDiscoveryRequest(BaseModel):
    target: str
    extensions: Optional[List[str]] = None


class RecursiveScanRequest(BaseModel):
    target: str
    max_depth: int = 3


# Health endpoint
@router.get("/health")
async def health_check():
    """Check Feroxbuster health status"""
    try:
        wrapper = get_feroxbuster_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "status": "healthy" if dependencies["success"] else "unhealthy",
            "tool": "Feroxbuster",
            "dependencies": dependencies,
            "ready_to_use": dependencies.get("ready_to_use", False),
            "can_build": dependencies.get("can_build", False),
            "timestamp": wrapper._get_timestamp(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )


@router.post("/scan")
async def run_content_discovery(
    request: ContentDiscoveryRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Run Feroxbuster content discovery"""
    try:
        wrapper = get_feroxbuster_wrapper()

        scan_options = {
            "threads": request.threads,
            "depth": request.depth,
            "timeout": request.timeout,
            "user_agent": request.user_agent,
        }

        if request.wordlist:
            scan_options["wordlist"] = request.wordlist
        if request.extensions:
            scan_options["extensions"] = request.extensions
        if request.status_codes:
            scan_options["status_codes"] = request.status_codes

        def run_discovery():
            """Background task for content discovery"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.execute_scan(request.target, scan_options)
                )
                logger.info(f"Feroxbuster scan completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background content discovery failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_discovery)

        return {
            "success": True,
            "message": "Content discovery started",
            "target": request.target,
            "configuration": scan_options,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Content discovery failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content discovery failed: {str(e)}",
        )


@router.post("/directory-brute-force")
async def directory_brute_force(
    request: DirectoryBruteForceRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Perform directory brute force attack"""
    try:
        wrapper = get_feroxbuster_wrapper()

        def run_brute_force():
            """Background task for directory brute force"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.directory_brute_force(request.target, request.wordlist)
                )
                logger.info(f"Directory brute force completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background directory brute force failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_brute_force)

        return {
            "success": True,
            "message": "Directory brute force started",
            "target": request.target,
            "wordlist": request.wordlist,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Directory brute force failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Directory brute force failed: {str(e)}",
        )


@router.post("/file-discovery")
async def file_discovery(
    request: FileDiscoveryRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Discover files with specific extensions"""
    try:
        wrapper = get_feroxbuster_wrapper()

        def run_file_discovery():
            """Background task for file discovery"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.file_discovery(request.target, request.extensions)
                )
                logger.info(f"File discovery completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background file discovery failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_file_discovery)

        return {
            "success": True,
            "message": "File discovery started",
            "target": request.target,
            "extensions": request.extensions,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"File discovery failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File discovery failed: {str(e)}",
        )


@router.post("/recursive-scan")
async def recursive_scan(
    request: RecursiveScanRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Perform recursive directory scanning"""
    try:
        wrapper = get_feroxbuster_wrapper()

        def run_recursive_scan():
            """Background task for recursive scanning"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.recursive_scan(request.target, request.max_depth)
                )
                logger.info(f"Recursive scan completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background recursive scan failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_recursive_scan)

        return {
            "success": True,
            "message": "Recursive scan started",
            "target": request.target,
            "max_depth": request.max_depth,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Recursive scan failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recursive scan failed: {str(e)}",
        )


@router.post("/build")
async def build_from_source(
    background_tasks: BackgroundTasks, token: str = Depends(verify_token)
):
    """Build Feroxbuster from source"""
    try:
        wrapper = get_feroxbuster_wrapper()

        def run_build():
            """Background task for building from source"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(wrapper.build_from_source())
                logger.info(f"Feroxbuster build completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background build failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_build)

        return {
            "success": True,
            "message": "Build from source started",
            "status": "building",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Build start failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Build start failed: {str(e)}",
        )


@router.get("/info")
async def get_tool_info():
    """Get Feroxbuster tool information"""
    try:
        wrapper = get_feroxbuster_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "name": "Feroxbuster",
            "description": "Fast Content Discovery Tool",
            "category": "Web Security",
            "language": "Rust",
            "dependencies": dependencies,
            "features": [
                "Fast Content Discovery",
                "Directory Brute Forcing",
                "File Discovery",
                "Recursive Scanning",
                "Multi-threading Support",
                "Custom Wordlists",
                "Extension Filtering",
                "Auto-tuning",
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
    """Get Feroxbuster status"""
    try:
        wrapper = get_feroxbuster_wrapper()
        dependencies = await wrapper.check_dependencies()

        ready_to_use = dependencies.get("ready_to_use", False)
        can_build = dependencies.get("can_build", False)

        status_msg = (
            "ready"
            if ready_to_use
            else "build_required" if can_build else "dependencies_missing"
        )

        return {
            "tool": "Feroxbuster",
            "status": status_msg,
            "dependencies": dependencies,
            "ready_to_use": ready_to_use,
            "can_build": can_build,
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Status check failed: {str(e)}",
        )
