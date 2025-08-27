#!/usr/bin/env python3
"""
MHDDoS FastAPI Router
DDoS Testing and Stress Testing Tool
"""

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from api.auth import verify_token
from integrations.tools.mhddos_wrapper import get_mhddos_wrapper

# Router setup
router = APIRouter()
security = HTTPBearer()
logger = logging.getLogger(__name__)


# Pydantic models
class StressTestRequest(BaseModel):
    target: str
    method: str = "GET"
    threads: int = 100
    duration: int = 60
    proxy_list: Optional[str] = None
    rate_limit: bool = True


class TargetCheckRequest(BaseModel):
    target: str


# Health endpoint
@router.get("/health")
async def health_check():
    """Check MHDDoS health status"""
    try:
        wrapper = get_mhddos_wrapper()
        dependencies = await wrapper.check_dependencies()
        
        return {
            "status": "healthy" if dependencies["success"] else "unhealthy",
            "tool": "MHDDoS",
            "dependencies": dependencies,
            "timestamp": wrapper._get_timestamp()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )


@router.post("/stress-test")
async def run_stress_test(
    request: StressTestRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token)
):
    """Run stress test against target"""
    try:
        wrapper = get_mhddos_wrapper()
        
        test_config = {
            "method": request.method,
            "threads": request.threads,
            "duration": request.duration,
            "rate_limit": request.rate_limit
        }
        
        def run_test():
            """Background task for stress testing"""
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.stress_test(request.target, test_config)
                )
                logger.info(f"Stress test completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background stress test failed: {e}")
        
        # Add to background tasks
        background_tasks.add_task(run_test)
        
        return {
            "success": True,
            "message": "Stress test started",
            "target": request.target,
            "configuration": test_config,
            "status": "running",
            "timestamp": wrapper._get_timestamp()
        }
        
    except Exception as e:
        logger.error(f"Stress test failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stress test failed: {str(e)}"
        )


@router.post("/check-target")
async def check_target(
    request: TargetCheckRequest,
    token: str = Depends(verify_token)
):
    """Check target availability"""
    try:
        wrapper = get_mhddos_wrapper()
        result = await wrapper.check_target_availability(request.target)
        
        return {
            "success": result["success"],
            "target": request.target,
            "available": result.get("available", False),
            "status_code": result.get("status_code"),
            "response_time": result.get("response_time"),
            "timestamp": result["timestamp"]
        }
        
    except Exception as e:
        logger.error(f"Target check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Target check failed: {str(e)}"
        )


@router.get("/methods")
async def get_methods():
    """Get available HTTP methods"""
    try:
        wrapper = get_mhddos_wrapper()
        methods = await wrapper.get_methods()
        
        return {
            "success": True,
            "methods": methods,
            "timestamp": wrapper._get_timestamp()
        }
        
    except Exception as e:
        logger.error(f"Failed to get methods: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get methods: {str(e)}"
        )


@router.get("/info")
async def get_tool_info():
    """Get MHDDoS tool information"""
    try:
        wrapper = get_mhddos_wrapper()
        dependencies = await wrapper.check_dependencies()
        
        return {
            "name": "MHDDoS",
            "description": "DDoS Testing and Stress Testing Tool",
            "category": "Stress Testing",
            "dependencies": dependencies,
            "features": [
                "HTTP/HTTPS Stress Testing",
                "Multiple HTTP Methods Support",
                "Proxy Support",
                "Rate Limiting",
                "Multi-threaded Testing"
            ],
            "warning": "This tool should only be used for authorized testing purposes",
            "timestamp": wrapper._get_timestamp()
        }
        
    except Exception as e:
        logger.error(f"Failed to get tool info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get tool info: {str(e)}"
        )


@router.get("/status")
async def get_status():
    """Get MHDDoS status"""
    try:
        wrapper = get_mhddos_wrapper()
        dependencies = await wrapper.check_dependencies()
        
        return {
            "tool": "MHDDoS",
            "status": "ready" if dependencies["success"] else "not_ready",
            "dependencies": dependencies,
            "ready_to_use": dependencies["success"],
            "timestamp": wrapper._get_timestamp()
        }
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Status check failed: {str(e)}"
        )