#!/usr/bin/env python3
"""
LANCELOTT - Legacy Entry Point
Redirects to the new enhanced application for backward compatibility
"""

import sys
import warnings
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Show deprecation warning
warnings.warn(
    "main.py is deprecated. Use 'python app.py' or 'python -m uvicorn app:app' instead.",
    DeprecationWarning,
    stacklevel=2,
)

print("🔄 Redirecting to enhanced LANCELOTT application...")
print("💡 For future use, please run: python app.py")
print("🚀 Starting LANCELOTT v2.1.0...\n")

# Import and run the enhanced application
if __name__ == "__main__":
    try:
        import uvicorn

        from app import app
        from config.lancelott_config import get_config

        # Get configuration
        config = get_config()

        # Run the enhanced application
        uvicorn.run(
            "app:app",
            host=config.api.host,
            port=config.api.port,
            reload=config.api.debug,
            workers=1 if config.api.debug else config.api.workers,
            log_level="info",
        )

    except ImportError as e:
        print(f"❌ Failed to import enhanced application: {e}")
        print(
            "🔧 Please ensure all dependencies are installed: pip install -r requirements.txt"
        )
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    logger.info("Starting LANCELOTT API")
    await tool_manager.initialize()
    logger.info("All tools initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down LANCELOTT API")
    await tool_manager.cleanup()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard"""
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
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .header h1 {
                font-size: 3em;
                margin: 0;
                color: #00ff88;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            .header p {
                font-size: 1.2em;
                margin: 10px 0;
                opacity: 0.9;
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
                margin: 0 20px;
                padding: 10px 20px;
                border: 2px solid #00ff88;
                border-radius: 5px;
                transition: all 0.3s ease;
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
                <p>Professional Penetration Testing Suite</p>
                <p>Unified Security Tools API Platform</p>
            </div>

            <div class="tools-grid">
                <div class="tool-card">
                    <h3>🔍 Nmap</h3>
                    <p>Network discovery and security auditing</p>
                </div>
                <div class="tool-card">
                    <h3>👁️ Argus</h3>
                    <p>Network monitoring and flow analysis</p>
                </div>
                <div class="tool-card">
                    <h3>🐙 Kraken</h3>
                    <p>Multi-tool security framework</p>
                </div>
                <div class="tool-card">
                    <h3>🌐 Metabigor</h3>
                    <p>Intelligence gathering and OSINT</p>
                </div>
                <div class="tool-card">
                    <h3>🗺️ Dismap</h3>
                    <p>Asset discovery and mapping</p>
                </div>
                <div class="tool-card">
                    <h3>🔬 Osmedeus</h3>
                    <p>Automated reconnaissance framework</p>
                </div>
                <div class="tool-card">
                    <h3>🕷️ SpiderFoot</h3>
                    <p>Open source intelligence automation</p>
                </div>
                <div class="tool-card">
                    <h3>📱 Social Analyzer</h3>
                    <p>Social media analysis and profiling</p>
                </div>
                <div class="tool-card">
                    <h3>⛈️ Storm Breaker</h3>
                    <p>Social engineering and OSINT tool</p>
                </div>
                <div class="tool-card">
                    <h3>📱 PhoneSploit Pro</h3>
                    <p>Android device exploitation</p>
                </div>
                <div class="tool-card">
                    <h3>⚡ Vajra</h3>
                    <p>User interface testing and automation</p>
                </div>
                <div class="tool-card">
                    <h3>🛠️ RedTeam Toolkit</h3>
                    <p>Comprehensive red team utilities</p>
                </div>
            </div>

            <div class="api-links">
                <a href="/docs">📚 API Documentation</a>
                <a href="/redoc">📖 Alternative Docs</a>
                <a href="/api/v1/health">💓 Health Check</a>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "tools_available": await tool_manager.get_available_tools(),
    }


@app.get("/api/v1/tools", dependencies=[Depends(verify_token)])
async def list_tools():
    """List all available tools and their status"""
    return await tool_manager.get_tool_status()


@app.get("/api/v1/tools/{tool_name}/status", dependencies=[Depends(verify_token)])
async def get_tool_status(tool_name: str):
    """Get status of a specific tool"""
    status = await tool_manager.get_tool_status(tool_name)
    if not status:
        raise HTTPException(status_code=404, detail="Tool not found")
    return status


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
        log_level="info",
    )
