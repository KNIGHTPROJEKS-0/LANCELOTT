"""
Firebase API Routes for LANCELOTT Framework
FastAPI routes for Firebase authentication, dashboard, and services

Author: LANCELOTT Development Team
Version: 2.1.0
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field

from api.routes.auth_routes import router as auth_router
from integrations.firebase_auth import (
    FirebaseUser,
    ScanResult,
    get_current_user,
    get_firebase_auth,
    get_firebase_service,
    require_permission,
)
from integrations.firebase_integration import get_firebase_manager

# Setup logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/firebase", tags=["Firebase"])

# Include authentication routes
router.include_router(auth_router, prefix="", tags=["Firebase Authentication"])


# Request/Response Models
class FirebaseConfigResponse(BaseModel):
    """Firebase configuration response"""

    config: Dict[str, Any]
    dashboard_url: str
    project_id: str


class AuthTokenRequest(BaseModel):
    """Authentication token request"""

    token: str


class UserProfileUpdate(BaseModel):
    """User profile update request"""

    display_name: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class ScanResultCreate(BaseModel):
    """Create scan result request"""

    tool_name: str = Field(..., description="Name of the security tool used")
    target: str = Field(..., description="Target of the scan")
    status: str = Field(default="pending", description="Scan status")
    results: Dict[str, Any] = Field(default_factory=dict, description="Scan results")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class ScanStatusUpdate(BaseModel):
    """Scan status update request"""

    status: str = Field(..., description="New scan status")
    results: Optional[Dict[str, Any]] = Field(None, description="Updated results")


# Health Check Routes
@router.get("/health", summary="Firebase Health Check")
async def firebase_health_check():
    """
    Check Firebase service health and connectivity

    Returns:
        Dict containing health status of Firebase services
    """
    try:
        firebase_manager = get_firebase_manager()
        health_status = firebase_manager.health_check()

        return {
            "status": (
                "healthy" if health_status.get("firebase_initialized") else "unhealthy"
            ),
            "timestamp": datetime.now().isoformat(),
            "services": health_status,
        }
    except Exception as e:
        logger.error(f"Firebase health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Firebase service unavailable",
        )


# Configuration Routes
@router.get(
    "/config",
    response_model=FirebaseConfigResponse,
    summary="Get Firebase Configuration",
)
async def get_firebase_config():
    """
    Get Firebase client configuration for web applications

    Returns:
        Firebase configuration object
    """
    try:
        firebase_manager = get_firebase_manager()
        config = firebase_manager.get_config()

        return FirebaseConfigResponse(
            config=config,
            dashboard_url=firebase_manager.get_dashboard_url(),
            project_id=config.get("projectId", ""),
        )
    except Exception as e:
        logger.error(f"Failed to get Firebase config: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve Firebase configuration",
        )


@router.get("/dashboard", summary="Redirect to Firebase Dashboard")
async def redirect_to_dashboard():
    """
    Redirect to Firebase hosting dashboard

    Returns:
        Redirect response to Firebase dashboard
    """
    try:
        dashboard_url = os.getenv("FIREBASE_DASHBOARD_URL")
        if not dashboard_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Firebase dashboard URL not configured",
            )

        return RedirectResponse(url=dashboard_url, status_code=status.HTTP_302_FOUND)
    except Exception as e:
        logger.error(f"Dashboard redirect failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to redirect to dashboard",
        )


# Authentication Routes
@router.post("/auth/verify", summary="Verify Firebase Token")
async def verify_firebase_token(request: AuthTokenRequest):
    """
    Verify Firebase ID token and return user information

    Args:
        request: Token verification request

    Returns:
        User information if token is valid
    """
    try:
        firebase_auth = get_firebase_auth()
        user = firebase_auth.verify_token(request.token)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        return {
            "valid": True,
            "user": user.dict(),
            "message": "Token verified successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token verification failed",
        )


@router.get("/auth/me", summary="Get Current User")
async def get_current_user_info(current_user: FirebaseUser = Depends(get_current_user)):
    """
    Get current authenticated user information

    Args:
        current_user: Current authenticated user

    Returns:
        Current user information
    """
    return {
        "user": current_user.dict(),
        "authenticated": True,
        "timestamp": datetime.now().isoformat(),
    }


# User Profile Routes
@router.get("/users/profile", summary="Get User Profile")
async def get_user_profile(current_user: FirebaseUser = Depends(get_current_user)):
    """
    Get current user's profile information

    Args:
        current_user: Current authenticated user

    Returns:
        User profile information
    """
    try:
        firebase_auth = get_firebase_auth()
        profile = firebase_auth.get_user_profile(current_user.uid)

        return {"profile": profile, "user": current_user.dict()}
    except Exception as e:
        logger.error(f"Failed to get user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile",
        )


@router.put("/users/profile", summary="Update User Profile")
async def update_user_profile(
    updates: UserProfileUpdate, current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Update current user's profile

    Args:
        updates: Profile updates
        current_user: Current authenticated user

    Returns:
        Success message
    """
    try:
        firebase_auth = get_firebase_auth()
        update_data = {}

        if updates.display_name is not None:
            update_data["display_name"] = updates.display_name

        if updates.settings is not None:
            # Ensure settings is properly handled as Dict[str, Any]
            if isinstance(updates.settings, dict):
                update_data["settings"] = updates.settings

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No updates provided"
            )

        success = firebase_auth.update_user_profile(current_user.uid, update_data)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update profile",
            )

        return {"message": "Profile updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile update failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed",
        )


