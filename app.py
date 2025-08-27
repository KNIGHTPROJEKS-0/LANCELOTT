#!/usr/bin/env python3
"""
LANCELOTT - Enhanced Application
FastAPI application with unified integration framework
"""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles

# Enhanced framework imports
from api.advanced_routes import router as advanced_router

# Core imports
from api.auth import verify_token
from api.routes import (
    argus_router,
    auth_router,
    cliwrap_router,
    crush_router,
    dismap_router,
    enhanced_nmap_router,
    feroxbuster_router,
    firebase_router,
    hydra_router,
    intelscan_router,
    kraken_router,
    langchain_router,
    langchainjs_router,
    metabigor_router,
    mhddos_router,
    n8n_router,
    nmap_router,
    osmedeus_router,
    phonesploit_router,
    redeye_router,
    redteam_toolkit_router,
    sherlock_router,
    social_analyzer_router,
    spiderfoot_router,
    storm_breaker_router,
    supercompat_router,
    supergateway_router,
    tars_router,
    vajra_router,
    vanguard_router,
    web_check_router,
    webstor_router,
)
from core.config import settings
from core.firebase_config import initialize_firebase
from core.logger_config import setup_logging
from core.tool_manager import ToolManager
from integrations.integration_manager import IntegrationManager
from integrations.n8n_integration import N8nIntegration
from status.status_monitor import StatusMonitor

