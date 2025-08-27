"""
Firebase Authentication and Services Wrapper for LANCELOTT Framework
Enhanced Firebase functionality with LANCELOTT-specific features

Author: LANCELOTT Development Team
Version: 2.1.0
"""

import json
import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Dict, List, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from integrations.firebase_integration import FirebaseManager, get_firebase_manager

# Setup logging
logger = logging.getLogger(__name__)

# Security scheme for FastAPI
security = HTTPBearer()


class FirebaseUser(BaseModel):
    """Firebase User model for LANCELOTT"""

    uid: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    email_verified: bool = False
    role: str = "user"
    permissions: List[str] = []
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None


class ScanResult(BaseModel):
    """Scan result model for Firebase storage"""

    id: Optional[str] = None
    user_id: str
    tool_name: str
    target: str
    status: str  # pending, running, completed, failed
    results: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    timestamp: datetime
    duration: Optional[int] = None  # in seconds


class FirebaseAuth:
    """
    Firebase Authentication wrapper for LANCELOTT
    """

    def __init__(self):
        self.firebase_manager = get_firebase_manager()

    def verify_token(self, token: str) -> Optional[FirebaseUser]:
        """
        Verify Firebase ID token and return user information

        Args:
            token: Firebase ID token

        Returns:
            FirebaseUser if valid, None otherwise
        """
        try:
            decoded_token = self.firebase_manager.verify_token(token)
            if not decoded_token:
                return None

            # Get additional user data from Firestore
            user_data = self.get_user_profile(decoded_token.get("uid"))

            return FirebaseUser(
                uid=decoded_token.get("uid"),
                email=decoded_token.get("email"),
                display_name=user_data.get("display_name") or decoded_token.get("name"),
                email_verified=decoded_token.get("email_verified", False),
                role=user_data.get("role", "user"),
                permissions=user_data.get("permissions", []),
                created_at=user_data.get("created_at"),
                last_login=datetime.now(),
            )

        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return None

    def create_user_profile(
        self,
        uid: str,
        email: str,
        display_name: Optional[str] = None,
        role: str = "user",
        permissions: Optional[List[str]] = None,
    ) -> bool:
        """
        Create user profile in Firestore

        Args:
            uid: User UID
            email: User email
            display_name: Display name
            role: User role
            permissions: User permissions

        Returns:
            True if successful, False otherwise
        """
        try:
            if permissions is None:
                permissions = ["read:own_scans", "create:scans"]

            user_profile = {
                "uid": uid,
                "email": email,
                "display_name": display_name,
                "role": role,
                "permissions": permissions,
                "created_at": datetime.now(),
                "last_login": datetime.now(),
                "scan_count": 0,
                "settings": {
                    "theme": "dark",
                    "notifications": True,
                    "auto_scan": False,
                },
            }

            return self.firebase_manager.save_scan_result("users", uid, user_profile)

        except Exception as e:
            logger.error(f"Failed to create user profile: {e}")
            return False

    def get_user_profile(self, uid: str) -> Dict[str, Any]:
        """
        Get user profile from Firestore

        Args:
            uid: User UID

        Returns:
            User profile data
        """
        try:
            if not self.firebase_manager.initialized:
                self.firebase_manager.initialize()

            user_ref = self.firebase_manager.db.collection("users").document(uid)
            user_doc = user_ref.get()

            if user_doc.exists:
                return user_doc.to_dict()
            else:
                return {}

        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            return {}

    def update_user_profile(self, uid: str, updates: Dict[str, Any]) -> bool:
        """
        Update user profile in Firestore

        Args:
            uid: User UID
            updates: Fields to update

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.firebase_manager.initialized:
                self.firebase_manager.initialize()

            updates["last_updated"] = datetime.now()
            user_ref = self.firebase_manager.db.collection("users").document(uid)
            user_ref.update(updates)

            logger.info(f"User profile updated: {uid}")
            return True

        except Exception as e:
            logger.error(f"Failed to update user profile: {e}")
            return False

    def has_permission(self, user: FirebaseUser, permission: str) -> bool:
        """
        Check if user has specific permission

        Args:
            user: Firebase user
            permission: Permission to check

        Returns:
            True if user has permission, False otherwise
        """
        return permission in user.permissions or user.role == "admin"


class FirebaseService:
    """
    Firebase Services wrapper for LANCELOTT operations
    """

    def __init__(self):
        self.firebase_manager = get_firebase_manager()

    def save_scan_result(self, user_id: str, scan_data: ScanResult) -> str:
        """
        Save scan result to Firebase

        Args:
            user_id: User ID
            scan_data: Scan result data

        Returns:
            Document ID if successful, empty string otherwise
        """
        try:
            # Generate document ID
            doc_id = f"{user_id}_{scan_data.tool_name}_{int(scan_data.timestamp.timestamp())}"

            # Prepare data for storage
            data = scan_data.dict()
            data["timestamp"] = scan_data.timestamp.isoformat()

            # Save to Firestore
            if self.firebase_manager.save_scan_result("scan_results", doc_id, data):
                # Update user scan count
                self.increment_user_scan_count(user_id)
                return doc_id

            return ""

        except Exception as e:
            logger.error(f"Failed to save scan result: {e}")
            return ""

    def get_user_scans(self, user_id: str, limit: int = 50) -> List[ScanResult]:
        """
        Get user's scan results

        Args:
            user_id: User ID
            limit: Maximum number of results

        Returns:
            List of scan results
        """
        try:
            results = self.firebase_manager.get_scan_results(
                "scan_results", user_id, limit
            )

            scan_results = []
            for result in results:
                # Convert timestamp back to datetime
                if "timestamp" in result and isinstance(result["timestamp"], str):
                    result["timestamp"] = datetime.fromisoformat(result["timestamp"])

                scan_results.append(ScanResult(**result))

            return scan_results

        except Exception as e:
            logger.error(f"Failed to get user scans: {e}")
            return []

    def get_scan_by_id(self, scan_id: str) -> Optional[ScanResult]:
        """
        Get specific scan result by ID

        Args:
            scan_id: Scan result ID

        Returns:
            Scan result if found, None otherwise
        """
        try:
            if not self.firebase_manager.initialized:
                self.firebase_manager.initialize()

            doc_ref = self.firebase_manager.db.collection("scan_results").document(
                scan_id
            )
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                if "timestamp" in data and isinstance(data["timestamp"], str):
                    data["timestamp"] = datetime.fromisoformat(data["timestamp"])
                return ScanResult(**data)

            return None

        except Exception as e:
            logger.error(f"Failed to get scan by ID: {e}")
            return None

    def update_scan_status(
        self, scan_id: str, status: str, results: Optional[Dict] = None
    ) -> bool:
        """
        Update scan status and results

        Args:
            scan_id: Scan ID
            status: New status
            results: Optional results data

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.firebase_manager.initialized:
                self.firebase_manager.initialize()

            updates = {"status": status, "updated_at": datetime.now().isoformat()}

            if results:
                updates["results"] = results

            if status == "completed":
                updates["completed_at"] = datetime.now().isoformat()

            doc_ref = self.firebase_manager.db.collection("scan_results").document(
                scan_id
            )
            doc_ref.update(updates)

            return True

        except Exception as e:
            logger.error(f"Failed to update scan status: {e}")
            return False

    def increment_user_scan_count(self, user_id: str) -> bool:
        """
        Increment user's scan count

        Args:
            user_id: User ID

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.firebase_manager.initialized:
                self.firebase_manager.initialize()

            from google.cloud.firestore_v1 import Increment

            user_ref = self.firebase_manager.db.collection("users").document(user_id)
            user_ref.update({"scan_count": Increment(1)})

            return True

        except Exception as e:
            logger.error(f"Failed to increment scan count: {e}")
            return False

    def get_dashboard_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get dashboard statistics for user

        Args:
            user_id: User ID

        Returns:
            Dashboard statistics
        """
        try:
            # Get user profile
            auth = FirebaseAuth()
            user_profile = auth.get_user_profile(user_id)

            # Get recent scans
            recent_scans = self.get_user_scans(user_id, 10)

            # Calculate statistics
            total_scans = user_profile.get("scan_count", 0)
            completed_scans = len([s for s in recent_scans if s.status == "completed"])
            failed_scans = len([s for s in recent_scans if s.status == "failed"])
            running_scans = len([s for s in recent_scans if s.status == "running"])

            # Tool usage statistics
            tool_usage: Dict[str, int] = {}
            for scan in recent_scans:
                tool_usage[scan.tool_name] = tool_usage.get(scan.tool_name, 0) + 1

            return {
                "user_id": user_id,
                "total_scans": total_scans,
                "completed_scans": completed_scans,
                "failed_scans": failed_scans,
                "running_scans": running_scans,
                "tool_usage": tool_usage,
                "recent_scans": len(recent_scans),
                "last_scan": (
                    recent_scans[0].timestamp.isoformat() if recent_scans else None
                ),
            }

        except Exception as e:
            logger.error(f"Failed to get dashboard stats: {e}")
            return {}


# FastAPI Dependencies
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> FirebaseUser:
    """
    FastAPI dependency to get current authenticated user

    Args:
        credentials: HTTP authorization credentials

    Returns:
        Authenticated Firebase user

    Raises:
        HTTPException: If authentication fails
    """
    auth = FirebaseAuth()
    user = auth.verify_token(credentials.credentials)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_permission(permission: str):
    """
    Decorator to require specific permission

    Args:
        permission: Required permission

    Returns:
        Decorator function
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get user from kwargs (injected by FastAPI)
            user = kwargs.get("current_user")
            if not user or not isinstance(user, FirebaseUser):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )

            auth = FirebaseAuth()
            if not auth.has_permission(user, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{permission}' required",
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator


# Global instances
firebase_auth = FirebaseAuth()
firebase_service = FirebaseService()


def get_firebase_auth() -> FirebaseAuth:
    """Get Firebase authentication instance"""
    return firebase_auth


def get_firebase_service() -> FirebaseService:
    """Get Firebase service instance"""
    return firebase_service
