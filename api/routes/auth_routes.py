"""
Firebase Authentication API Routes for LANCELOTT Framework
Provides authentication endpoints for user login, registration, and management

Author: LANCELOTT Development Team
Version: 2.1.0
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr

from integrations.firebase_auth import (
    FirebaseAuth,
    FirebaseService,
    FirebaseUser,
    get_current_user,
    get_firebase_auth,
    get_firebase_service,
    require_permission,
)
from integrations.firebase_integration import get_firebase_manager

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/auth", tags=["Firebase Authentication"])

# Security scheme
security = HTTPBearer()


# Request/Response Models
class LoginRequest(BaseModel):
    """Login request model"""

    email: EmailStr
    password: str
    remember_me: bool = False


class RegisterRequest(BaseModel):
    """Registration request model"""

    email: EmailStr
    password: str
    display_name: Optional[str] = None
    role: str = "user"


class TokenResponse(BaseModel):
    """Token response model"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: FirebaseUser


class UserUpdateRequest(BaseModel):
    """User update request model"""

    display_name: Optional[str] = None
    settings: Optional[Dict] = None


class PasswordResetRequest(BaseModel):
    """Password reset request model"""

    email: EmailStr


class CustomTokenRequest(BaseModel):
    """Custom token request model"""

    uid: str
    additional_claims: Optional[Dict] = None


# Authentication Endpoints
@router.get("/config")
async def get_auth_config():
    """
    Get Firebase authentication configuration for client apps

    Returns Firebase client configuration needed for web/mobile apps
    """
    try:
        firebase_manager = get_firebase_manager()
        config = firebase_manager.get_config()

        return {
            "status": "success",
            "config": config,
            "project_id": config.get("projectId"),
            "auth_domain": config.get("authDomain"),
            "features": {
                "email_password": True,
                "google_signin": True,
                "phone_auth": False,
                "anonymous_auth": False,
            },
        }

    except Exception as e:
        logger.error(f"Failed to get auth config: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get authentication configuration",
        )


@router.post("/verify-token", response_model=FirebaseUser)
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify Firebase ID token and return user information

    Args:
        credentials: Bearer token from Authorization header

    Returns:
        Authenticated user information
    """
    try:
        firebase_auth = get_firebase_auth()
        user = firebase_auth.verify_token(credentials.credentials)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Update last login
        firebase_auth.update_user_profile(user.uid, {"last_login": datetime.now()})

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
        )


@router.post("/create-custom-token")
@require_permission("admin:all")
async def create_custom_token(
    request: CustomTokenRequest, current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Create a custom token for a user (admin only)

    Args:
        request: Custom token request with UID and optional claims
        current_user: Current authenticated admin user

    Returns:
        Custom token
    """
    try:
        firebase_manager = get_firebase_manager()
        token = firebase_manager.create_custom_token(
            request.uid, request.additional_claims
        )

        if not token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create custom token",
            )

        return {"status": "success", "custom_token": token, "uid": request.uid}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Custom token creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create custom token",
        )


# User Management Endpoints
@router.get("/user/profile", response_model=FirebaseUser)
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

        # Merge Firebase Auth data with Firestore profile
        user_data = {
            "uid": current_user.uid,
            "email": current_user.email,
            "display_name": profile.get("display_name") or current_user.display_name,
            "email_verified": current_user.email_verified,
            "role": profile.get("role", "user"),
            "permissions": profile.get("permissions", []),
            "created_at": profile.get("created_at"),
            "last_login": profile.get("last_login"),
        }

        return FirebaseUser(**user_data)

    except Exception as e:
        logger.error(f"Failed to get user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile",
        )