# Global instances
integration_manager = None
status_monitor = None
n8n_integration = None
tool_manager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan with proper initialization and cleanup"""
    global integration_manager, status_monitor, n8n_integration, tool_manager

    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting LANCELOTT...")

    try:
        # Initialize core managers
        tool_manager = ToolManager()
        integration_manager = IntegrationManager()
        status_monitor = StatusMonitor()
        n8n_integration = N8nIntegration()

        # Initialize Firebase
        firebase_success = initialize_firebase()
        if firebase_success:
            logger.info("✅ Firebase initialized successfully")
        else:
            logger.warning(
                "⚠️ Firebase initialization failed - continuing without Firebase"
            )

        # Initialize tool manager
        await tool_manager.initialize()
        logger.info("✅ Tool manager initialized")

        # Initialize integration manager
        init_results = await integration_manager.initialize_all()
        successful_tools = sum(1 for success in init_results.values() if success)
        total_tools = len(init_results)
        logger.info(
            f"✅ Integration manager initialized: {successful_tools}/{total_tools} tools"
        )

        # Store instances in app state
        app.state.tool_manager = tool_manager
        app.state.integration_manager = integration_manager
        app.state.status_monitor = status_monitor
        app.state.n8n_integration = n8n_integration

        # Start background monitoring
        asyncio.create_task(background_monitoring())

        logger.info("🎯 LANCELOTT startup completed successfully")

        yield

    except Exception as e:
        logger.error(f"❌ Failed to initialize LANCELOTT: {e}")
        sys.exit(1)

    finally:
        # Cleanup
        logger.info("🛑 Shutting down LANCELOTT...")

        if integration_manager:
            await integration_manager.cleanup_all()

        if tool_manager:
            await tool_manager.cleanup()

        logger.info("👋 LANCELOTT shutdown completed")


async def background_monitoring():
    """Background task for continuous monitoring"""
    while True:
        try:
            if status_monitor:
                await status_monitor.check_all_components()
            await asyncio.sleep(30)  # Check every 30 seconds
        except Exception as e:
            logging.getLogger(__name__).error(f"Background monitoring error: {e}")
            await asyncio.sleep(60)  # Wait longer on error


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="LANCELOTT",
    description="Unified Security Tools API - Professional Penetration Testing Suite",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "health", "description": "Health and status monitoring"},
        {"name": "tools", "description": "Security tool management and execution"},
        {"name": "scans", "description": "Scan operations and results"},
        {"name": "integrations", "description": "Tool integrations and management"},
        {"name": "workflows", "description": "n8n workflow automation"},
        {"name": "reports", "description": "Report generation and management"},
        {"name": "admin", "description": "Administrative operations"},
    ],
)

# Setup logging
logger = setup_logging()

# Security
security = HTTPBearer()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include existing routers with enhanced prefixes
app.include_router(nmap_router, prefix="/api/v1/tools/nmap", tags=["tools", "nmap"])
app.include_router(argus_router, prefix="/api/v1/tools/argus", tags=["tools", "argus"])
app.include_router(
    crush_router, prefix="/api/v1/tools/crush", tags=["tools", "crush", "orchestration"]
)
app.include_router(
    cliwrap_router,
    prefix="/api/v1/tools/cliwrap",
    tags=["tools", "cliwrap", "utilities"],
)
app.include_router(
    kraken_router, prefix="/api/v1/tools/kraken", tags=["tools", "kraken"]
)
app.include_router(
    metabigor_router, prefix="/api/v1/tools/metabigor", tags=["tools", "metabigor"]
)
app.include_router(
    dismap_router, prefix="/api/v1/tools/dismap", tags=["tools", "dismap"]
)
app.include_router(
    osmedeus_router, prefix="/api/v1/tools/osmedeus", tags=["tools", "osmedeus"]
)
app.include_router(
    spiderfoot_router, prefix="/api/v1/tools/spiderfoot", tags=["tools", "spiderfoot"]
)
app.include_router(
    social_analyzer_router,
    prefix="/api/v1/tools/social-analyzer",
    tags=["tools", "social-analyzer"],
)
app.include_router(
    storm_breaker_router,
    prefix="/api/v1/tools/storm-breaker",
    tags=["tools", "storm-breaker"],
)
app.include_router(
    phonesploit_router,
    prefix="/api/v1/tools/phonesploit",
    tags=["tools", "phonesploit"],
)
app.include_router(vajra_router, prefix="/api/v1/tools/vajra", tags=["tools", "vajra"])
app.include_router(
    redteam_toolkit_router,
    prefix="/api/v1/tools/redteam-toolkit",
    tags=["tools", "redteam-toolkit"],
)
app.include_router(
    supergateway_router,
    prefix="/api/v1/integrations/supergateway",
    tags=["integrations", "supergateway"],
)
app.include_router(
    supercompat_router,
    prefix="/api/v1/integrations/supercompat",
    tags=["integrations", "supercompat"],
)
app.include_router(
    webstor_router, prefix="/api/v1/tools/webstor", tags=["tools", "webstor"]
)
app.include_router(hydra_router, prefix="/api/v1/tools/hydra", tags=["tools", "hydra"])
app.include_router(
    sherlock_router, prefix="/api/v1/tools/sherlock", tags=["tools", "sherlock"]
)
app.include_router(
    web_check_router, prefix="/api/v1/tools/web-check", tags=["tools", "web-check"]
)
app.include_router(
    vanguard_router, prefix="/api/v1/security/vanguard", tags=["security", "vanguard"]
)
app.include_router(
    n8n_router, prefix="/api/v1/workflows/n8n", tags=["workflows", "n8n"]
)

# New integrated tools
app.include_router(
    redeye_router, prefix="/api/v1/tools/redeye", tags=["tools", "redeye"]
)
app.include_router(
    mhddos_router, prefix="/api/v1/tools/mhddos", tags=["tools", "mhddos"]
)
app.include_router(
    intelscan_router, prefix="/api/v1/tools/intel-scan", tags=["tools", "intel-scan"]
)
app.include_router(
    feroxbuster_router,
    prefix="/api/v1/tools/feroxbuster",
    tags=["tools", "feroxbuster"],
)
app.include_router(
    enhanced_nmap_router,
    prefix="/api/v1/tools/enhanced-nmap",
    tags=["tools", "enhanced-nmap"],
)

# Include LangChain AI framework routers
app.include_router(
    langchain_router,
    prefix="/api/v1/ai/langchain",
    tags=["ai", "langchain", "frameworks"],
)
app.include_router(
    langchainjs_router,
    prefix="/api/v1/ai/langchainjs",
    tags=["ai", "langchainjs", "frameworks"],
)

# Include Firebase integration router
app.include_router(
    firebase_router,
    prefix="/api/v1/firebase",
    tags=["firebase", "authentication", "integrations"],
)

# Include authentication router
app.include_router(
    auth_router,
    prefix="/api/v1",
    tags=["authentication", "users"],
)

# Include advanced API routes
app.include_router(
    advanced_router, prefix="/api/v1/advanced", tags=["advanced", "orchestration"]
)

# Include TARS API routes
app.include_router(tars_router, prefix="/api/v1/tars", tags=["tars", "agent", "ui"])


# Enhanced API endpoints
@app.get("/", response_class=HTMLResponse)
async def root():
    """Enhanced main dashboard"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LANCELOTT</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .header h1 {
                font-size: 3.5em;
                margin: 0;
                color: #00ff88;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            .header p {
                font-size: 1.3em;
                margin: 10px 0;
                opacity: 0.9;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .stat-card {
                background: rgba(0,255,136,0.1);
                border: 2px solid #00ff88;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
            }
            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #00ff88;
            }
            .tools-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }
            .tool-card {
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                transition: transform 0.3s ease;
            }
            .tool-card:hover {
                transform: translateY(-5px);
                border-color: #00ff88;
            }
            .tool-card h3 {
                color: #00ff88;
                margin-top: 0;
            }
            .api-links {
                text-align: center;
                margin: 40px 0;
            }
            .api-links a {
                color: #00ff88;
                text-decoration: none;
                margin: 0 15px;
                padding: 12px 24px;
                border: 2px solid #00ff88;
                border-radius: 5px;
                transition: all 0.3s ease;
                display: inline-block;
            }
            .api-links a:hover {
                background: #00ff88;
                color: #1e3c72;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ LANCELOTT</h1>
                <p>Professional Penetration Testing Suite v2.1</p>
                <p>Unified Security Tools & AI-Enhanced Automation Platform</p>
            </div>

            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">15+</div>
                    <div>Security Tools</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">3</div>
                    <div>AI Integrations</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">∞</div>
                    <div>Workflow Possibilities</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">24/7</div>
                    <div>Monitoring</div>
                </div>
            </div>

            <div class="tools-grid">
                <div class="tool-card">
                    <h3>🔍 Network Reconnaissance</h3>
                    <p>Nmap, Dismap, Osmedeus - Comprehensive network discovery and mapping</p>
                </div>
                <div class="tool-card">
                    <h3>🌐 Web Application Testing</h3>
                    <p>Argus, Kraken, Webstor - Advanced web security assessment</p>
                </div>
                <div class="tool-card">
                    <h3>🕵️ OSINT & Intelligence</h3>
                    <p>Metabigor, SpiderFoot, Social Analyzer - Open source intelligence gathering</p>
                </div>
                <div class="tool-card">
                    <h3>📱 Mobile & IoT Security</h3>
                    <p>PhoneSploit Pro, specialized mobile device exploitation</p>
                </div>
                <div class="tool-card">
                    <h3>⚡ Automated Testing</h3>
                    <p>Vajra, n8n workflows - AI-enhanced automation and orchestration</p>
                </div>
                <div class="tool-card">
                    <h3>🤖 AI Integration</h3>
                    <p>SuperGateway, SuperCompat - Multi-provider AI compatibility layer</p>
                </div>
            </div>

            <div class="api-links">
                <a href="/docs">📚 API Documentation</a>
                <a href="/api/v1/health">💓 System Health</a>
                <a href="/api/v1/status/dashboard">📊 Status Dashboard</a>
                <a href="/api/v1/integrations/status">🔧 Tool Status</a>
                <a href="/api/v1/workflows/n8n">🔄 Workflows</a>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/api/v1/health", tags=["health"])
async def health_check():
    """Enhanced health check endpoint"""
    try:
        system_health = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.1.0",
            "framework": "enhanced",
        }

        if hasattr(app.state, "tool_manager") and app.state.tool_manager:
            system_health["tools_available"] = (
                await app.state.tool_manager.get_available_tools()
            )

        if hasattr(app.state, "integration_manager") and app.state.integration_manager:
            system_health["integrations_status"] = (
                app.state.integration_manager.get_tool_status()
            )

        return system_health

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e),
            },
        )


