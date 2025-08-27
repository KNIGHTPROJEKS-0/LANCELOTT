"""RedTeam Toolkit API routes"""
from fastapi import APIRouter, Depends
from api.auth import verify_token

router = APIRouter()

@router.get("/status")
async def get_status(username: str = Depends(verify_token)):
    return {"status": "available"}