@router.put("/user/profile")
async def update_user_profile(
    request: UserUpdateRequest, current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Update current user's profile

    Args:
        request: Profile update request
        current_user: Current authenticated user

    Returns:
        Success message
    """
    try:
        firebase_auth = get_firebase_auth()

        # Prepare updates
        updates: Dict[str, Any] = {}
        if request.display_name is not None:
            updates["display_name"] = request.display_name

        if request.settings is not None:
            updates["settings"] = request.settings

        updates["last_updated"] = datetime.now()

        # Update profile
        success = firebase_auth.update_user_profile(current_user.uid, updates)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update profile",
            )

        return {"status": "success", "message": "Profile updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile update failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile",
        )


@router.get("/user/permissions")
async def get_user_permissions(current_user: FirebaseUser = Depends(get_current_user)):
    """
    Get current user's permissions

    Args:
        current_user: Current authenticated user

    Returns:
        User permissions and role information
    """
    try:
        return {
            "status": "success",
            "user_id": current_user.uid,
            "role": current_user.role,
            "permissions": current_user.permissions,
            "is_admin": current_user.role == "admin",
            "can_access_dashboard": "access:dashboard" in current_user.permissions
            or current_user.role == "admin",
            "can_manage_tools": "manage:tools" in current_user.permissions
            or current_user.role == "admin",
        }

    except Exception as e:
        logger.error(f"Failed to get permissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user permissions",
        )


# Admin Endpoints
@router.get("/admin/users")
@require_permission("read:all_users")
async def list_users(
    limit: int = 50,
    offset: int = 0,
    current_user: FirebaseUser = Depends(get_current_user),
):
    """
    List all users (admin only)

    Args:
        limit: Maximum number of users to return
        offset: Offset for pagination
        current_user: Current authenticated admin user

    Returns:
        List of users
    """
    try:
        firebase_manager = get_firebase_manager()

        # Get users from Firestore
        if not firebase_manager.initialized:
            firebase_manager.initialize()

        users_ref = firebase_manager.db.collection("users")
        query = users_ref.limit(limit).offset(offset)

        users = []
        for doc in query.stream():
            user_data = doc.to_dict()
            user_data["uid"] = doc.id
            users.append(user_data)

        return {
            "status": "success",
            "users": users,
            "count": len(users),
            "limit": limit,
            "offset": offset,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to list users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list users",
        )


@router.post("/admin/users")
@require_permission("manage:users")
async def create_user(
    request: RegisterRequest, current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Create a new user (admin only)

    Args:
        request: User registration request
        current_user: Current authenticated admin user

    Returns:
        Created user information
    """
    try:
        firebase_manager = get_firebase_manager()
        firebase_auth = get_firebase_auth()

        # Create user in Firebase Auth
        uid = firebase_manager.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name,
        )

        if not uid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user in Firebase Auth",
            )

        # Create user profile
        success = firebase_auth.create_user_profile(
            uid=uid,
            email=request.email,
            display_name=request.display_name,
            role=request.role,
        )

        if not success:
            # Cleanup: delete from Firebase Auth if profile creation fails
            try:
                from firebase_admin import auth as firebase_admin_auth

                firebase_admin_auth.delete_user(uid)
            except:
                pass

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user profile",
            )

        return {
            "status": "success",
            "message": "User created successfully",
            "uid": uid,
            "email": request.email,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )


@router.delete("/admin/users/{user_id}")
@require_permission("manage:users")
async def delete_user(
    user_id: str, current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Delete a user (admin only)

    Args:
        user_id: User ID to delete
        current_user: Current authenticated admin user

    Returns:
        Success message
    """
    try:
        # Prevent admin from deleting themselves
        if user_id == current_user.uid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account",
            )

        firebase_manager = get_firebase_manager()

        # Delete from Firebase Auth
        from firebase_admin import auth as firebase_admin_auth

        firebase_admin_auth.delete_user(user_id)

        # Delete user profile from Firestore
        if firebase_manager.initialized:
            firebase_manager.db.collection("users").document(user_id).delete()

        return {"status": "success", "message": "User deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User deletion failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user",
        )


# Dashboard Stats Endpoint
@router.get("/dashboard/stats")
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

        # Add user information
        stats["user_info"] = {
            "uid": current_user.uid,
            "email": current_user.email,
            "display_name": current_user.display_name,
            "role": current_user.role,
            "is_admin": current_user.role == "admin",
        }

        return {"status": "success", "stats": stats}

    except Exception as e:
        logger.error(f"Failed to get dashboard stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get dashboard statistics",
        )


# Health Check Endpoint
@router.get("/health")
async def auth_health_check():
    """
    Authentication service health check

    Returns:
        Health status and configuration information
    """
    try:
        firebase_manager = get_firebase_manager()
        health_info = firebase_manager.health_check()

        return {
            "status": "healthy",
            "service": "Firebase Authentication",
            "timestamp": datetime.now().isoformat(),
            "firebase_status": health_info,
        }

    except Exception as e:
        logger.error(f"Auth health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "Firebase Authentication",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }
