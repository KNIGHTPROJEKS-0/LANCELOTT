"""
Configuration settings for LANCELOTT
Integrated with unified configuration system
"""

import os
from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore", case_sensitive=True)
    """Application settings - Legacy compatibility layer"""

    # Application
    APP_NAME: str = "LANCELOTT"
    VERSION: str = "2.1.0"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 7777

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TOOLS_DIR: str = os.path.join(
        BASE_DIR, "tools"
    )  # Updated to use new tools directory
    REPORTS_DIR: str = os.path.join(BASE_DIR, "reports")
    LOGS_DIR: str = os.path.join(BASE_DIR, "logs")
    STATIC_DIR: str = os.path.join(BASE_DIR, "static")

    # Updated Tool Paths - Now using tools/ directory
    NMAP_PATH: str = os.path.join(BASE_DIR, "nmap")  # Nmap stays in root
    ARGUS_PATH: str = os.path.join(TOOLS_DIR, "Argus")
    KRAKEN_PATH: str = os.path.join(TOOLS_DIR, "Kraken")
    METABIGOR_PATH: str = os.path.join(TOOLS_DIR, "Metabigor")
    DISMAP_PATH: str = os.path.join(TOOLS_DIR, "dismap")
    OSMEDEUS_PATH: str = os.path.join(TOOLS_DIR, "Osmedeus")
    SPIDERFOOT_PATH: str = os.path.join(TOOLS_DIR, "Spiderfoot")
    SOCIAL_ANALYZER_PATH: str = os.path.join(TOOLS_DIR, "Social-Analyzer")
    STORM_BREAKER_PATH: str = os.path.join(TOOLS_DIR, "Storm-Breaker")
    PHONESPLOIT_PATH: str = os.path.join(TOOLS_DIR, "PhoneSploit-Pro")
    VAJRA_PATH: str = os.path.join(TOOLS_DIR, "Vajra")
    REDTEAM_TOOLKIT_PATH: str = os.path.join(TOOLS_DIR, "RedTeam-ToolKit")
    UI_TARS_PATH: str = os.path.join(TOOLS_DIR, "UI-TARS")
    WEBSTOR_PATH: str = os.path.join(TOOLS_DIR, "Webstor")
    SHERLOCK_PATH: str = os.path.join(TOOLS_DIR, "SHERLOCK")
    WEB_CHECK_PATH: str = os.path.join(TOOLS_DIR, "Web-Check")
    HYDRA_PATH: str = os.path.join(TOOLS_DIR, "THC-Hydra")

    # Framework integration paths (outside tools directory)
    SUPERGATEWAY_PATH: str = os.path.join(BASE_DIR, "SuperGateway")
    SUPERCOMPAT_PATH: str = os.path.join(BASE_DIR, "SuperCompat")
    VANGUARD_PATH: str = os.path.join(BASE_DIR, "Vanguard")

    # Vanguard Paths
    VANGUARD_BOAZ_PATH: str = os.path.join(VANGUARD_PATH, "BOAZ")
    VANGUARD_FAKEHTTP_PATH: str = os.path.join(VANGUARD_PATH, "FakeHTTP")
    VANGUARD_DE4PY_PATH: str = os.path.join(VANGUARD_PATH, "de4py")
    VANGUARD_PYARMOR_PATH: str = os.path.join(VANGUARD_PATH, "pyarmor")
    VANGUARD_UTLS_PATH: str = os.path.join(VANGUARD_PATH, "utls")
    VANGUARD_JS_OBFUSCATOR_PATH: str = os.path.join(
        VANGUARD_PATH, "javascript-obfuscator"
    )
    VANGUARD_SKIDFUSCATOR_PATH: str = os.path.join(
        VANGUARD_PATH, "skidfuscator-java-obfuscator"
    )

    # Database (if needed)
    DATABASE_URL: str = "sqlite:///./cerberus_fangs.db"

    # Redis (if needed)
    REDIS_URL: str = "redis://localhost:6379"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # File Upload
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")

    # Scan Settings
    MAX_CONCURRENT_SCANS: int = 5
    SCAN_TIMEOUT: int = 3600  # 1 hour


# Create legacy settings instance
settings = Settings()


def get_unified_config():
    """Get the new unified configuration system"""
    try:
        from config.lancelott_config import get_config

        return get_config()
    except ImportError:
        # Fallback to legacy settings
        return None


def get_enhanced_settings():
    """Get enhanced settings that merge legacy and unified configs"""
    unified_config = get_unified_config()

    if unified_config:
        # Update legacy settings with unified config values
        settings.HOST = unified_config.api.host
        settings.PORT = unified_config.api.port
        settings.DEBUG = unified_config.api.debug
        settings.SECRET_KEY = unified_config.security.jwt_secret

    return settings


# Ensure required directories exist
from pathlib import Path

for directory in [
    settings.REPORTS_DIR,
    settings.LOGS_DIR,
    settings.STATIC_DIR,
    settings.TOOLS_DIR,
]:
    Path(directory).mkdir(parents=True, exist_ok=True)
