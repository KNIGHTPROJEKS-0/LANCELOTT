#!/usr/bin/env python3
"""
SuperCompat Router - AI Compatibility Layer API Endpoints
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from api.auth import verify_token
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import StreamingResponse
from integrations.ai.supercompat_manager import get_supercompat_manager

router = APIRouter()


class TranslateRequest(BaseModel):
    """Request model for AI provider translation"""

    source_provider: str
    target_provider: str
    data: Dict[str, Any]


class CompatibilityRequest(BaseModel):
    """Request model for compatibility check"""

    source_provider: str
    target_provider: str
    feature: str


class StreamRequest(BaseModel):
    """Request model for streaming AI requests"""

    provider: str
    data: Dict[str, Any]


@router.get("/health")
async def supercompat_health():
    """Check SuperCompat health"""
    try:
        manager = get_supercompat_manager()
        is_healthy = await manager.health_check()
        status = manager.get_status()

        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "service_info": status,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start")
async def start_supercompat(
    port: int = 3001,
    background_tasks: BackgroundTasks = None,
    token: str = Depends(verify_token),
):
    """Start SuperCompat AI compatibility service"""
    try:
        manager = get_supercompat_manager()
        success = await manager.start_compat_service(port)

        if success:
            return {
                "status": "started",
                "port": port,
                "base_url": manager.base_url,
                "timestamp": datetime.utcnow().isoformat(),
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to start SuperCompat")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_supercompat(token: str = Depends(verify_token)):
    """Stop SuperCompat AI compatibility service"""
    try:
        manager = get_supercompat_manager()
        success = await manager.stop_compat_service()

        return {
            "status": "stopped" if success else "error",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_supercompat_status():
    """Get SuperCompat status and information"""
    try:
        manager = get_supercompat_manager()
        status = manager.get_status()
        info = await manager.get_service_info()

        return {
            "status": status,
            "info": info,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers")
async def get_supported_providers():
    """Get list of supported AI providers"""
    try:
        manager = get_supercompat_manager()
        providers = await manager.get_supported_providers()

        return {
            "providers": providers,
            "count": len(providers),
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate/request")
async def translate_ai_request(
    request: TranslateRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Translate AI request between providers"""
    try:
        manager = get_supercompat_manager()

        result = await manager.translate_request(
            request.source_provider, request.target_provider, request.data
        )

        # Log the translation
        background_tasks.add_task(
            log_translation,
            "request",
            request.source_provider,
            request.target_provider,
            True,
        )

        return {
            "translated": result,
            "source": request.source_provider,
            "target": request.target_provider,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate/response")
async def translate_ai_response(
    request: TranslateRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Translate AI response between providers"""
    try:
        manager = get_supercompat_manager()

        result = await manager.translate_response(
            request.source_provider, request.target_provider, request.data
        )

        # Log the translation
        background_tasks.add_task(
            log_translation,
            "response",
            request.source_provider,
            request.target_provider,
            True,
        )

        return {
            "translated": result,
            "source": request.source_provider,
            "target": request.target_provider,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compatibility")
async def check_compatibility(
    source: str, target: str, feature: str, token: str = Depends(verify_token)
):
    """Check feature compatibility between providers"""
    try:
        manager = get_supercompat_manager()

        compatible = await manager.validate_compatibility(source, target, feature)

        return {
            "compatible": compatible,
            "source": source,
            "target": target,
            "feature": feature,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def stream_compatible_request(
    request: StreamRequest, token: str = Depends(verify_token)
):
    """Stream compatible AI request"""
    try:
        manager = get_supercompat_manager()

        async def generate_stream():
            async for data in manager.stream_compatible_request(
                request.provider, request.data
            ):
                yield f"data: {data}\n\n"

        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache"},
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch/translate")
async def batch_translate(
    requests: List[TranslateRequest],
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Perform batch translation of AI requests/responses"""
    try:
        manager = get_supercompat_manager()
        results = []

        for req in requests:
            try:
                result = await manager.translate_request(
                    req.source_provider, req.target_provider, req.data
                )
                results.append(
                    {
                        "success": True,
                        "translated": result,
                        "source": req.source_provider,
                        "target": req.target_provider,
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "success": False,
                        "error": str(e),
                        "source": req.source_provider,
                        "target": req.target_provider,
                    }
                )

        # Log batch operation
        background_tasks.add_task(
            log_batch_translation,
            len(requests),
            sum(1 for r in results if r["success"]),
        )

        return {
            "results": results,
            "total": len(requests),
            "successful": sum(1 for r in results if r["success"]),
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_compat_info():
    """Get SuperCompat service information"""
    try:
        manager = get_supercompat_manager()
        info = await manager.get_service_info()
        providers = await manager.get_supported_providers()

        return {
            "service": "SuperCompat",
            "version": "1.0.0",
            "description": "AI Compatibility Layer for LANCELOTT Framework",
            "features": [
                "Multi-Provider Translation",
                "Request/Response Conversion",
                "Streaming Support",
                "Compatibility Validation",
                "Batch Processing",
            ],
            "supported_providers": providers,
            "info": info,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def log_translation(
    translation_type: str, source: str, target: str, success: bool
):
    """Background task to log AI translations"""
    import logging

    logger = logging.getLogger(__name__)
    status = "SUCCESS" if success else "FAILED"
    logger.info(
        f"AI Translation - Type: {translation_type}, {source} -> {target}, Status: {status}"
    )


async def log_batch_translation(total: int, successful: int):
    """Background task to log batch translations"""
    import logging

    logger = logging.getLogger(__name__)
    logger.info(
        f"Batch Translation - Total: {total}, Successful: {successful}, Failed: {total - successful}"
    )


# Include health check at router level
@router.get("/")
async def supercompat_root():
    """SuperCompat service root endpoint"""
    return {
        "service": "SuperCompat",
        "description": "AI Compatibility Layer for LANCELOTT Framework",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/start",
            "/stop",
            "/status",
            "/providers",
            "/translate/request",
            "/translate/response",
            "/compatibility",
            "/stream",
            "/batch/translate",
            "/info",
        ],
        "timestamp": datetime.utcnow().isoformat(),
    }
