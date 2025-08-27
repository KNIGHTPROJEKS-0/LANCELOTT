#!/usr/bin/env python3
"""
RedEye FastAPI Router
Red Team Analysis and Campaign Management Platform
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from api.auth import verify_token
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from integrations.tools.redeye_wrapper import get_redeye_wrapper

# Router setup
router = APIRouter()
security = HTTPBearer()
logger = logging.getLogger(__name__)


# Pydantic models
class CampaignImportRequest(BaseModel):
    campaign_path: str
    parser_type: str = "cobalt-strike"


class DatabaseSetupRequest(BaseModel):
    database_type: str = "sqlite"
    database_url: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class ServerStartRequest(BaseModel):
    port: int = 3000
    environment: str = "development"


class AnalysisRequest(BaseModel):
    target: str
    options: Optional[Dict[str, Any]] = None


# Health endpoint
@router.get("/health")
async def health_check():
    """Check RedEye health status"""
    try:
        wrapper = get_redeye_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "status": "healthy" if dependencies["success"] else "unhealthy",
            "tool": "RedEye",
            "dependencies": dependencies,
            "timestamp": wrapper._get_timestamp(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )


# Database management
@router.post("/database/setup")
async def setup_database(
    request: DatabaseSetupRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Setup RedEye database"""
    try:
        wrapper = get_redeye_wrapper()

        database_config = {"type": request.database_type, "url": request.database_url}

        if request.config:
            database_config.update(request.config)

        result = await wrapper.setup_database(database_config)

        return {
            "success": result["success"],
            "message": result.get("message", "Database setup completed"),
            "config": database_config,
            "timestamp": result["timestamp"],
        }

    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database setup failed: {str(e)}",
        )


# Campaign management
@router.post("/campaign/import")
async def import_campaign(
    request: CampaignImportRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Import campaign data into RedEye"""
    try:
        wrapper = get_redeye_wrapper()

        result = await wrapper.import_campaign(
            request.campaign_path, request.parser_type
        )

        if result["success"]:
            return {
                "success": True,
                "message": "Campaign imported successfully",
                "campaign_path": request.campaign_path,
                "parser_type": request.parser_type,
                "timestamp": result["timestamp"],
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Campaign import failed"),
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Campaign import failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Campaign import failed: {str(e)}",
        )


@router.get("/campaigns")
async def get_campaigns(token: str = Depends(verify_token)):
    """Get list of campaigns"""
    try:
        wrapper = get_redeye_wrapper()
        result = await wrapper.get_campaigns()

        return {
            "success": result["success"],
            "campaigns": result.get("campaigns", []),
            "timestamp": result["timestamp"],
        }

    except Exception as e:
        logger.error(f"Failed to get campaigns: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get campaigns: {str(e)}",
        )


# Server management
@router.post("/server/start")
async def start_server(
    request: ServerStartRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Start RedEye server"""
    try:
        wrapper = get_redeye_wrapper()

        result = await wrapper.start_server(request.port)

        if result["success"]:
            return {
                "success": True,
                "message": f"RedEye server started on port {request.port}",
                "port": request.port,
                "pid": result.get("pid"),
                "timestamp": result["timestamp"],
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Failed to start server"),
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Server start failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server start failed: {str(e)}",
        )


# Analysis endpoints
@router.post("/analyze")
async def run_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Run RedEye analysis"""
    try:
        wrapper = get_redeye_wrapper()

        def run_scan():
            """Background task for running analysis"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.execute_scan(request.target, request.options)
                )
                logger.info(f"RedEye analysis completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background analysis failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_scan)

        return {
            "success": True,
            "message": "RedEye analysis started",
            "target": request.target,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Analysis start failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis start failed: {str(e)}",
        )


# Tool information
@router.get("/info")
async def get_tool_info():
    """Get RedEye tool information"""
    try:
        wrapper = get_redeye_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "name": "RedEye",
            "description": "Red Team Analysis and Campaign Management Platform",
            "version": "latest",
            "category": "Red Team",
            "dependencies": dependencies,
            "features": [
                "Campaign Data Analysis",
                "Red Team Activity Visualization",
                "Attack Timeline Construction",
                "IOC Extraction",
                "Report Generation",
            ],
            "supported_formats": ["Cobalt Strike", "Brute Ratel", "Sliver"],
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Failed to get tool info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get tool info: {str(e)}",
        )


# Status endpoint
@router.get("/status")
async def get_status():
    """Get RedEye status"""
    try:
        wrapper = get_redeye_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "tool": "RedEye",
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
        )  #!/usr/bin/env python3