# Scan Results Routes
@router.post("/scans", summary="Create Scan Result")
async def create_scan_result(
    scan_data: ScanResultCreate, current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Create a new scan result entry

    Args:
        scan_data: Scan result data
        current_user: Current authenticated user

    Returns:
        Created scan result with ID
    """
    try:
        firebase_service = get_firebase_service()

        scan_result = ScanResult(
            user_id=current_user.uid,
            tool_name=scan_data.tool_name,
            target=scan_data.target,
            status=scan_data.status,
            results=scan_data.results,
            metadata=scan_data.metadata,
            timestamp=datetime.now(),
        )

        scan_id = firebase_service.save_scan_result(current_user.uid, scan_result)

        if not scan_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create scan result",
            )

        scan_result.id = scan_id
        return {"scan": scan_result.dict(), "id": scan_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scan creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create scan result",
        )


@router.get("/scans", summary="Get User Scans")
async def get_user_scans(
    current_user: FirebaseUser = Depends(get_current_user),
    limit: int = Query(
        50, description="Maximum number of scans to return", ge=1, le=100
    ),
):
    """
    Get current user's scan results

    Args:
        current_user: Current authenticated user
        limit: Maximum number of results

    Returns:
        List of user's scan results
    """
    try:
        firebase_service = get_firebase_service()
        scans = firebase_service.get_user_scans(current_user.uid, limit)

        return {
            "scans": [scan.dict() for scan in scans],
            "count": len(scans),
            "user_id": current_user.uid,
        }
    except Exception as e:
        logger.error(f"Failed to get user scans: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve scan results",
        )


@router.get("/scans/{scan_id}", summary="Get Scan by ID")
async def get_scan_by_id(
    scan_id: str = Path(..., description="Scan result ID"),
    current_user: FirebaseUser = Depends(get_current_user),
):
    """
    Get specific scan result by ID

    Args:
        scan_id: Scan result ID
        current_user: Current authenticated user

    Returns:
        Scan result if found and accessible
    """
    try:
        firebase_service = get_firebase_service()
        scan = firebase_service.get_scan_by_id(scan_id)

        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found"
            )

        # Check if user owns this scan or has admin permission
        firebase_auth = get_firebase_auth()
        if scan.user_id != current_user.uid and not firebase_auth.has_permission(
            current_user, "read:all_scans"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this scan",
            )

        return {"scan": scan.dict()}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get scan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve scan",
        )


@router.put("/scans/{scan_id}/status", summary="Update Scan Status")
async def update_scan_status(
    scan_id: str = Path(..., description="Scan result ID"),
    current_user: FirebaseUser = Depends(get_current_user),
    status_update: ScanStatusUpdate = Body(...),
):
    """
    Update scan status and results

    Args:
        scan_id: Scan result ID
        status_update: Status update data
        current_user: Current authenticated user

    Returns:
        Success message
    """
    try:
        firebase_service = get_firebase_service()

        # First check if scan exists and user has access
        scan = firebase_service.get_scan_by_id(scan_id)
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found"
            )

        firebase_auth = get_firebase_auth()
        if scan.user_id != current_user.uid and not firebase_auth.has_permission(
            current_user, "update:all_scans"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to update this scan",
            )

        # Update scan status
        success = firebase_service.update_scan_status(
            scan_id, status_update.status, status_update.results
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update scan status",
            )

        return {"message": "Scan status updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scan status update failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update scan status",
        )


# Dashboard Routes
@router.get("/dashboard/stats", summary="Get Dashboard Statistics")
async def get_dashboard_stats(current_user: FirebaseUser = Depends(get_current_user)):
    """
    Get dashboard statistics for current user

    Args:
        current_user: Current authenticated user

    Returns:
        Dashboard statistics
    """
    try:
        firebase_service = get_firebase_service()
        stats = firebase_service.get_dashboard_stats(current_user.uid)

        return {"stats": stats, "generated_at": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"Failed to get dashboard stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard statistics",
        )


# Admin Routes (require admin permission)
@router.get("/admin/users", summary="Get All Users (Admin)")
@require_permission("admin:read_users")
async def get_all_users(
    current_user: FirebaseUser = Depends(get_current_user),
    limit: int = Query(
        50, description="Maximum number of users to return", ge=1, le=100
    ),
):
    """
    Get all users (admin only)

    Args:
        current_user: Current authenticated user (must be admin)
        limit: Maximum number of results

    Returns:
        List of all users
    """
    try:
        firebase_manager = get_firebase_manager()
        if not firebase_manager.initialized:
            firebase_manager.initialize()

        # Check if db is available
        if not firebase_manager.db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Firebase database not available",
            )

        # Get users from Firestore
        users_ref = firebase_manager.db.collection("users").limit(limit)
        users = []

        for doc in users_ref.stream():
            user_data = doc.to_dict()
            user_data["id"] = doc.id
            users.append(user_data)

        return {"users": users, "count": len(users), "admin": current_user.uid}

    except Exception as e:
        logger.error(f"Failed to get all users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users",
        )


@router.get("/admin/scans", summary="Get All Scans (Admin)")
@require_permission("admin:read_scans")
async def get_all_scans(
    current_user: FirebaseUser = Depends(get_current_user),
    limit: int = Query(
        100, description="Maximum number of scans to return", ge=1, le=500
    ),
):
    """
    Get all scan results (admin only)

    Args:
        current_user: Current authenticated user (must be admin)
        limit: Maximum number of results

    Returns:
        List of all scan results
    """
    try:
        firebase_service = get_firebase_service()
        scans = firebase_service.firebase_manager.get_scan_results(
            "scan_results", None, limit
        )

        return {"scans": scans, "count": len(scans), "admin": current_user.uid}

    except Exception as e:
        logger.error(f"Failed to get all scans: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve all scans",
        )
