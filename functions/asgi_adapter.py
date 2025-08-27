"""
ASGI Adapter for Firebase Functions
Adapts FastAPI ASGI application to work with Firebase Functions HTTP interface

This adapter allows Firebase Functions to serve FastAPI applications
by converting between Firebase Functions request/response format and ASGI.
"""

import asyncio
import io
import sys
from typing import Any, Dict, List, Tuple
from urllib.parse import parse_qs, unquote

from firebase_functions import https_fn


class ASGIAdapter:
    """
    ASGI Adapter for Firebase Functions

    Converts Firebase Functions HTTP requests to ASGI format and back,
    allowing FastAPI applications to run in Firebase Functions.
    """

    def __init__(self, app):
        """
        Initialize the ASGI adapter

        Args:
            app: FastAPI application instance
        """
        self.app = app

    def __call__(self, request: https_fn.Request) -> https_fn.Response:
        """
        Handle Firebase Functions HTTP request

        Args:
            request: Firebase Functions HTTP request

        Returns:
            Firebase Functions HTTP response
        """
        try:
            # Run the ASGI application
            return asyncio.run(self._handle_async(request))
        except Exception as e:
            import traceback

            error_details = traceback.format_exc()

            return https_fn.Response(
                response=f"ASGI Adapter Error: {str(e)}\n\nDetails:\n{error_details}",
                status=500,
                headers={
                    "Content-Type": "text/plain",
                    "Access-Control-Allow-Origin": "*",
                },
            )

    async def _handle_async(self, request: https_fn.Request) -> https_fn.Response:
        """
        Async handler for ASGI application

        Args:
            request: Firebase Functions HTTP request

        Returns:
            Firebase Functions HTTP response
        """
        # Convert Firebase request to ASGI scope
        scope = self._build_scope(request)

        # Prepare response handling
        response_started = False
        status_code = 200
        response_headers = []
        body_parts = []

        async def receive():
            """ASGI receive callable"""
            # For HTTP, we only need to send the body once
            return {
                "type": "http.request",
                "body": request.data if request.data else b"",
                "more_body": False,
            }

        async def send(message):
            """ASGI send callable"""
            nonlocal response_started, status_code, response_headers, body_parts

            if message["type"] == "http.response.start":
                response_started = True
                status_code = message["status"]
                response_headers = message.get("headers", [])

            elif message["type"] == "http.response.body":
                body = message.get("body", b"")
                if body:
                    body_parts.append(body)

        # Call the ASGI application
        await self.app(scope, receive, send)

        # Build the response
        response_body = b"".join(body_parts)

        # Convert headers to Firebase format
        headers_dict = {}
        for header_pair in response_headers:
            if isinstance(header_pair, (list, tuple)) and len(header_pair) == 2:
                key = header_pair[0]
                value = header_pair[1]

                # Decode bytes to string if needed
                if isinstance(key, bytes):
                    key = key.decode("latin-1")
                if isinstance(value, bytes):
                    value = value.decode("latin-1")

                headers_dict[key] = value

        # Always add CORS headers
        headers_dict.update(
            {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            }
        )

        return https_fn.Response(
            response=response_body.decode("utf-8") if response_body else "",
            status=status_code,
            headers=headers_dict,
        )

    def _build_scope(self, request: https_fn.Request) -> Dict[str, Any]:
        """
        Build ASGI scope from Firebase request

        Args:
            request: Firebase Functions HTTP request

        Returns:
            ASGI scope dictionary
        """
        # Parse URL components
        url = request.url
        path = request.path
        query_string = request.query_string.encode() if request.query_string else b""

        # Build headers
        headers = []
        for key, value in request.headers.items():
            headers.append([key.lower().encode(), value.encode()])

        # Build scope
        scope = {
            "type": "http",
            "method": request.method.upper(),
            "path": unquote(path),
            "raw_path": path.encode(),
            "query_string": query_string,
            "root_path": "",
            "scheme": "https",
            "server": ("localhost", 443),
            "headers": headers,
            "asgi": {"version": "3.0", "spec_version": "2.1"},
        }

        return scope