"""
RedEye FastAPI Router
Red Team Analysis and Campaign Management Platform
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from api.auth import verify_token
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from integrations.tools.redeye_wrapper import get_redeye_wrapper

# Router setup
router = APIRouter()
security = HTTPBearer()
logger = logging.getLogger(__name__)


# Pydantic models
class CampaignImportRequest(BaseModel):
    campaign_path: str
    parser_type: str = "cobalt-strike"


class DatabaseSetupRequest(BaseModel):
    database_type: str = "sqlite"
    database_url: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class ServerStartRequest(BaseModel):
    port: int = 3000
    environment: str = "development"


class AnalysisRequest(BaseModel):
    target: str
    options: Optional[Dict[str, Any]] = None


# Health endpoint
@router.get("/health")
async def health_check():
    """Check RedEye health status"""
    try:
        wrapper = get_redeye_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "status": "healthy" if dependencies["success"] else "unhealthy",
            "tool": "RedEye",
            "dependencies": dependencies,
            "timestamp": wrapper._get_timestamp(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )


# Database management
@router.post("/database/setup")
async def setup_database(
    request: DatabaseSetupRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Setup RedEye database"""
    try:
        wrapper = get_redeye_wrapper()

        database_config = {"type": request.database_type, "url": request.database_url}

        if request.config:
            database_config.update(request.config)

        result = await wrapper.setup_database(database_config)

        return {
            "success": result["success"],
            "message": result.get("message", "Database setup completed"),
            "config": database_config,
            "timestamp": result["timestamp"],
        }

    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database setup failed: {str(e)}",
        )


# Campaign management
@router.post("/campaign/import")
async def import_campaign(
    request: CampaignImportRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Import campaign data into RedEye"""
    try:
        wrapper = get_redeye_wrapper()

        result = await wrapper.import_campaign(
            request.campaign_path, request.parser_type
        )

        if result["success"]:
            return {
                "success": True,
                "message": "Campaign imported successfully",
                "campaign_path": request.campaign_path,
                "parser_type": request.parser_type,
                "timestamp": result["timestamp"],
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Campaign import failed"),
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Campaign import failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Campaign import failed: {str(e)}",
        )


@router.get("/campaigns")
async def get_campaigns(token: str = Depends(verify_token)):
    """Get list of campaigns"""
    try:
        wrapper = get_redeye_wrapper()
        result = await wrapper.get_campaigns()

        return {
            "success": result["success"],
            "campaigns": result.get("campaigns", []),
            "timestamp": result["timestamp"],
        }

    except Exception as e:
        logger.error(f"Failed to get campaigns: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get campaigns: {str(e)}",
        )


# Server management
@router.post("/server/start")
async def start_server(
    request: ServerStartRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Start RedEye server"""
    try:
        wrapper = get_redeye_wrapper()

        result = await wrapper.start_server(request.port)

        if result["success"]:
            return {
                "success": True,
                "message": f"RedEye server started on port {request.port}",
                "port": request.port,
                "pid": result.get("pid"),
                "timestamp": result["timestamp"],
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Failed to start server"),
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Server start failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server start failed: {str(e)}",
        )


# Analysis endpoints
@router.post("/analyze")
async def run_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Run RedEye analysis"""
    try:
        wrapper = get_redeye_wrapper()

        def run_scan():
            """Background task for running analysis"""
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    wrapper.execute_scan(request.target, request.options)
                )
                logger.info(f"RedEye analysis completed: {result['success']}")
            except Exception as e:
                logger.error(f"Background analysis failed: {e}")

        # Add to background tasks
        background_tasks.add_task(run_scan)

        return {
            "success": True,
            "message": "RedEye analysis started",
            "target": request.target,
            "status": "running",
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Analysis start failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis start failed: {str(e)}",
        )


# Tool information
@router.get("/info")
async def get_tool_info():
    """Get RedEye tool information"""
    try:
        wrapper = get_redeye_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "name": "RedEye",
            "description": "Red Team Analysis and Campaign Management Platform",
            "version": "latest",
            "category": "Red Team",
            "dependencies": dependencies,
            "features": [
                "Campaign Data Analysis",
                "Red Team Activity Visualization",
                "Attack Timeline Construction",
                "IOC Extraction",
                "Report Generation",
            ],
            "supported_formats": ["Cobalt Strike", "Brute Ratel", "Sliver"],
            "timestamp": wrapper._get_timestamp(),
        }

    except Exception as e:
        logger.error(f"Failed to get tool info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get tool info: {str(e)}",
        )


# Status endpoint
@router.get("/status")
async def get_status():
    """Get RedEye status"""
    try:
        wrapper = get_redeye_wrapper()
        dependencies = await wrapper.check_dependencies()

        return {
            "tool": "RedEye",
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
