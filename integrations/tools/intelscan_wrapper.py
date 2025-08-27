#!/usr/bin/env python3
"""
Intel-Scan Tool Integration Wrapper
Intelligence Gathering and Reconnaissance Tool
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.base_tool_wrapper import BaseToolWrapper


class IntelScanWrapper(BaseToolWrapper):
    """Wrapper for Intel-Scan intelligence gathering tool"""

    def __init__(self):
        super().__init__(
            name="Intel-Scan",
            executable_path="tools/Intel-Scan/intelscan_cli.py",
            config_file="config/intelscan.conf",
            description="Intelligence Gathering and Reconnaissance Tool",
            category="OSINT",
            port=7020,
        )
        self.logger = logging.getLogger(__name__)

    async def execute_scan(
        self, target: str, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute Intel-Scan intelligence gathering"""
        if options is None:
            options = {}

        try:
            # Build command
            cmd = ["python3", "intelscan_cli.py"]

            # Add target
            cmd.extend(["--target", target])

            # Add scan type
            scan_type = options.get("scan_type", "comprehensive")
            cmd.extend(["--scan-type", scan_type])

            # Add output format
            output_format = options.get("output_format", "json")
            cmd.extend(["--output", output_format])

            # Add wordlist if specified
            if "wordlist" in options:
                cmd.extend(["--wordlist", options["wordlist"]])

            # Add threads
            threads = options.get("threads", 10)
            cmd.extend(["--threads", str(threads)])

            # Add timeout
            timeout = options.get("timeout", 30)
            cmd.extend(["--timeout", str(timeout)])

            # Set working directory
            work_dir = Path(self.executable_path).parent

            # Execute command
            result = await self._execute_command(cmd, work_dir)

            return {
                "success": True,
                "tool": self.name,
                "target": target,
                "scan_type": scan_type,
                "threads": threads,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Intel-Scan execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": self.name,
                "target": target,
                "timestamp": self._get_timestamp(),
            }

    async def subdomain_enumeration(
        self, domain: str, options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Perform subdomain enumeration"""
        if options is None:
            options = {}

        try:
            cmd = ["python3", "intelscan_cli.py"]
            cmd.extend(["--target", domain])
            cmd.extend(["--scan-type", "subdomain"])

            # Use custom wordlist if provided
            wordlist = options.get("wordlist", "data/wordlists/common_subdomains.txt")
            cmd.extend(["--wordlist", wordlist])

            # Add DNS servers if specified
            if "dns_servers" in options:
                cmd.extend(["--dns", ",".join(options["dns_servers"])])

            work_dir = Path(self.executable_path).parent
            result = await self._execute_command(cmd, work_dir)

            return {
                "success": True,
                "scan_type": "subdomain_enumeration",
                "domain": domain,
                "wordlist": wordlist,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Subdomain enumeration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def port_discovery(
        self, target: str, port_range: str = "1-1000"
    ) -> Dict[str, Any]:
        """Perform port discovery scan"""
        try:
            cmd = ["python3", "intelscan_cli.py"]
            cmd.extend(["--target", target])
            cmd.extend(["--scan-type", "port"])
            cmd.extend(["--ports", port_range])

            work_dir = Path(self.executable_path).parent
            result = await self._execute_command(cmd, work_dir)

            return {
                "success": True,
                "scan_type": "port_discovery",
                "target": target,
                "port_range": port_range,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Port discovery failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    async def technology_detection(self, target: str) -> Dict[str, Any]:
        """Detect technologies used by target"""
        try:
            cmd = ["python3", "intelscan_cli.py"]
            cmd.extend(["--target", target])
            cmd.extend(["--scan-type", "tech"])

            work_dir = Path(self.executable_path).parent
            result = await self._execute_command(cmd, work_dir)

            return {
                "success": True,
                "scan_type": "technology_detection",
                "target": target,
                "results": result,
                "timestamp": self._get_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Technology detection failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": self._get_timestamp(),
            }

    def parse_results(self, output: str) -> Dict[str, Any]:
        """Parse Intel-Scan output"""
        try:
            # Try to parse JSON output
            if output.strip().startswith("{") or output.strip().startswith("["):
                parsed_data = json.loads(output)
                return {
                    "format": "json",
                    "data": parsed_data,
                    "summary": self._generate_summary(parsed_data),
                }

            # Parse text output
            lines = output.strip().split("\n")
            findings = []

            for line in lines:
                if line.strip() and not line.startswith("#"):
                    findings.append(line.strip())

            return {
                "format": "text",
                "findings": findings,
                "total_findings": len(findings),
                "raw_output": output,
            }

        except Exception as e:
            return {
                "error": f"Failed to parse Intel-Scan output: {e}",
                "raw_output": output,
            }

    def _generate_summary(self, data: Any) -> str:
        """Generate summary from parsed data"""
        try:
            if isinstance(data, dict):
                if "subdomains" in data:
                    return f"Found {len(data['subdomains'])} subdomains"
                elif "ports" in data:
                    open_ports = [p for p in data["ports"] if p.get("status") == "open"]
                    return f"Found {len(open_ports)} open ports out of {len(data['ports'])} scanned"
                elif "technologies" in data:
                    return f"Detected {len(data['technologies'])} technologies"
            elif isinstance(data, list):
                return f"Found {len(data)} items"

            return "Scan completed successfully"
        except:
            return "Results available"

    async def get_scan_types(self) -> List[str]:
        """Get available scan types"""
        return ["comprehensive", "subdomain", "port", "tech", "quick", "deep"]

    async def check_dependencies(self) -> Dict[str, Any]:
        """Check Intel-Scan dependencies"""
        try:
            # Check Python
            python_result = subprocess.run(
                ["python3", "--version"], capture_output=True, text=True
            )

            # Check required packages
            packages_to_check = ["requests", "dnspython", "colorama"]
            package_results = {}

            for package in packages_to_check:
                try:
                    __import__(package)
                    package_results[package] = {"available": True, "version": "unknown"}
                except ImportError:
                    package_results[package] = {"available": False, "version": None}

            # Check wordlist file
            wordlist_path = (
                Path(self.executable_path).parent
                / "data"
                / "wordlists"
                / "common_subdomains.txt"
            )
            wordlist_available = wordlist_path.exists()

            dependencies = {
                "python": {
                    "available": python_result.returncode == 0,
                    "version": (
                        python_result.stdout.strip()
                        if python_result.returncode == 0
                        else None
                    ),
                },
                "packages": package_results,
                "wordlist": {
                    "available": wordlist_available,
                    "path": str(wordlist_path),
                },
            }

            all_available = (
                dependencies["python"]["available"]
                and all(pkg["available"] for pkg in package_results.values())
                and wordlist_available
            )

            return {
                "success": all_available,
                "dependencies": dependencies,
                "message": (
                    "All dependencies available"
                    if all_available
                    else "Missing dependencies"
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
_intelscan_wrapper = None


def get_intelscan_wrapper() -> IntelScanWrapper:
    """Get global Intel-Scan wrapper instance"""
    global _intelscan_wrapper
    if _intelscan_wrapper is None:
        _intelscan_wrapper = IntelScanWrapper()
    return _intelscan_wrapper
