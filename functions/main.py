"""
Firebase Cloud Functions for LANCELOTT Framework
Main entry point for serverless backend deployment

This module provides Firebase Cloud Functions integration for the LANCELOTT
security toolkit, enabling serverless deployment while maintaining full
FastAPI functionality.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from firebase_admin import credentials, initialize_app

# Firebase Functions imports
from firebase_functions import https_fn, options

# FastAPI app import
from app import app as fastapi_app

# Initialize Firebase Admin
try:
    # Try to initialize with service account
    cred_path = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_PATH",
        "./config/firebase/lancelott-z9dko-firebase-adminsdk-fbsvc-887499da9a.json",
    )
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        initialize_app(cred)
    else:
        # Initialize with default credentials in Cloud environment
        initialize_app()
except Exception as e:
    print(f"Warning: Firebase initialization failed: {e}")


# Configure CORS for Firebase hosting
@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=["*"],
        cors_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        cors_allow_headers=["Content-Type", "Authorization"],
    ),
    memory=options.MemoryOption.MB_512,
    timeout_sec=540,
)
def lancelott_api(req: https_fn.Request) -> https_fn.Response:
    """
    Main Firebase Cloud Function for LANCELOTT API

    This function serves the entire FastAPI application through Firebase Functions,
    providing serverless execution with automatic scaling.

    Args:
        req: Firebase Functions HTTP request

    Returns:
        Firebase Functions HTTP response
    """
    try:
        # Create ASGI app wrapper for Firebase Functions
        from functions.asgi_adapter import ASGIAdapter

        adapter = ASGIAdapter(fastapi_app)
        return adapter(req)

    except Exception as e:
        import traceback

        error_details = traceback.format_exc()

        return https_fn.Response(
            response=f"LANCELOTT API Error: {str(e)}\n\nDetails:\n{error_details}",
            status=500,
            headers={"Content-Type": "text/plain", "Access-Control-Allow-Origin": "*"},
        )


# Health check function
@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=["*"], cors_methods=["GET"], cors_allow_headers=["Content-Type"]
    )
)
def health_check(req: https_fn.Request) -> https_fn.Response:
    """
    Health check endpoint for Firebase Functions

    Returns basic health status and Firebase connectivity information.
    """
    try:
        from firebase_admin import firestore

        # Test Firebase connectivity
        db = firestore.client()

        # Basic health check
        health_status = {
            "status": "healthy",
            "service": "LANCELOTT Firebase Functions",
            "version": "2.1.0",
            "firebase_connected": True,
            "timestamp": str(__import__("datetime").datetime.now()),
        }

        return https_fn.Response(
            response=__import__("json").dumps(health_status),
            status=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        )

    except Exception as e:
        error_response = {
            "status": "unhealthy",
            "service": "LANCELOTT Firebase Functions",
            "error": str(e),
            "firebase_connected": False,
            "timestamp": str(__import__("datetime").datetime.now()),
        }

        return https_fn.Response(
            response=__import__("json").dumps(error_response),
            status=503,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        )


# Scheduled function for system maintenance
@https_fn.on_schedule(schedule="0 2 * * *")  # Daily at 2 AM
def daily_maintenance(event) -> None:
    """
    Daily maintenance function for LANCELOTT system

    Performs cleanup tasks, health checks, and system optimization.
    """
    try:
        from datetime import datetime, timedelta

        from firebase_admin import firestore

        db = firestore.client()

        # Clean up old temporary files
        cutoff_date = datetime.now() - timedelta(days=7)

        # Clean old scan results (keep last 30 days)
        old_scans = (
            db.collection("scans")
            .where("created_at", "<", cutoff_date - timedelta(days=23))
            .limit(100)
            .get()
        )

        for scan in old_scans:
            scan.reference.delete()

        # Log maintenance completion
        db.collection("system_logs").add(
            {
                "type": "maintenance",
                "action": "daily_cleanup",
                "timestamp": datetime.now(),
                "items_cleaned": len(old_scans),
            }
        )

        print(f"Daily maintenance completed: {len(old_scans)} old items cleaned")

    except Exception as e:
        print(f"Daily maintenance failed: {e}")

        # Log error
        try:
            db.collection("system_logs").add(
                {
                    "type": "error",
                    "action": "daily_maintenance",
                    "error": str(e),
                    "timestamp": datetime.now(),
                }
            )
        except:
            pass


# Security scan webhook function
@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=["*"],
        cors_methods=["POST"],
        cors_allow_headers=["Content-Type", "Authorization"],
    )
)
def scan_webhook(req: https_fn.Request) -> https_fn.Response:
    """
    Webhook handler for security scan results

    Receives scan results from external tools and processes them through
    the LANCELOTT pipeline.
    """
    try:
        import json

        from firebase_admin import firestore

        # Parse request data
        if req.method != "POST":
            return https_fn.Response(
                response="Method not allowed",
                status=405,
                headers={"Access-Control-Allow-Origin": "*"},
            )

        data = req.get_json()
        if not data:
            return https_fn.Response(
                response="No data provided",
                status=400,
                headers={"Access-Control-Allow-Origin": "*"},
            )

        # Store scan result in Firestore
        db = firestore.client()
        scan_ref = db.collection("scan_webhooks").add(
            {
                "data": data,
                "timestamp": __import__("datetime").datetime.now(),
                "source_ip": req.headers.get("X-Forwarded-For", "unknown"),
                "processed": False,
            }
        )

        response_data = {
            "status": "received",
            "scan_id": scan_ref[1].id,
            "message": "Scan data received and queued for processing",
        }

        return https_fn.Response(
            response=json.dumps(response_data),
            status=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        )

    except Exception as e:
        return https_fn.Response(
            response=f"Webhook processing failed: {str(e)}",
            status=500,
            headers={"Access-Control-Allow-Origin": "*"},
        )
