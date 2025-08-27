"""
SHERLOCK API Router
Hunt down social media accounts by username across social networks
"""

import asyncio
import json
from asyncio import subprocess as asyncio_subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel

from fastapi import APIRouter, BackgroundTasks, HTTPException

router = APIRouter()


class SherlockSearchRequest(BaseModel):
    username: str
    sites: Optional[List[str]] = None  # Specific sites to search, None for all
    timeout: int = 60
    proxy: Optional[str] = None
    options: Dict[str, Any] = {}


class SherlockSearchResponse(BaseModel):
    search_id: str
    status: str
    username: str
    started_at: datetime
    results: Optional[Dict[str, Any]] = None


# In-memory storage for search results
search_results: Dict[str, Dict[str, Any]] = {}


@router.get("/", summary="Get Sherlock information")
async def get_sherlock_info():
    """Get information about the Sherlock tool"""
    return {
        "name": "Sherlock",
        "version": "1.14.0",
        "description": "Hunt down social media accounts by username across social networks",
        "supported_sites": "400+ social media platforms",
        "endpoints": [
            "/search - Start a username search",
            "/search/{search_id} - Get search results",
            "/searches - List all searches",
            "/sites - Get list of supported sites",
        ],
        "features": [
            "Social media username enumeration",
            "Real-time availability checking",
            "Customizable site selection",
            "JSON and CSV output formats",
            "Proxy support",
            "False positive detection",
        ],
    }


@router.get("/sites", summary="Get supported sites")
async def get_supported_sites():
    """Get list of supported social media sites"""
    try:
        # Read the sites data from Sherlock's data.json
        with open("/app/SHERLOCK/sherlock_project/resources/data.json", "r") as f:
            sites_data = json.load(f)

        sites_list = []
        for site_name, site_info in sites_data.items():
            sites_list.append(
                {
                    "name": site_name,
                    "url": site_info.get("urlMain", ""),
                    "category": site_info.get("tags", []),
                    "status": "active",
                }
            )

        return {"total_sites": len(sites_list), "sites": sites_list}
    except Exception as e:
        return {
            "total_sites": 0,
            "sites": [],
            "error": f"Could not load sites data: {str(e)}",
        }


@router.post(
    "/search", response_model=SherlockSearchResponse, summary="Start username search"
)
async def start_sherlock_search(
    request: SherlockSearchRequest, background_tasks: BackgroundTasks
):
    """Start a new Sherlock username search"""
    search_id = str(uuid4())

    # Initialize search result
    search_results[search_id] = {
        "search_id": search_id,
        "status": "started",
        "username": request.username,
        "started_at": datetime.now(),
        "results": None,
    }

    # Start background search
    background_tasks.add_task(run_sherlock_search, search_id, request)

    return SherlockSearchResponse(
        search_id=search_id,
        status="started",
        username=request.username,
        started_at=datetime.now(),
    )


@router.get(
    "/search/{search_id}",
    response_model=SherlockSearchResponse,
    summary="Get search results",
)
async def get_search_results(search_id: str):
    """Get results for a specific search"""
    if search_id not in search_results:
        raise HTTPException(status_code=404, detail="Search not found")

    result = search_results[search_id]
    return SherlockSearchResponse(**result)


@router.get("/searches", summary="List all searches")
async def list_searches():
    """List all Sherlock searches"""
    return {"searches": list(search_results.values()), "total": len(search_results)}


async def run_sherlock_search(search_id: str, request: SherlockSearchRequest):
    """Run Sherlock search in background"""
    try:
        search_results[search_id]["status"] = "running"

        # Build sherlock command
        cmd = [
            "python",
            "-m",
            "sherlock_project",
            request.username,
            "--json",
            f"/tmp/sherlock_{search_id}.json",
            "--timeout",
            str(request.timeout),
        ]

        # Add specific sites if provided
        if request.sites:
            for site in request.sites:
                cmd.extend(["--site", site])

        # Add proxy if provided
        if request.proxy:
            cmd.extend(["--proxy", request.proxy])

        # Add additional options
        for key, value in request.options.items():
            if key == "print_all":
                cmd.append("--print-all")
            elif key == "print_found":
                cmd.append("--print-found")
            elif key == "no_color":
                cmd.append("--no-color")
            elif key == "browse":
                cmd.append("--browse")

        # Run the search
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio_subprocess.PIPE,
            stderr=asyncio_subprocess.PIPE,
            cwd="/app/SHERLOCK",
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            # Try to read JSON results
            try:
                with open(f"/tmp/sherlock_{search_id}.json", "r") as f:
                    json_results = json.load(f)

                # Parse results
                results = {
                    "found_accounts": [],
                    "total_sites_checked": 0,
                    "found_count": 0,
                    "raw_output": stdout.decode(),
                }

                for username, user_data in json_results.items():
                    results["total_sites_checked"] = len(user_data)
                    for site, site_data in user_data.items():
                        if site_data.get("status") == "Claimed":
                            results["found_accounts"].append(
                                {
                                    "site": site,
                                    "url": site_data.get("url_user", ""),
                                    "status": site_data.get("status", ""),
                                    "response_time": site_data.get(
                                        "response_time_s", 0
                                    ),
                                }
                            )

                results["found_count"] = len(results["found_accounts"])

                search_results[search_id].update(
                    {
                        "status": "completed",
                        "results": results,
                        "completed_at": datetime.now(),
                    }
                )

                # Cleanup temp file
                import os

                try:
                    os.remove(f"/tmp/sherlock_{search_id}.json")
                except:
                    pass

            except Exception as e:
                # Fallback to raw output
                search_results[search_id].update(
                    {
                        "status": "completed",
                        "results": {
                            "raw_output": stdout.decode(),
                            "found_accounts": [],
                            "error": f"JSON parsing failed: {str(e)}",
                        },
                        "completed_at": datetime.now(),
                    }
                )
        else:
            search_results[search_id].update(
                {
                    "status": "failed",
                    "error": stderr.decode(),
                    "completed_at": datetime.now(),
                }
            )

    except Exception as e:
        search_results[search_id].update(
            {"status": "failed", "error": str(e), "completed_at": datetime.now()}
        )
