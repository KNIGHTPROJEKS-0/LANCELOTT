#!/usr/bin/env python3
"""
Metabigor Integration for CERBERUS-FANGS LANCELOTT
Provides OSINT and intelligence gathering capabilities
"""

import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


class MetabigorWrapper:
    def __init__(self, metabigor_path: Optional[str] = None):
        """Initialize Metabigor wrapper"""
        if metabigor_path is None:
            # Auto-detect metabigor path
            current_dir = Path(__file__).parent
            self.metabigor_path = current_dir / "Metabigor" / "metabigor"
        else:
            self.metabigor_path = Path(metabigor_path)
        self.logger = logging.getLogger(__name__)

        if not self.metabigor_path.exists():
            raise FileNotFoundError(
                f"Metabigor binary not found at {self.metabigor_path}"
            )

    def _run_command(self, cmd: List[str], timeout: int = 300) -> Dict[str, Any]:
        """Run metabigor command and return results"""
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "returncode": -1,
            }
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1}

    def ip_intelligence(
        self, target: str, output_format: str = "json"
    ) -> Dict[str, Any]:
        """Gather IP intelligence using Metabigor"""
        cmd = [str(self.metabigor_path), "ip", "--target", target]
        if output_format == "json":
            cmd.extend(["--json"])

        result = self._run_command(cmd)

        if result["success"] and output_format == "json":
            try:
                result["data"] = json.loads(result["stdout"])
            except json.JSONDecodeError:
                result["data"] = {"raw_output": result["stdout"]}

        return result

    def cert_intelligence(
        self, target: str, output_format: str = "json"
    ) -> Dict[str, Any]:
        """Gather certificate intelligence"""
        cmd = [str(self.metabigor_path), "cert", "--target", target]
        if output_format == "json":
            cmd.extend(["--json"])

        result = self._run_command(cmd)

        if result["success"] and output_format == "json":
            try:
                result["data"] = json.loads(result["stdout"])
            except json.JSONDecodeError:
                result["data"] = {"raw_output": result["stdout"]}

        return result

    def net_intelligence(
        self, target: str, output_format: str = "json"
    ) -> Dict[str, Any]:
        """Gather network intelligence"""
        cmd = [str(self.metabigor_path), "net", "--target", target]
        if output_format == "json":
            cmd.extend(["--json"])

        result = self._run_command(cmd)

        if result["success"] and output_format == "json":
            try:
                result["data"] = json.loads(result["stdout"])
            except json.JSONDecodeError:
                result["data"] = {"raw_output": result["stdout"]}

        return result

    def scan_target(
        self,
        target: str,
        scan_type: str = "all",
        output_format: str = "json",
        output_file: Optional[str] = None,
        threads: int = 10,
        verbose: bool = False,
        ports: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Perform network scan using Metabigor"""
        cmd = [str(self.metabigor_path), "scan", "--target", target]

        if scan_type == "full":
            cmd.extend(["--full"])
        elif scan_type == "quick":
            cmd.extend(["--quick"])

        if ports:
            cmd.extend(["--ports", ports])

        cmd.extend(["--json"])

        result = self._run_command(cmd, timeout=600)  # Longer timeout for scans

        if result["success"]:
            try:
                result["data"] = json.loads(result["stdout"])
            except json.JSONDecodeError:
                result["data"] = {"raw_output": result["stdout"]}

        return result

    def related_domains(
        self, target: str, output_format: str = "json"
    ) -> Dict[str, Any]:
        """Find related domains and subdomains"""
        cmd = [str(self.metabigor_path), "related", "--target", target]
        if output_format == "json":
            cmd.extend(["--json"])

        result = self._run_command(cmd)

        if result["success"] and output_format == "json":
            try:
                result["data"] = json.loads(result["stdout"])
            except json.JSONDecodeError:
                result["data"] = {"raw_output": result["stdout"]}

        return result


def main():
    """CLI interface for Metabigor wrapper"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Metabigor Integration for CERBERUS-FANGS"
    )
    parser.add_argument(
        "command",
        choices=["ip", "cert", "net", "scan", "related"],
        help="Command to execute",
    )
    parser.add_argument("--target", required=True, help="Target to analyze")
    parser.add_argument(
        "--scan-type",
        choices=["quick", "full"],
        default="quick",
        help="Scan type for scan command",
    )
    parser.add_argument("--ports", help="Ports to scan (for scan command)")
    parser.add_argument(
        "--output", choices=["json", "text"], default="json", help="Output format"
    )
    parser.add_argument("--metabigor-path", help="Path to metabigor binary")

    args = parser.parse_args()

    try:
        metabigor = MetabigorWrapper(args.metabigor_path)
        result = None

        if args.command == "ip":
            result = metabigor.ip_intelligence(args.target, args.output)
        elif args.command == "cert":
            result = metabigor.cert_intelligence(args.target, args.output)
        elif args.command == "net":
            result = metabigor.net_intelligence(args.target, args.output)
        elif args.command == "scan":
            result = metabigor.scan_target(
                args.target, args.scan_type, ports=args.ports
            )
        elif args.command == "related":
            result = metabigor.related_domains(args.target, args.output)

        if result is not None:
            if args.output == "json":
                print(json.dumps(result, indent=2))
            else:
                print(result["stdout"] if result["success"] else result["stderr"])

            sys.exit(0 if result["success"] else 1)
        else:
            print("Unknown command", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
