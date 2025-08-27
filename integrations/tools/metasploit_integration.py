#!/usr/bin/env python3
"""
Metasploit Framework Integration for CERBERUS-FANGS
Provides Python wrapper for Metasploit Framework operations
"""

import json
import signal
import subprocess
import sys
import time
from pathlib import Path
from threading import Event, Thread
from typing import Any, Dict, List, Optional, Union

import pexpect


class MetasploitWrapper:
    """Python wrapper for Metasploit Framework"""

    def __init__(self, msf_path: Optional[str] = None, workspace: str = "default"):
        """Initialize Metasploit wrapper"""
        if msf_path is None:
            # Auto-detect MSF path
            current_dir = Path(__file__).parent
            self.msf_path = current_dir / "Metasploit-Framework"
        else:
            self.msf_path = Path(msf_path)

        self.workspace = workspace
        self.msfconsole_path = self.msf_path / "msfconsole"
        self.msfdb_path = self.msf_path / "msfdb"
        self.console_session = None

    def _run_command(
        self, cmd: List[str], timeout: int = 60, cwd: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Execute command and return structured result"""
        try:
            if cwd is None:
                cwd = self.msf_path

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout, cwd=str(cwd)
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
                "command": " ".join(cmd),
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "returncode": -1,
                "command": " ".join(cmd),
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "command": " ".join(cmd),
            }

    def initialize_database(self) -> Dict[str, Any]:
        """Initialize Metasploit database"""
        cmd = [str(self.msfdb_path), "init"]
        return self._run_command(cmd, timeout=120)

    def check_database_status(self) -> Dict[str, Any]:
        """Check database connection status"""
        cmd = [str(self.msfdb_path), "status"]
        return self._run_command(cmd)

    def start_console(self, timeout: int = 30) -> bool:
        """Start interactive msfconsole session"""
        try:
            # Start msfconsole with expect
            self.console_session = pexpect.spawn(
                str(self.msfconsole_path), timeout=timeout, cwd=str(self.msf_path)
            )

            # Wait for prompt
            self.console_session.expect(r"msf6?\s*>")

            # Set workspace
            if self.workspace != "default":
                self.console_session.sendline(f"workspace -a {self.workspace}")
                self.console_session.expect(r"msf6?\s*>")

            return True
        except Exception as e:
            print(f"Failed to start console: {e}")
            return False

    def execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute command in msfconsole session"""
        if not self.console_session:
            return {
                "success": False,
                "output": "",
                "error": "Console session not started",
            }

        try:
            self.console_session.sendline(command)
            self.console_session.expect(r"msf6?\s*>", timeout=timeout)

            output = self.console_session.before.decode("utf-8")

            return {"success": True, "output": output.strip(), "error": ""}
        except Exception as e:
            return {"success": False, "output": "", "error": str(e)}

    def close_console(self):
        """Close msfconsole session"""
        if self.console_session:
            try:
                self.console_session.sendline("exit")
                self.console_session.close()
            except:
                pass
            self.console_session = None

    def search_exploits(
        self, target: str, service: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search for exploits targeting specific service or platform"""
        if not self.console_session:
            if not self.start_console():
                return {"success": False, "error": "Failed to start console"}

        search_term = target
        if service:
            search_term = f"{service} {target}"

        result = self.execute_command(f"search {search_term}")

        if result["success"]:
            # Parse search results
            lines = result["output"].split("\n")
            exploits = []

            for line in lines:
                if "exploit/" in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        exploits.append(
                            {
                                "name": parts[0],
                                "disclosure_date": parts[1] if len(parts) > 1 else "",
                                "rank": parts[2] if len(parts) > 2 else "",
                                "description": (
                                    " ".join(parts[3:]) if len(parts) > 3 else ""
                                ),
                            }
                        )

            result["exploits"] = exploits

        return result

    def use_module(self, module_name: str) -> Dict[str, Any]:
        """Load and configure a specific module"""
        if not self.console_session:
            if not self.start_console():
                return {"success": False, "error": "Failed to start console"}

        return self.execute_command(f"use {module_name}")

    def show_options(self) -> Dict[str, Any]:
        """Show current module options"""
        if not self.console_session:
            return {"success": False, "error": "Console session not started"}

        result = self.execute_command("show options")

        if result["success"]:
            # Parse options
            lines = result["output"].split("\n")
            options = []

            for line in lines:
                if "Required" in line and ("yes" in line or "no" in line):
                    parts = line.split()
                    if len(parts) >= 4:
                        options.append(
                            {
                                "name": parts[0],
                                "current_setting": parts[1],
                                "required": parts[2],
                                "description": " ".join(parts[3:]),
                            }
                        )

            result["options"] = options

        return result

    def set_option(self, option: str, value: str) -> Dict[str, Any]:
        """Set module option"""
        if not self.console_session:
            return {"success": False, "error": "Console session not started"}

        return self.execute_command(f"set {option} {value}")

    def run_exploit(self, background: bool = False) -> Dict[str, Any]:
        """Execute loaded exploit"""
        if not self.console_session:
            return {"success": False, "error": "Console session not started"}

        command = "exploit"
        if background:
            command += " -j"  # Run in background

        return self.execute_command(command, timeout=60)

    def scan_network(self, target: str, ports: str = "1-1000") -> Dict[str, Any]:
        """Perform network scan using auxiliary scanners"""
        if not self.console_session:
            if not self.start_console():
                return {"success": False, "error": "Failed to start console"}

        # Use port scanner
        result = self.use_module("auxiliary/scanner/portscan/tcp")
        if not result["success"]:
            return result

        # Set options
        self.set_option("RHOSTS", target)
        self.set_option("PORTS", ports)

        # Run scan
        return self.execute_command("run", timeout=120)

    def brute_force_service(
        self,
        target: str,
        service: str,
        userlist: Optional[str] = None,
        passlist: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Perform brute force attack on service"""
        if not self.console_session:
            if not self.start_console():
                return {"success": False, "error": "Failed to start console"}

        # Service module mapping
        service_modules = {
            "ssh": "auxiliary/scanner/ssh/ssh_login",
            "ftp": "auxiliary/scanner/ftp/ftp_login",
            "telnet": "auxiliary/scanner/telnet/telnet_login",
            "mysql": "auxiliary/scanner/mysql/mysql_login",
            "smb": "auxiliary/scanner/smb/smb_login",
        }

        module = service_modules.get(service.lower())
        if not module:
            return {"success": False, "error": f"Unsupported service: {service}"}

        # Load module
        result = self.use_module(module)
        if not result["success"]:
            return result

        # Set target
        self.set_option("RHOSTS", target)

        # Set wordlists if provided
        if userlist:
            self.set_option("USER_FILE", userlist)
        if passlist:
            self.set_option("PASS_FILE", passlist)

        # Run brute force
        return self.execute_command("run", timeout=300)

    def generate_payload(
        self, payload_type: str, lhost: str, lport: str, output_format: str = "exe"
    ) -> Dict[str, Any]:
        """Generate payload using msfvenom"""
        msfvenom_path = self.msf_path / "msfvenom"

        cmd = [
            str(msfvenom_path),
            "-p",
            payload_type,
            f"LHOST={lhost}",
            f"LPORT={lport}",
            "-f",
            output_format,
        ]

        return self._run_command(cmd, timeout=60)


def main():
    """CLI interface for Metasploit wrapper"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Metasploit Integration for CERBERUS-FANGS"
    )
    parser.add_argument(
        "command",
        choices=["init", "status", "search", "scan", "brute", "payload"],
        help="Command to execute",
    )
    parser.add_argument("--target", help="Target to attack/analyze")
    parser.add_argument("--service", help="Service to target")
    parser.add_argument("--ports", default="1-1000", help="Ports to scan")
    parser.add_argument("--payload", help="Payload type for generation")
    parser.add_argument("--lhost", help="Local host for payload")
    parser.add_argument("--lport", help="Local port for payload")
    parser.add_argument("--userlist", help="Username wordlist")
    parser.add_argument("--passlist", help="Password wordlist")
    parser.add_argument("--msf-path", help="Path to Metasploit Framework")
    parser.add_argument("--workspace", default="default", help="MSF workspace")

    args = parser.parse_args()

    try:
        msf = MetasploitWrapper(args.msf_path, args.workspace)
        result = None

        if args.command == "init":
            result = msf.initialize_database()
        elif args.command == "status":
            result = msf.check_database_status()
        elif args.command == "search":
            if not args.target:
                print("--target required for search command", file=sys.stderr)
                sys.exit(1)
            if msf.start_console():
                result = msf.search_exploits(args.target, args.service)
                msf.close_console()
        elif args.command == "scan":
            if not args.target:
                print("--target required for scan command", file=sys.stderr)
                sys.exit(1)
            if msf.start_console():
                result = msf.scan_network(args.target, args.ports)
                msf.close_console()
        elif args.command == "brute":
            if not args.target or not args.service:
                print(
                    "--target and --service required for brute command", file=sys.stderr
                )
                sys.exit(1)
            if msf.start_console():
                result = msf.brute_force_service(
                    args.target, args.service, args.userlist, args.passlist
                )
                msf.close_console()
        elif args.command == "payload":
            if not all([args.payload, args.lhost, args.lport]):
                print(
                    "--payload, --lhost, and --lport required for payload command",
                    file=sys.stderr,
                )
                sys.exit(1)
            result = msf.generate_payload(args.payload, args.lhost, args.lport)

        if result is not None:
            print(json.dumps(result, indent=2))
            sys.exit(0 if result["success"] else 1)
        else:
            print("Command execution failed", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
