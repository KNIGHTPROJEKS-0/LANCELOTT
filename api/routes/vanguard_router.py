#!/usr/bin/env python3
"""
Vanguard Router - Obfuscation and Security Tools API Endpoints
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from api.auth import verify_token
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from integrations.security.vanguard_manager import (
    ObfuscationRequest,
    ObfuscationType,
    get_vanguard_manager,
)

router = APIRouter()


class ObfuscateFileRequest(BaseModel):
    """Request model for file obfuscation"""

    tool: str
    target_file: str
    obfuscation_type: str
    options: Dict[str, Any] = {}
    output_path: Optional[str] = None


class BuildToolRequest(BaseModel):
    """Request model for building a tool"""

    tool: str


class ProtectionRecommendationRequest(BaseModel):
    """Request model for protection recommendations"""

    file_path: str


@router.get("/health")
async def vanguard_health():
    """Check Vanguard tools health"""
    try:
        manager = get_vanguard_manager()
        status = manager.get_status()

        return {
            "status": "healthy",
            "service_info": status,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tools")
async def list_obfuscation_tools():
    """List all available obfuscation tools"""
    try:
        manager = get_vanguard_manager()
        tools = await manager.list_available_tools()

        return {
            "tools": tools,
            "count": len(tools),
            "available": sum(1 for tool in tools if tool["available"]),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tools/{tool_id}")
async def get_tool_info(tool_id: str):
    """Get detailed information about a specific tool"""
    try:
        manager = get_vanguard_manager()
        tool_info = await manager.get_tool_info(tool_id)

        if not tool_info:
            raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")

        return {
            "tool": tool_info,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tools/{tool_id}/build")
async def build_tool(
    tool_id: str, background_tasks: BackgroundTasks, token: str = Depends(verify_token)
):
    """Build a specific obfuscation tool"""
    try:
        manager = get_vanguard_manager()

        # Check if tool exists
        tool_info = await manager.get_tool_info(tool_id)
        if not tool_info:
            raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")

        if not tool_info["build_required"]:
            return {
                "status": "skipped",
                "message": f"Tool {tool_id} does not require building",
                "timestamp": datetime.utcnow().isoformat(),
            }

        # Start build process
        success = await manager.build_tool(tool_id)

        # Log the build
        background_tasks.add_task(log_tool_build, tool_id, success)

        return {
            "status": "success" if success else "failed",
            "tool": tool_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/obfuscate")
async def obfuscate_file(
    request: ObfuscateFileRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Obfuscate a file using specified tool"""
    try:
        manager = get_vanguard_manager()

        # Validate obfuscation type
        try:
            obf_type = ObfuscationType(request.obfuscation_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid obfuscation type: {request.obfuscation_type}",
            )

        # Create obfuscation request
        obf_request = ObfuscationRequest(
            tool=request.tool,
            target_file=request.target_file,
            obfuscation_type=obf_type,
            options=request.options,
            output_path=request.output_path,
        )

        # Execute obfuscation
        result = await manager.obfuscate_file(obf_request)

        # Log the obfuscation
        background_tasks.add_task(
            log_obfuscation, request.tool, request.target_file, result.success
        )

        return {
            "result": {
                "success": result.success,
                "output_file": result.output_file,
                "tool_used": result.tool_used,
                "obfuscation_type": result.obfuscation_type,
                "protection_level": result.protection_level,
                "size_change": result.size_change,
                "execution_time": result.execution_time,
                "warnings": result.warnings,
                "error_message": result.error_message,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-and-obfuscate")
async def upload_and_obfuscate(
    file: UploadFile = File(...),
    tool: str = "auto",
    obfuscation_type: str = "auto",
    options: str = "{}",
    background_tasks: BackgroundTasks = BackgroundTasks(),
    token: str = Depends(verify_token),
):
    """Upload a file and obfuscate it"""
    try:
        import json
        import tempfile

        manager = get_vanguard_manager()

        # Parse options
        try:
            parsed_options = json.loads(options)
        except json.JSONDecodeError:
            parsed_options = {}

        # Create temporary file
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=Path(file.filename).suffix
        ) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Auto-detect tool and type if requested
            if tool == "auto" or obfuscation_type == "auto":
                recommendations = await manager.get_protection_recommendations(
                    temp_file_path
                )
                if recommendations:
                    if tool == "auto":
                        tool = recommendations[0]["tool"]
                    if obfuscation_type == "auto":
                        file_ext = Path(file.filename).suffix.lower()
                        if file_ext in [".py"]:
                            obfuscation_type = "python"
                        elif file_ext in [".js", ".ts"]:
                            obfuscation_type = "javascript"
                        elif file_ext in [".jar", ".class"]:
                            obfuscation_type = "java"
                        else:
                            obfuscation_type = "binary"
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="Could not auto-detect appropriate obfuscation tool",
                    )

            # Validate obfuscation type
            try:
                obf_type = ObfuscationType(obfuscation_type)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid obfuscation type: {obfuscation_type}",
                )

            # Create output path
            output_filename = (
                f"{Path(file.filename).stem}_obfuscated{Path(file.filename).suffix}"
            )
            output_path = Path(temp_file_path).parent / output_filename

            # Create obfuscation request
            obf_request = ObfuscationRequest(
                tool=tool,
                target_file=temp_file_path,
                obfuscation_type=obf_type,
                options=parsed_options,
                output_path=str(output_path),
            )

            # Execute obfuscation
            result = await manager.obfuscate_file(obf_request)

            # Log the obfuscation
            background_tasks.add_task(
                log_obfuscation, tool, file.filename, result.success
            )

            if (
                result.success
                and result.output_file
                and Path(result.output_file).exists()
            ):
                # Return the obfuscated file
                return FileResponse(
                    path=result.output_file,
                    filename=output_filename,
                    media_type="application/octet-stream",
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Obfuscation failed: {result.error_message}",
                )

        finally:
            # Cleanup temporary files
            try:
                Path(temp_file_path).unlink()
                if result.success and result.output_file:
                    background_tasks.add_task(cleanup_temp_file, result.output_file)
            except:
                pass

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommendations")
async def get_protection_recommendations(
    request: ProtectionRecommendationRequest, token: str = Depends(verify_token)
):
    """Get obfuscation tool recommendations for a file"""
    try:
        manager = get_vanguard_manager()
        recommendations = await manager.get_protection_recommendations(
            request.file_path
        )

        return {
            "file_path": request.file_path,
            "recommendations": recommendations,
            "count": len(recommendations),
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_vanguard_status():
    """Get Vanguard system status"""
    try:
        manager = get_vanguard_manager()
        status = manager.get_status()

        return {
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types")
async def get_obfuscation_types():
    """Get available obfuscation types"""
    try:
        types = [
            {"type": obf_type.value, "description": _get_type_description(obf_type)}
            for obf_type in ObfuscationType
        ]

        return {
            "types": types,
            "count": len(types),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _get_type_description(obf_type: ObfuscationType) -> str:
    """Get description for obfuscation type"""
    descriptions = {
        ObfuscationType.PYTHON: "Python source code obfuscation and protection",
        ObfuscationType.JAVASCRIPT: "JavaScript/TypeScript code obfuscation",
        ObfuscationType.JAVA: "Java bytecode and JAR file obfuscation",
        ObfuscationType.BINARY: "Binary executable obfuscation and encryption",
        ObfuscationType.NETWORK: "Network protocol and TLS fingerprint obfuscation",
        ObfuscationType.SHELLCODE: "Shellcode encryption and evasion techniques",
    }
    return descriptions.get(obf_type, "Unknown obfuscation type")


async def log_tool_build(tool_id: str, success: bool):
    """Background task to log tool builds"""
    import logging

    logger = logging.getLogger(__name__)
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Vanguard Tool Build - Tool: {tool_id}, Status: {status}")


async def log_obfuscation(tool: str, filename: str, success: bool):
    """Background task to log obfuscation operations"""
    import logging

    logger = logging.getLogger(__name__)
    status = "SUCCESS" if success else "FAILED"
    logger.info(
        f"Vanguard Obfuscation - Tool: {tool}, File: {filename}, Status: {status}"
    )


async def cleanup_temp_file(file_path: str):
    """Background task to cleanup temporary files"""
    try:
        Path(file_path).unlink()
    except:
        pass


# Include health check at router level
@router.get("/")
async def vanguard_root():
    """Vanguard service root endpoint"""
    return {
        "service": "Vanguard",
        "description": "Obfuscation and Security Tools for LANCELOTT Framework",
        "version": "1.0.0",
        "features": [
            "Multi-Language Obfuscation",
            "Binary Protection",
            "Network Protocol Obfuscation",
            "Shellcode Encryption",
            "Automated Tool Selection",
            "File Upload Support",
        ],
        "endpoints": [
            "/health",
            "/tools",
            "/tools/{tool_id}",
            "/tools/{tool_id}/build",
            "/obfuscate",
            "/upload-and-obfuscate",
            "/recommendations",
            "/status",
            "/types",
        ],
        "timestamp": datetime.utcnow().isoformat(),
    }
