"""
Firebase Integration Module for LANCELOTT Framework
Provides Firebase authentication, database, and storage services

Author: LANCELOTT Development Team
Version: 2.1.0
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import firebase_admin
    from firebase_admin import auth, credentials, firestore, storage
    from google.cloud import firestore as firestore_client
    from google.cloud.firestore_v1.base_query import FieldFilter
except ImportError as e:
    logging.error(f"Firebase dependencies not installed: {e}")
    firebase_admin = None

from core.config import get_settings

# Setup logging
logger = logging.getLogger(__name__)


class FirebaseManager:
    """
    Firebase Manager for LANCELOTT Framework
    Handles Firebase authentication, Firestore database, and Cloud Storage
    """

    def __init__(self):
        self.settings = get_settings()
        self.app = None
        self.db = None
        self.bucket = None
        self.initialized = False

    def initialize(self) -> bool:
        """
        Initialize Firebase Admin SDK with service account

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            if firebase_admin is None:
                logger.error("Firebase Admin SDK not available")
                return False

            # Check if already initialized
            if self.initialized:
                logger.info("Firebase already initialized")
                return True

            # Get service account path from environment
            service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
            if not service_account_path or not Path(service_account_path).exists():
                logger.error(
                    f"Firebase service account file not found: {service_account_path}"
                )
                return False

            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(service_account_path)

            # Get Firebase configuration
            firebase_config = {
                "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "")
            }

            # Initialize the app
            self.app = firebase_admin.initialize_app(cred, firebase_config)

            # Initialize Firestore database
            self.db = firestore.client()

            # Initialize Cloud Storage
            if firebase_config["storageBucket"]:
                self.bucket = storage.bucket()

            self.initialized = True
            logger.info("Firebase initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            return False

    def get_config(self) -> Dict[str, Any]:
        """
        Get Firebase client configuration for web applications

        Returns:
            Dict containing Firebase client configuration
        """
        return {
            "apiKey": os.getenv("FIREBASE_API_KEY"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "appId": os.getenv("FIREBASE_APP_ID"),
        }

    def verify_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Firebase ID token

        Args:
            id_token: Firebase ID token to verify

        Returns:
            Decoded token if valid, None otherwise
        """
        try:
            if not self.initialized:
                self.initialize()

            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return None

    def create_custom_token(
        self, uid: str, additional_claims: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Create a custom token for a user

        Args:
            uid: User ID
            additional_claims: Additional claims to include in token

        Returns:
            Custom token if successful, None otherwise
        """
        try:
            if not self.initialized:
                self.initialize()

            token = auth.create_custom_token(uid, additional_claims)
            return token.decode("utf-8")
        except Exception as e:
            logger.error(f"Custom token creation failed: {e}")
            return None

    def create_user(
        self, email: str, password: str, display_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Create a new user in Firebase Authentication

        Args:
            email: User email
            password: User password
            display_name: Optional display name

        Returns:
            User UID if successful, None otherwise
        """
        try:
            if not self.initialized:
                self.initialize()

            user_args = {"email": email, "password": password, "email_verified": False}

            if display_name:
                user_args["display_name"] = display_name

            user_record = auth.create_user(**user_args)
            logger.info(f"User created successfully: {user_record.uid}")
            return user_record.uid

        except Exception as e:
            logger.error(f"User creation failed: {e}")
            return None

    def get_user(self, uid: str) -> Optional[Dict[str, Any]]:
        """
        Get user information by UID

        Args:
            uid: User UID

        Returns:
            User information if found, None otherwise
        """
        try:
            if not self.initialized:
                self.initialize()

            user_record = auth.get_user(uid)
            return {
                "uid": user_record.uid,
                "email": user_record.email,
                "display_name": user_record.display_name,
                "email_verified": user_record.email_verified,
                "creation_time": user_record.user_metadata.creation_timestamp,
                "last_sign_in": user_record.user_metadata.last_sign_in_timestamp,
            }
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            return None

    def save_scan_result(
        self, collection: str, document_id: str, data: Dict[str, Any]
    ) -> bool:
        """
        Save scan results to Firestore

        Args:
            collection: Firestore collection name
            document_id: Document ID
            data: Data to save

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.initialized:
                self.initialize()

            doc_ref = self.db.collection(collection).document(document_id)
            doc_ref.set(data)
            logger.info(f"Scan result saved to {collection}/{document_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to save scan result: {e}")
            return False

    def get_scan_results(
        self, collection: str, user_id: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get scan results from Firestore

        Args:
            collection: Firestore collection name
            user_id: Optional user ID filter
            limit: Maximum number of results

        Returns:
            List of scan results
        """
        try:
            if not self.initialized:
                self.initialize()

            query = self.db.collection(collection)

            if user_id:
                query = query.where("user_id", "==", user_id)

            query = query.order_by(
                "timestamp", direction=firestore.Query.DESCENDING
            ).limit(limit)

            results = []
            for doc in query.stream():
                result = doc.to_dict()
                result["id"] = doc.id
                results.append(result)

            return results

        except Exception as e:
            logger.error(f"Failed to get scan results: {e}")
            return []

    def upload_file(self, file_path: str, destination_blob_name: str) -> Optional[str]:
        """
        Upload a file to Firebase Cloud Storage

        Args:
            file_path: Local file path
            destination_blob_name: Destination blob name in storage

        Returns:
            Public URL if successful, None otherwise
        """
        try:
            if not self.initialized or not self.bucket:
                self.initialize()

            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(file_path)

            # Make the blob publicly accessible
            blob.make_public()

            logger.info(f"File uploaded to {destination_blob_name}")
            return blob.public_url

        except Exception as e:
            logger.error(f"File upload failed: {e}")
            return None

    def delete_file(self, blob_name: str) -> bool:
        """
        Delete a file from Firebase Cloud Storage

        Args:
            blob_name: Blob name to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.initialized or not self.bucket:
                self.initialize()

            blob = self.bucket.blob(blob_name)
            blob.delete()

            logger.info(f"File deleted: {blob_name}")
            return True

        except Exception as e:
            logger.error(f"File deletion failed: {e}")
            return False

    def get_dashboard_url(self) -> str:
        """
        Get Firebase dashboard URL

        Returns:
            Dashboard URL
        """
        return os.getenv(
            "FIREBASE_DASHBOARD_URL", "https://console.firebase.google.com"
        )

    def health_check(self) -> Dict[str, Any]:
        """
        Perform Firebase health check

        Returns:
            Health check results
        """
        result = {
            "firebase_initialized": self.initialized,
            "admin_sdk_available": firebase_admin is not None,
            "service_account_configured": bool(
                os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
            ),
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "dashboard_url": self.get_dashboard_url(),
        }

        if self.initialized:
            try:
                # Test Firestore connection
                self.db.collection("health_check").document("test").get()
                result["firestore_connected"] = True
            except:
                result["firestore_connected"] = False

            try:
                # Test Storage connection
                if self.bucket:
                    list(self.bucket.list_blobs(max_results=1))
                    result["storage_connected"] = True
                else:
                    result["storage_connected"] = False
            except:
                result["storage_connected"] = False

        return result


# Global Firebase manager instance
firebase_manager = FirebaseManager()


def get_firebase_manager() -> FirebaseManager:
    """
    Get the global Firebase manager instance

    Returns:
        FirebaseManager instance
    """
    return firebase_manager