@app.get("/api/v1/status/dashboard", tags=["health"])
async def status_dashboard():
    """Comprehensive status dashboard"""
    try:
        if not hasattr(app.state, "status_monitor") or not app.state.status_monitor:
            raise HTTPException(status_code=503, detail="Status monitor not available")

        # Get current status
        await app.state.status_monitor.check_all_components()
        report = app.state.status_monitor.generate_status_report("json")

        return report

    except Exception as e:
        logger.error(f"Status dashboard error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/integrations/status", tags=["integrations"])
async def integrations_status():
    """Get status of all tool integrations"""
    try:
        if (
            not hasattr(app.state, "integration_manager")
            or not app.state.integration_manager
        ):
            raise HTTPException(
                status_code=503, detail="Integration manager not available"
            )

        status = app.state.integration_manager.get_tool_status()
        health_results = await app.state.integration_manager.health_check_all()

        # Combine status and health information
        for tool_name in status.keys():
            if tool_name in health_results:
                status[tool_name]["health"] = health_results[tool_name]

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "tools": status,
            "summary": {
                "total": len(status),
                "enabled": sum(1 for t in status.values() if t.get("enabled", False)),
                "initialized": sum(
                    1 for t in status.values() if t.get("initialized", False)
                ),
                "healthy": sum(1 for t in status.values() if t.get("health", False)),
            },
        }

    except Exception as e:
        logger.error(f"Integration status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/integrations/{tool_name}/execute", tags=["integrations"])
