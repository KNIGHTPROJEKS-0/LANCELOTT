"""
Pydantic models for CERBERUS-FANGS LANCELOTT API
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class ScanType(str, Enum):
    """Types of scans available"""
    NETWORK_SCAN = "network_scan"
    PORT_SCAN = "port_scan"
    VULNERABILITY_SCAN = "vulnerability_scan"
    OSINT_SCAN = "osint_scan"
    SOCIAL_SCAN = "social_scan"
    WEB_SCAN = "web_scan"
    MOBILE_SCAN = "mobile_scan"


class ToolStatus(str, Enum):
    """Tool status enumeration"""
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    RUNNING = "running"
    ERROR = "error"


class ScanStatus(str, Enum):
    """Scan status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BaseRequest(BaseModel):
    """Base request model"""
    model_config = ConfigDict(extra="forbid")


class BaseResponse(BaseModel):
    """Base response model"""
    success: bool
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Nmap Models
class NmapScanRequest(BaseRequest):
    """Nmap scan request model"""
    target: str = Field(..., description="Target IP address, hostname, or CIDR range")
    scan_type: str = Field(default="basic", description="Type of scan (basic, stealth, comprehensive)")
    ports: Optional[str] = Field(None, description="Port range to scan (e.g., '80,443,8080' or '1-1000')")
    output_format: str = Field(default="xml", description="Output format (xml, json, grepable)")
    timing: Optional[str] = Field(None, description="Timing template (T0-T5)")
    additional_flags: Optional[List[str]] = Field(default=[], description="Additional nmap flags")


# Argus Models
class ArgusMonitorRequest(BaseRequest):
    """Argus monitoring request model"""
    interface: str = Field(..., description="Network interface to monitor")
    duration: Optional[int] = Field(3600, description="Monitoring duration in seconds")
    filter_expression: Optional[str] = Field(None, description="BPF filter expression")
    output_file: Optional[str] = Field(None, description="Output file path")


# Kraken Models
class KrakenScanRequest(BaseRequest):
    """Kraken scan request model"""
    target: str = Field(..., description="Target URL or IP address")
    scan_modules: List[str] = Field(default=[], description="Modules to use for scanning")
    depth: Optional[int] = Field(1, description="Scan depth")
    threads: Optional[int] = Field(10, description="Number of threads")


# Metabigor Models
class MetabigorRequest(BaseRequest):
    """Metabigor OSINT request model"""
    target: str = Field(..., description="Target domain, IP, or organization")
    modules: List[str] = Field(default=[], description="OSINT modules to use")
    passive_only: bool = Field(True, description="Use only passive techniques")
    output_format: str = Field(default="json", description="Output format")


# Dismap Models
class DismapScanRequest(BaseRequest):
    """Dismap asset discovery request model"""
    target: str = Field(..., description="Target IP range or domain")
    threads: Optional[int] = Field(100, description="Number of threads")
    timeout: Optional[int] = Field(10, description="Request timeout in seconds")
    output_file: Optional[str] = Field(None, description="Output file path")


# SpiderFoot Models
class SpiderFootScanRequest(BaseRequest):
    """SpiderFoot OSINT scan request model"""
    target: str = Field(..., description="Target domain, IP, or entity")
    modules: List[str] = Field(default=[], description="SpiderFoot modules to use")
    scan_name: Optional[str] = Field(None, description="Custom scan name")


# Social Analyzer Models
class SocialAnalyzerRequest(BaseRequest):
    """Social Analyzer request model"""
    username: str = Field(..., description="Username to analyze")
    websites: List[str] = Field(default=[], description="Specific websites to check")
    mode: str = Field(default="fast", description="Analysis mode (fast, normal, slow)")


# Storm Breaker Models
class StormBreakerRequest(BaseRequest):
    """Storm Breaker social engineering request model"""
    target_info: Dict[str, Any] = Field(..., description="Target information")
    attack_type: str = Field(..., description="Type of social engineering attack")
    template: Optional[str] = Field(None, description="Template to use")


# PhoneSploit Models
class PhoneSploitRequest(BaseRequest):
    """PhoneSploit request model"""
    device_ip: str = Field(..., description="Target Android device IP address")
    command: str = Field(..., description="Command to execute")
    port: Optional[int] = Field(5555, description="ADB port")


# Generic Scan Request
class ScanRequest(BaseRequest):
    """Generic scan request model"""
    tool: str = Field(..., description="Tool to use for scanning")
    target: str = Field(..., description="Target to scan")
    scan_type: ScanType = Field(..., description="Type of scan to perform")
    options: Dict[str, Any] = Field(default={}, description="Tool-specific options")
    priority: Optional[int] = Field(1, description="Scan priority (1-5, 5 being highest)")
    timeout: Optional[int] = Field(3600, description="Scan timeout in seconds")


# Response Models
class ScanResult(BaseModel):
    """Scan result model"""
    scan_id: str
    tool: str
    target: str
    status: ScanStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration: Optional[float] = None
    results: Dict[str, Any] = Field(default={})
    error_message: Optional[str] = None
    output_files: List[str] = Field(default=[])


class ToolInfo(BaseModel):
    """Tool information model"""
    name: str
    status: ToolStatus
    description: str
    category: str
    version: Optional[str] = None
    last_checked: datetime
    capabilities: List[str] = Field(default=[])


class HealthCheck(BaseResponse):
    """Health check response model"""
    version: str
    uptime: float
    tools_available: List[str]
    active_scans: int


class ScanListResponse(BaseResponse):
    """Scan list response model"""
    scans: List[ScanResult]
    total: int
    page: int
    per_page: int


class ProcessInfo(BaseModel):
    """Process information model"""
    process_id: str
    tool: str
    target: str
    status: str
    started_at: datetime
    progress: Optional[float] = None


# File Upload Models
class FileUpload(BaseModel):
    """File upload model"""
    filename: str
    content_type: str
    size: int
    upload_path: str
    uploaded_at: datetime


# Report Models
class ReportRequest(BaseRequest):
    """Report generation request model"""
    scan_ids: List[str] = Field(..., description="Scan IDs to include in report")
    report_format: str = Field(default="html", description="Report format (html, pdf, json)")
    include_raw_data: bool = Field(False, description="Include raw scan data")
    template: Optional[str] = Field(None, description="Report template to use")


class ReportInfo(BaseModel):
    """Report information model"""
    report_id: str
    title: str
    format: str
    created_at: datetime
    file_path: str
    size: int
    scan_count: int


# Authentication Models
class TokenRequest(BaseRequest):
    """Token request model"""
    username: str
    password: str


class TokenResponse(BaseResponse):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# WebSocket Models
class WebSocketMessage(BaseModel):
    """WebSocket message model"""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ScanProgress(BaseModel):
    """Scan progress model"""
    scan_id: str
    progress: float  # 0.0 to 1.0
    stage: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
