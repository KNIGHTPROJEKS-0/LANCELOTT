#!/usr/bin/env python3
"""
CERBERUS-FANGS Tool Integration Manager
Coordinates Metabigor, Metasploit, and other security tools
"""

import asyncio
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from metabigor_integration import MetabigorWrapper
from metasploit_integration import MetasploitWrapper


@dataclass
class TargetInfo:
    """Target information structure"""

    ip: str
    domain: Optional[str] = None
    ports: Optional[List[int]] = None
    services: Optional[List[str]] = None
    vulnerabilities: Optional[List[str]] = None
    certificates: Optional[Dict[str, Any]] = None


class CerbeusFangsManager:
    """Main integration manager for CERBERUS-FANGS"""

    def __init__(self, workspace: str = "cerberus_fangs"):
        """Initialize the manager"""
        self.workspace = workspace
        self.metabigor = MetabigorWrapper()
        self.metasploit = MetasploitWrapper(workspace=workspace)
        self.targets: Dict[str, TargetInfo] = {}
        self.results_dir = (
            Path("reports") / f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def passive_reconnaissance(self, target: str) -> TargetInfo:
        """Perform passive reconnaissance using Metabigor"""
        print(f"[*] Starting passive reconnaissance for {target}")

        target_info = TargetInfo(
            ip=target if self._is_ip(target) else "",
            domain=target if not self._is_ip(target) else None,
        )

        # IP Intelligence
        if target_info.ip:
            print(f"[+] Gathering IP intelligence for {target_info.ip}")
            ip_result = self.metabigor.ip_intelligence(target_info.ip)
            self._save_result("ip_intelligence", target, ip_result)

        # Certificate Intelligence
        if target_info.domain:
            print(f"[+] Gathering certificate intelligence for {target_info.domain}")
            cert_result = self.metabigor.cert_intelligence(target_info.domain)
            target_info.certificates = cert_result.get("data", {})
            self._save_result("cert_intelligence", target, cert_result)

        # Network Intelligence
        print(f"[+] Gathering network intelligence for {target}")
        net_result = self.metabigor.net_intelligence(target)
        self._save_result("net_intelligence", target, net_result)

        # Related Domains
        if target_info.domain:
            print(f"[+] Finding related domains for {target_info.domain}")
            related_result = self.metabigor.related_domains(target_info.domain)
            self._save_result("related_domains", target, related_result)

        # Store target info
        self.targets[target] = target_info

        return target_info

    def active_reconnaissance(
        self, target: str, ports: str = "1-1000"
    ) -> Dict[str, Any]:
        """Perform active reconnaissance using Metasploit"""
        print(f"[*] Starting active reconnaissance for {target}")

        # Initialize MSF if needed
        db_status = self.metasploit.check_database_status()
        if not db_status["success"]:
            print("[+] Initializing Metasploit database...")
            init_result = self.metasploit.initialize_database()
            if not init_result["success"]:
                print(f"[-] Failed to initialize database: {init_result['stderr']}")
                return {"success": False, "error": "Database initialization failed"}

        # Port scanning
        print(f"[+] Scanning ports {ports} on {target}")
        scan_result = self.metasploit.scan_network(target, ports)
        self._save_result("port_scan", target, scan_result)

        # Update target info with discovered ports
        if target in self.targets:
            # Parse scan results to extract open ports
            if scan_result["success"]:
                # This would need proper parsing of MSF output
                self.targets[target].ports = self._parse_open_ports(
                    scan_result["output"]
                )

        return scan_result

    def vulnerability_assessment(
        self, target: str, service: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search for vulnerabilities and exploits"""
        print(f"[*] Searching for vulnerabilities for {target}")

        search_result = self.metasploit.search_exploits(target, service)
        self._save_result("vulnerability_search", target, search_result)

        # Update target info with vulnerabilities
        if target in self.targets and search_result["success"]:
            exploits = search_result.get("exploits", [])
            self.targets[target].vulnerabilities = [exp["name"] for exp in exploits]

        return search_result

    def comprehensive_scan(
        self, target: str, ports: str = "1-1000", include_brute_force: bool = False
    ) -> Dict[str, Any]:
        """Perform comprehensive scanning combining all tools"""
        print(f"[*] Starting comprehensive scan for {target}")

        results = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "passive_recon": {},
            "active_recon": {},
            "vulnerability_assessment": {},
        }

        try:
            # Passive reconnaissance
            target_info = self.passive_reconnaissance(target)
            results["passive_recon"] = {
                "domain": target_info.domain,
                "ip": target_info.ip,
                "certificates": target_info.certificates,
            }

            # Active reconnaissance
            scan_result = self.active_reconnaissance(target, ports)
            results["active_recon"] = scan_result

            # Vulnerability assessment
            vuln_result = self.vulnerability_assessment(target)
            results["vulnerability_assessment"] = vuln_result

            # Optional brute force testing
            if include_brute_force and target_info.ports:
                print("[+] Performing targeted brute force attacks...")
                brute_results = self._perform_brute_force_attacks(
                    target, target_info.ports
                )
                results["brute_force"] = brute_results

            # Generate summary report
            self._generate_summary_report(target, results)

            print(
                f"[*] Comprehensive scan completed. Results saved to {self.results_dir}"
            )

            return {
                "success": True,
                "results": results,
                "results_dir": str(self.results_dir),
            }

        except Exception as e:
            error_result = {"success": False, "error": str(e)}
            self._save_result("error", target, error_result)
            return error_result

    def _is_ip(self, target: str) -> bool:
        """Check if target is an IP address"""
        import re

        ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
        return bool(re.match(ip_pattern, target))

    def _parse_open_ports(self, scan_output: str) -> List[int]:
        """Parse open ports from scan output"""
        # This would need proper parsing based on MSF output format
        # For now, return empty list
        ports = []
        lines = scan_output.split("\n")
        for line in lines:
            if "open" in line.lower():
                # Extract port numbers (this is simplified)
                import re

                port_match = re.search(r"(\d+)/", line)
                if port_match:
                    ports.append(int(port_match.group(1)))
        return ports

    def _perform_brute_force_attacks(
        self, target: str, ports: List[int]
    ) -> Dict[str, Any]:
        """Perform brute force attacks on discovered services"""
        brute_results = {}

        # Common service mappings
        service_ports = {22: "ssh", 21: "ftp", 23: "telnet", 3306: "mysql", 445: "smb"}

        for port in ports:
            if port in service_ports:
                service = service_ports[port]
                print(f"[+] Attempting brute force on {service} (port {port})")

                result = self.metasploit.brute_force_service(target, service)
                brute_results[f"{service}_{port}"] = result
                self._save_result(f"brute_force_{service}", target, result)

        return brute_results

    def _save_result(self, scan_type: str, target: str, result: Dict[str, Any]):
        """Save scan result to file"""
        filename = f"{scan_type}_{target.replace('.', '_').replace(':', '_')}.json"
        filepath = self.results_dir / filename

        with open(filepath, "w") as f:
            json.dump(result, f, indent=2, default=str)

    def _generate_summary_report(self, target: str, results: Dict[str, Any]):
        """Generate human-readable summary report"""
        report_file = (
            self.results_dir
            / f"summary_{target.replace('.', '_').replace(':', '_')}.md"
        )

        with open(report_file, "w") as f:
            f.write(f"# CERBERUS-FANGS Scan Report for {target}\n\n")
            f.write(f"**Scan Date:** {results['timestamp']}\n\n")

            # Passive Reconnaissance Summary
            f.write("## Passive Reconnaissance\n\n")
            passive = results.get("passive_recon", {})
            if passive.get("domain"):
                f.write(f"- **Domain:** {passive['domain']}\n")
            if passive.get("ip"):
                f.write(f"- **IP Address:** {passive['ip']}\n")

            # Active Reconnaissance Summary
            f.write("\n## Active Reconnaissance\n\n")
            if target in self.targets:
                target_info = self.targets[target]
                if target_info.ports:
                    f.write(
                        f"- **Open Ports:** {', '.join(map(str, target_info.ports))}\n"
                    )
                if target_info.services:
                    f.write(f"- **Services:** {', '.join(target_info.services)}\n")

            # Vulnerability Assessment Summary
            f.write("\n## Vulnerability Assessment\n\n")
            vuln_data = results.get("vulnerability_assessment", {})
            if vuln_data.get("exploits"):
                f.write("### Available Exploits:\n\n")
                for exploit in vuln_data["exploits"][:10]:  # Top 10
                    f.write(
                        f"- **{exploit['name']}** ({exploit.get('rank', 'Unknown')})\n"
                    )
                    f.write(f"  - {exploit.get('description', 'No description')}\n")

            # Recommendations
            f.write("\n## Recommendations\n\n")
            f.write("- Review open ports and disable unnecessary services\n")
            f.write("- Apply security patches for identified vulnerabilities\n")
            f.write("- Implement strong authentication mechanisms\n")
            f.write("- Configure proper firewall rules\n")


def main():
    """CLI interface for CERBERUS-FANGS Manager"""
    import argparse

    parser = argparse.ArgumentParser(
        description="CERBERUS-FANGS Security Testing Framework"
    )
    parser.add_argument(
        "command",
        choices=["passive", "active", "vuln", "comprehensive"],
        help="Scan type to perform",
    )
    parser.add_argument("--target", required=True, help="Target to scan")
    parser.add_argument(
        "--ports", default="1-1000", help="Ports to scan for active reconnaissance"
    )
    parser.add_argument(
        "--workspace", default="cerberus_fangs", help="MSF workspace name"
    )
    parser.add_argument(
        "--brute-force", action="store_true", help="Include brute force attacks"
    )
    parser.add_argument("--service", help="Specific service for vulnerability search")

    args = parser.parse_args()

    try:
        manager = CerbeusFangsManager(args.workspace)
        result = None

        if args.command == "passive":
            target_info = manager.passive_reconnaissance(args.target)
            result = {"success": True, "target_info": target_info.__dict__}
        elif args.command == "active":
            result = manager.active_reconnaissance(args.target, args.ports)
        elif args.command == "vuln":
            result = manager.vulnerability_assessment(args.target, args.service)
        elif args.command == "comprehensive":
            result = manager.comprehensive_scan(
                args.target, args.ports, args.brute_force
            )

        if result:
            print(json.dumps(result, indent=2, default=str))
            sys.exit(0 if result.get("success", False) else 1)
        else:
            print("Command execution failed", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