async def execute_tool_command(
    tool_name: str,
    command: str,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Execute a command with a specific tool via integration manager"""
    try:
        if (
            not hasattr(app.state, "integration_manager")
            or not app.state.integration_manager
        ):
            raise HTTPException(
                status_code=503, detail="Integration manager not available"
            )

        result = await app.state.integration_manager.execute_tool_command(
            tool_name, command
        )

        # Log the execution
        background_tasks.add_task(
            log_tool_execution, tool_name, command, result.get("success", False)
        )

        return result

    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/workflows/n8n/health", tags=["workflows"])
async def n8n_health():
    """Check n8n workflow system health"""
    try:
        if not hasattr(app.state, "n8n_integration") or not app.state.n8n_integration:
            raise HTTPException(status_code=503, detail="n8n integration not available")

        healthy = await app.state.n8n_integration.check_n8n_health()

        return {
            "healthy": healthy,
            "timestamp": datetime.utcnow().isoformat(),
            "n8n_url": app.state.n8n_integration.n8n_url,
        }

    except Exception as e:
        logger.error(f"n8n health check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/workflows/n8n/setup", tags=["workflows"])
async def setup_n8n_workflows(token: str = Depends(verify_token)):
    """Setup n8n workflows for LANCELOTT"""
    try:
        if not hasattr(app.state, "n8n_integration") or not app.state.n8n_integration:
            raise HTTPException(status_code=503, detail="n8n integration not available")

        results = await app.state.n8n_integration.setup_complete_integration()
        return results

    except Exception as e:
        logger.error(f"n8n setup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/status/report/generate", tags=["health"])
async def generate_status_report(
    format: str = "json", save_to_file: bool = False, token: str = Depends(verify_token)
):
    """Generate and optionally save a comprehensive status report"""
    try:
        if not hasattr(app.state, "status_monitor") or not app.state.status_monitor:
            raise HTTPException(status_code=503, detail="Status monitor not available")

        # Get current status
        await app.state.status_monitor.check_all_components()

        if save_to_file:
            report_path = app.state.status_monitor.save_report(output_format=format)
            return {
                "report_saved": True,
                "file_path": report_path,
                "timestamp": datetime.utcnow().isoformat(),
            }
        else:
            report = app.state.status_monitor.generate_status_report(format)
            return report

    except Exception as e:
        logger.error(f"Report generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def log_tool_execution(tool_name: str, command: str, success: bool):
    """Background task to log tool executions"""
    logger.info(
        f"Tool execution: {tool_name} | Command: {command} | Success: {success}"
    )


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
        log_level="info",
    )
