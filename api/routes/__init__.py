"""
Route imports for CERBERUS-FANGS LANCELOTT API
"""

from .argus import router as argus_router
from .auth_routes import router as auth_router
from .cliwrap_router import router as cliwrap_router
from .crush_router import router as crush_router
from .dismap import router as dismap_router
from .enhanced_nmap_router import router as enhanced_nmap_router
from .feroxbuster_router import router as feroxbuster_router
from .firebase_routes import router as firebase_router
from .hydra import router as hydra_router
from .intelscan_router import router as intelscan_router
from .kraken import router as kraken_router
from .langchain_router import router as langchain_router
from .langchainjs_router import router as langchainjs_router
from .metabigor import router as metabigor_router
from .mhddos_router import router as mhddos_router
from .n8n_workflows import n8n_router
from .nmap import router as nmap_router
from .osmedeus import router as osmedeus_router
from .phonesploit import router as phonesploit_router
from .redeye_router import router as redeye_router
from .redteam_toolkit import router as redteam_toolkit_router
from .sherlock_router import router as sherlock_router
from .social_analyzer import router as social_analyzer_router
from .spiderfoot import router as spiderfoot_router
from .storm_breaker import router as storm_breaker_router
from .supercompat_router import router as supercompat_router
from .supergateway_router import router as supergateway_router
from .ui_tars_router import router as ui_tars_router
from .vajra import router as vajra_router
from .vanguard_router import router as vanguard_router
from .web_check_router import router as web_check_router
from .webstor import router as webstor_router

__all__ = [
    "nmap_router",
    "argus_router",
    "crush_router",
    "cliwrap_router",
    "kraken_router",
    "metabigor_router",
    "dismap_router",
    "osmedeus_router",
    "spiderfoot_router",
    "social_analyzer_router",
    "storm_breaker_router",
    "phonesploit_router",
    "vajra_router",
    "redteam_toolkit_router",
    "supergateway_router",
    "supercompat_router",
    "webstor_router",
    "hydra_router",
    "vanguard_router",
    "sherlock_router",
    "web_check_router",
    "n8n_router",
    # New integrated tools
    "redeye_router",
    "mhddos_router",
    "intelscan_router",
    "feroxbuster_router",
    "enhanced_nmap_router",
    # AI Framework Routers
    "langchain_router",
    "langchainjs_router",
    # Firebase Integration
    "firebase_router",
    "auth_router",
    # UI & GUI Automation
    "ui_tars_router",
]
