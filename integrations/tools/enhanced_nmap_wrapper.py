#!/usr/bin/env python3
"""
Enhanced Nmap Tool Integration Wrapper
Advanced Network Discovery and Security Auditing
"""

import asyncio
import json
import logging
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.base_tool_wrapper import BaseToolWrapper


class EnhancedNmapWrapper(BaseToolWrapper):
    """Enhanced wrapper for Nmap network scanner"""

    def __init__(self):
        super().__init__(
            name="Enhanced-Nmap",
            executable_path="tools/nmap/nmap",
            config_file="config/nmap.conf",
            description="Advanced Network Discovery and Security Auditing Tool",
            category="Network Security",
            port=7022,
        )
        self.logger = logging.getLogger(__name__)

    async def execute_scan(
        self, target: str, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute enhanced Nmap scan"""
        if options is None:
            options = {}

        try:
            # Build command
            cmd = [str(self.executable_path)]

            # Add scan type
            scan_type = options.get("scan_type", "syn")
            if scan_type == "syn":
                cmd.append("-sS")
            elif scan_type == "tcp":
                cmd.append("-sT")
            elif scan_type == "udp":
                cmd.append("-sU")
            elif scan_type == "stealth":
                cmd.extend(["-sS", "-T2"])
            elif scan_type == "aggressive":
                cmd.extend(["-A", "-T4"])

            # Add port specification
            ports = options.get("ports", "1-1000")
            cmd.extend(["-p", ports])

            # Add timing template
            timing = options.get("timing", "normal")
            timing_map = {
                "paranoid": "-T0",
                "sneaky": "-T1",
                "polite": "-T2",
                "normal": "-T3",
                "aggressive": "-T4",
                "insane": "-T5",
            }
            if timing in timing_map:
                cmd.append(timing_map[timing])

            # Add version detection
            if options.get("version_detection", True):
                cmd.append("-sV")

            # Add OS detection
            if options.get("os_detection", False):
                cmd.append("-O")

            # Add script scanning
            scripts = options.get("scripts", [])
            if scripts:
                if isinstance(scripts, list):
                    cmd.extend(["--script", ",".join(scripts)])
                else:
                    cmd.extend(["--script", scripts])

            # Add default scripts for comprehensive scan
            if options.get("default_scripts", False):
                cmd.append("-sC")

            # Add output format
            output_file = f"/tmp/nmap_scan_{self._get_timestamp().replace(':', '-')}"
            cmd.extend(["-oX", f"{output_file}.xml"])
            cmd.extend(["-oN", f"{output_file}.txt"])

            # Add verbosity
            verbosity = options.get("verbosity", 1)
            cmd.extend(["-v"] * verbosity)

            # Add target
            cmd.append(target)

            # Execute command
            result = await self._execute_command(cmd, timeout=600)

            # Parse XML output
            xml_data = await self._parse_xml_output(f"{output_file}.xml")

            return {
                "success": True,
                "tool": self.name,
                "target": target,
                "scan_type": scan_type,
                "ports": ports,
                "timing": timing,
                "xml_results": xml_data,
                "raw_output": result,
                "output_files": {
                    "xml": f"{output_file}.xml",
                    "text": f"{output_file}.txt",
                },
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Enhanced Nmap execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": self.name,
                "target": target,
                "timestamp": self._get_timestamp(),
            }

    async def vulnerability_scan(
        self, target: str, vuln_categories: List[str] = None
    ) -> Dict[str, Any]:
        """Perform vulnerability scanning with NSE scripts"""
        try:
            if vuln_categories is None:
                vuln_categories = ["vuln", "safe"]

            cmd = [str(self.executable_path)]
            cmd.extend(["-sV", "-sC"])
            cmd.extend(["--script", "vuln"])
            cmd.extend(["-p", "1-65535"])
            cmd.extend(["-T4"])
            cmd.append(target)

            result = await self._execute_command(cmd, timeout=1200)

            return {
                "success": True,
                "scan_type": "vulnerability_scan",
                "target": target,
                "categories": vuln_categories,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Vulnerability scan failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def service_enumeration(
        self, target: str, ports: str = "1-10000"
    ) -> Dict[str, Any]:
        """Perform detailed service enumeration"""
        try:
            cmd = [str(self.executable_path)]
            cmd.extend(["-sV", "-sS"])
            cmd.extend(["-p", ports])
            cmd.extend(["--version-intensity", "9"])
            cmd.extend(["--script", "banner,default"])
            cmd.extend(["-T4"])
            cmd.append(target)

            result = await self._execute_command(cmd, timeout=900)

            return {
                "success": True,
                "scan_type": "service_enumeration",
                "target": target,
                "ports": ports,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Service enumeration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def stealth_scan(
        self, target: str, ports: str = "80,443,22,21,25,53,110,995,993,143"
    ) -> Dict[str, Any]:
        """Perform stealth scan to avoid detection"""
        try:
            cmd = [str(self.executable_path)]
            cmd.extend(["-sS", "-f", "-f"])  # Fragment packets
            cmd.extend(["-D", "RND:10"])  # Decoy scan
            cmd.extend(["-p", ports])
            cmd.extend(["-T1"])  # Slowest timing
            cmd.extend(["--randomize-hosts"])
            cmd.append(target)

            result = await self._execute_command(cmd, timeout=1800)

            return {
                "success": True,
                "scan_type": "stealth_scan",
                "target": target,
                "ports": ports,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Stealth scan failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def _parse_xml_output(self, xml_file: str) -> Dict[str, Any]:
        """Parse Nmap XML output"""
        try:
            xml_path = Path(xml_file)
            if not xml_path.exists():
                return {}

            tree = ET.parse(xml_file)
            root = tree.getroot()

            scan_info = {
                "scanner": root.get("scanner", "nmap"),
                "version": root.get("version", "unknown"),
                "start_time": root.get("start", "unknown"),
                "hosts": [],
            }

            for host in root.findall("host"):
                host_info = {
                    "status": (
                        host.find("status").get("state")
                        if host.find("status") is not None
                        else "unknown"
                    ),
                    "addresses": [],
                    "hostnames": [],
                    "ports": [],
                    "os": {},
                }

                # Extract addresses
                for address in host.findall("address"):
                    host_info["addresses"].append(
                        {"addr": address.get("addr"), "type": address.get("addrtype")}
                    )

                # Extract hostnames
                hostnames = host.find("hostnames")
                if hostnames is not None:
                    for hostname in hostnames.findall("hostname"):
                        host_info["hostnames"].append(
                            {"name": hostname.get("name"), "type": hostname.get("type")}
                        )

                # Extract ports
                ports = host.find("ports")
                if ports is not None:
                    for port in ports.findall("port"):
                        port_info = {
                            "protocol": port.get("protocol"),
                            "port_id": port.get("portid"),
                            "state": (
                                port.find("state").get("state")
                                if port.find("state") is not None
                                else "unknown"
                            ),
                        }

                        # Service information
                        service = port.find("service")
                        if service is not None:
                            port_info["service"] = {
                                "name": service.get("name"),
                                "product": service.get("product"),
                                "version": service.get("version"),
                                "extrainfo": service.get("extrainfo"),
                            }

                        host_info["ports"].append(port_info)

                # Extract OS information
                os_elem = host.find("os")
                if os_elem is not None:
                    osmatch = os_elem.find("osmatch")
                    if osmatch is not None:
                        host_info["os"] = {
                            "name": osmatch.get("name"),
                            "accuracy": osmatch.get("accuracy"),
                        }

                scan_info["hosts"].append(host_info)

            return scan_info

        except Exception as e:
            self.logger.warning(f"Failed to parse XML output: {e}")
            return {}

    def parse_results(self, output: str) -> Dict[str, Any]:
        """Parse Nmap text output"""
        try:
            lines = output.strip().split("\n")
            hosts = []
            current_host = None

            for line in lines:
                line = line.strip()

                # Host information
                if "Nmap scan report for" in line:
                    if current_host:
                        hosts.append(current_host)
                    current_host = {
                        "host": line.split("for ")[-1],
                        "ports": [],
                        "status": "up",
                    }

                # Port information
                elif "/" in line and (
                    "open" in line or "closed" in line or "filtered" in line
                ):
                    if current_host:
                        parts = line.split()
                        if len(parts) >= 3:
                            port_info = parts[0]
                            state = parts[1]
                            service = parts[2] if len(parts) > 2 else "unknown"

                            current_host["ports"].append(
                                {"port": port_info, "state": state, "service": service}
                            )

            if current_host:
                hosts.append(current_host)

            return {"hosts": hosts, "total_hosts": len(hosts), "raw_output": output}

        except Exception as e:
            return {"error": f"Failed to parse Nmap output: {e}", "raw_output": output}

    async def check_dependencies(self) -> Dict[str, Any]:
        """Check enhanced Nmap dependencies"""
        try:
            # Check if nmap binary exists
            binary_exists = Path(self.executable_path).exists()

            # Check nmap version
            version_result = subprocess.run(
                [str(self.executable_path), "--version"], capture_output=True, text=True
            )

            # Check for NSE scripts
            nse_path = Path(self.executable_path).parent / "scripts"
            nse_available = nse_path.exists()

            dependencies = {
                "binary": {
                    "available": binary_exists,
                    "path": str(self.executable_path),
                },
                "version": {
                    "available": version_result.returncode == 0,
                    "info": (
                        version_result.stdout.strip()
                        if version_result.returncode == 0
                        else None
                    ),
                },
                "nse_scripts": {"available": nse_available, "path": str(nse_path)},
            }

            all_available = binary_exists and version_result.returncode == 0

            return {
                "success": all_available,
                "dependencies": dependencies,
                "enhanced_features": nse_available,
                "message": (
                    "All dependencies available"
                    if all_available
                    else "Dependencies missing"
                ),
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }


# Global wrapper instance
_enhanced_nmap_wrapper = None


def get_enhanced_nmap_wrapper() -> EnhancedNmapWrapper:
    """Get global enhanced Nmap wrapper instance"""
    global _enhanced_nmap_wrapper
    if _enhanced_nmap_wrapper is None:
        _enhanced_nmap_wrapper = EnhancedNmapWrapper()
    return _enhanced_nmap_wrapper
