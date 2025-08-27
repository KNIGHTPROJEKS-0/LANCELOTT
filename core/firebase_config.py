#!/usr/bin/env python3
"""
Firebase Configuration Module
Handles Firebase Admin SDK initialization and connection management
"""

import base64
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import firebase_admin
from firebase_admin import auth, credentials, firestore, storage
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import firestore as firestore_client

logger = logging.getLogger(__name__)


class FirebaseConfig:
    """
    Firebase Configuration and Connection Manager

    Handles Firebase Admin SDK initialization with multiple credential sources:
    1. Service account JSON file
    2. Base64 encoded environment variable
    3. Default application credentials
    """

    def __init__(self):
        self.app: Optional[firebase_admin.App] = None
        self.db: Optional[firestore_client.Client] = None
        self.bucket: Optional[Any] = None
        self.is_initialized = False
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load Firebase configuration from environment variables

        Returns:
            Dict containing Firebase configuration
        """
        return {
            "project_id": os.getenv("FIREBASE_PROJECT_ID", "lancelott-cybersec"),
            "storage_bucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "service_account_path": os.getenv(
                "FIREBASE_SERVICE_ACCOUNT_PATH", "firebase-service-account.json"
            ),
            "service_account_base64": os.getenv("FIREBASE_SERVICE_ACCOUNT_BASE64"),
            "database_url": os.getenv("FIREBASE_DATABASE_URL"),
            "api_key": os.getenv("FIREBASE_API_KEY"),
            "auth_domain": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "messaging_sender_id": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "app_id": os.getenv("FIREBASE_APP_ID"),
            "measurement_id": os.getenv("FIREBASE_MEASUREMENT_ID"),
        }

    def _get_credentials(self) -> Optional[credentials.Certificate]:
        """
        Get Firebase credentials from multiple sources

        Returns:
            Firebase credentials or None if not found
        """
        # Try service account file first
        service_account_path = Path(self.config["service_account_path"])
        if service_account_path.exists():
            logger.info(f"Using service account file: {service_account_path}")
            try:
                return credentials.Certificate(str(service_account_path))
            except Exception as e:
                logger.warning(f"Failed to load service account file: {e}")

        # Try base64 encoded credentials
        if self.config["service_account_base64"]:
            logger.info("Using base64 encoded service account")
            try:
                decoded_credentials = base64.b64decode(
                    self.config["service_account_base64"]
                ).decode("utf-8")
                credential_dict = json.loads(decoded_credentials)
                return credentials.Certificate(credential_dict)
            except Exception as e:
                logger.warning(f"Failed to decode base64 credentials: {e}")

        # Try default application credentials
        try:
            logger.info("Attempting to use default application credentials")
            return credentials.ApplicationDefault()
        except DefaultCredentialsError as e:
            logger.warning(f"Default credentials not available: {e}")

        return None

    def initialize(self) -> bool:
        """
        Initialize Firebase Admin SDK

        Returns:
            True if initialization successful, False otherwise
        """
        if self.is_initialized:
            logger.info("Firebase already initialized")
            return True

        try:
            # Get credentials
            cred = self._get_credentials()
            if not cred:
                logger.error("No valid Firebase credentials found")
                return False

            # Initialize Firebase app
            config = {"projectId": self.config["project_id"]}

            if self.config["storage_bucket"]:
                config["storageBucket"] = self.config["storage_bucket"]

            if self.config["database_url"]:
                config["databaseURL"] = self.config["database_url"]

            # Check if app already exists
            try:
                self.app = firebase_admin.get_app()
                logger.info("Using existing Firebase app")
            except ValueError:
                # App doesn't exist, create new one
                self.app = firebase_admin.initialize_app(
                    cred, config, name="lancelott-main"
                )
                logger.info("Firebase app initialized successfully")

            # Initialize Firestore
            self.db = firestore.client(app=self.app)
            logger.info("Firestore client initialized")

            # Initialize Storage (if bucket configured)
            if self.config["storage_bucket"]:
                self.bucket = storage.bucket(app=self.app)
                logger.info("Storage bucket initialized")

            self.is_initialized = True
            logger.info("Firebase configuration completed successfully")
            return True

        except Exception as e:
            logger.error(f"Firebase initialization failed: {e}")
            return False

    def get_firestore_client(self) -> Optional[firestore_client.Client]:
        """
        Get Firestore client instance

        Returns:
            Firestore client or None if not initialized
        """
        if not self.is_initialized:
            logger.warning("Firebase not initialized. Call initialize() first.")
            return None
        return self.db

    def get_storage_bucket(self) -> Optional[Any]:
        """
        Get Storage bucket instance

        Returns:
            Storage bucket or None if not configured
        """
        if not self.is_initialized:
            logger.warning("Firebase not initialized. Call initialize() first.")
            return None
        return self.bucket

    def get_auth(self) -> Optional[Any]:
        """
        Get Firebase Auth instance

        Returns:
            Firebase Auth instance or None if not initialized
        """
        if not self.is_initialized:
            logger.warning("Firebase not initialized. Call initialize() first.")
            return None
        return auth

    def verify_connection(self) -> Dict[str, Any]:
        """
        Verify Firebase connection and return status

        Returns:
            Dictionary with connection status and details
        """
        status = {
            "initialized": self.is_initialized,
            "firestore": False,
            "storage": False,
            "auth": False,
            "project_id": self.config["project_id"],
            "error": None,
        }

        if not self.is_initialized:
            status["error"] = "Firebase not initialized"
            return status

        try:
            # Test Firestore connection
            if self.db:
                # Try to access a collection (this will test the connection)
                collections = list(self.db.collections())
                status["firestore"] = True
                logger.info("Firestore connection verified")
        except Exception as e:
            logger.warning(f"Firestore connection test failed: {e}")
            status["error"] = f"Firestore: {str(e)}"

        try:
            # Test Storage connection
            if self.bucket:
                # Test bucket access
                self.bucket.name
                status["storage"] = True
                logger.info("Storage connection verified")
        except Exception as e:
            logger.warning(f"Storage connection test failed: {e}")
            if status["error"]:
                status["error"] += f"; Storage: {str(e)}"
            else:
                status["error"] = f"Storage: {str(e)}"

        try:
            # Test Auth connection
            auth.list_users(app=self.app, max_results=1)
            status["auth"] = True
            logger.info("Auth connection verified")
        except Exception as e:
            logger.warning(f"Auth connection test failed: {e}")
            if status["error"]:
                status["error"] += f"; Auth: {str(e)}"
            else:
                status["error"] = f"Auth: {str(e)}"

        return status

    def log_event(self, collection: str, event_data: Dict[str, Any]) -> bool:
        """
        Log an event to Firestore

        Args:
            collection: Firestore collection name
            event_data: Event data to log

        Returns:
            True if successful, False otherwise
        """
        if not self.db:
            logger.warning("Firestore not available for logging")
            return False

        try:
            # Add timestamp if not present
            if "timestamp" not in event_data:
                event_data["timestamp"] = firestore.SERVER_TIMESTAMP

            # Add to collection
            doc_ref = self.db.collection(collection).add(event_data)
            logger.debug(f"Event logged to {collection}: {doc_ref[1].id}")
            return True

        except Exception as e:
            logger.error(f"Failed to log event to {collection}: {e}")
            return False

    def cleanup(self):
        """
        Cleanup Firebase resources
        """
        try:
            if self.app:
                firebase_admin.delete_app(self.app)
                logger.info("Firebase app cleaned up")
        except Exception as e:
            logger.warning(f"Firebase cleanup error: {e}")

        self.app = None
        self.db = None
        self.bucket = None
        self.is_initialized = False


# Global Firebase instance
_firebase_instance = None


def get_firebase() -> FirebaseConfig:
    """
    Get global Firebase configuration instance

    Returns:
        FirebaseConfig instance
    """
    global _firebase_instance
    if _firebase_instance is None:
        _firebase_instance = FirebaseConfig()
    return _firebase_instance


def initialize_firebase() -> bool:
    """
    Initialize global Firebase instance

    Returns:
        True if successful, False otherwise
    """
    firebase_config = get_firebase()
    return firebase_config.initialize()


def get_firestore() -> Optional[firestore_client.Client]:
    """
    Get Firestore client from global instance

    Returns:
        Firestore client or None
    """
    firebase_config = get_firebase()
    return firebase_config.get_firestore_client()


def log_to_firebase(collection: str, data: Dict[str, Any]) -> bool:
    """
    Log data to Firebase collection

    Args:
        collection: Collection name
        data: Data to log

    Returns:
        True if successful, False otherwise
    """
    firebase_config = get_firebase()
    return firebase_config.log_event(collection, data)
