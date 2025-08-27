"""
Argus API routes for CERBERUS-FANGS LANCELOTT
"""

from fastapi import APIRouter, Depends
from api.models import ArgusMonitorRequest, BaseResponse
from api.auth import verify_token

router = APIRouter()

@router.post("/monitor")
async def start_monitoring(
    request: ArgusMonitorRequest,
    username: str = Depends(verify_token)
):
    """Start Argus network monitoring"""
    return BaseResponse(success=True, message="Argus monitoring started")

@router.get("/status")
async def get_status(username: str = Depends(verify_token)):
    """Get Argus monitoring status"""
    return {"status": "available"}
