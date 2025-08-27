#!/usr/bin/env python3
"""
CERBERUS-FANGS LANCELOTT - n8n Integration Framework
Provides workflow automation capabilities using n8n
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import aiohttp
import requests


class N8nIntegration:
    """n8n workflow automation integration for LANCELOTT"""

    def __init__(
        self,
        n8n_url: str = "http://localhost:5678",
        n8n_path: str = None,
        webhook_url: str = None,
    ):
        self.n8n_url = n8n_url
        self.n8n_path = n8n_path or str(Path(__file__).parent.parent.parent / "n8n")
        self.webhook_url = webhook_url or f"{n8n_url}/webhook"
        self.logger = self._setup_logging()
        self.workflows: Dict[str, Dict] = {}

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for n8n integration"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        return logging.getLogger(__name__)

    async def check_n8n_health(self) -> bool:
        """Check if n8n instance is healthy"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.n8n_url}/healthz", timeout=10
                ) as response:
                    return response.status == 200
        except Exception as e:
            self.logger.warning(f"n8n health check failed: {e}")
            return False

    def start_n8n(self, tunnel: bool = False) -> subprocess.Popen:
        """Start n8n instance"""
        n8n_dir = Path(self.n8n_path)

        if not n8n_dir.exists():
            raise FileNotFoundError(f"n8n directory not found: {n8n_dir}")

        # Change to n8n directory
        os.chdir(n8n_dir)

        # Build command
        cmd = ["npx", "n8n", "start"]

        if tunnel:
            cmd.append("--tunnel")

        env = os.environ.copy()
        env.update(
            {
                "N8N_BASIC_AUTH_ACTIVE": "true",
                "N8N_BASIC_AUTH_USER": "admin",
                "N8N_BASIC_AUTH_PASSWORD": "lancelott",
                "N8N_HOST": "0.0.0.0",
                "N8N_PORT": "5678",
                "N8N_PROTOCOL": "http",
                "WEBHOOK_URL": self.webhook_url,
            }
        )

        self.logger.info("Starting n8n instance...")

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                cwd=n8n_dir,
            )

            # Wait a bit for startup
            time.sleep(5)

            if process.poll() is None:
                self.logger.info(f"n8n started successfully on {self.n8n_url}")
                return process
            else:
                stdout, stderr = process.communicate()
                self.logger.error(f"Failed to start n8n: {stderr.decode()}")
                raise RuntimeError("n8n failed to start")

        except Exception as e:
            self.logger.error(f"Error starting n8n: {e}")
            raise

    async def create_lancelott_workflows(self) -> Dict[str, str]:
        """Create predefined workflows for LANCELOTT operations"""
        workflows = {}

        # 1. Reconnaissance Workflow
        recon_workflow = {
            "name": "LANCELOTT Reconnaissance",
            "nodes": [
                {
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "position": [250, 300],
                    "parameters": {"httpMethod": "POST", "path": "recon"},
                },
                {
                    "name": "Nmap Scan",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [450, 300],
                    "parameters": {
                        "url": "http://localhost:7777/api/v1/nmap/scan",
                        "method": "POST",
                        "sendHeaders": True,
                        "headerParameters": {
                            "parameters": [
                                {"name": "Content-Type", "value": "application/json"}
                            ]
                        },
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {"name": "target", "value": "={{$json.target}}"},
                                {"name": "scan_type", "value": "quick"},
                            ]
                        },
                    },
                },
                {
                    "name": "SpiderFoot OSINT",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [650, 300],
                    "parameters": {
                        "url": "http://localhost:7777/api/v1/spiderfoot/scan",
                        "method": "POST",
                        "sendHeaders": True,
                        "headerParameters": {
                            "parameters": [
                                {"name": "Content-Type", "value": "application/json"}
                            ]
                        },
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {"name": "target", "value": "={{$json.target}}"}
                            ]
                        },
                    },
                },
                {
                    "name": "Generate Report",
                    "type": "n8n-nodes-base.function",
                    "position": [850, 300],
                    "parameters": {
                        "functionCode": "const nmap_results = $('Nmap Scan').first().json;\nconst spiderfoot_results = $('SpiderFoot OSINT').first().json;\n\nconst report = {\n  target: $json.target,\n  timestamp: new Date(),\n  nmap: nmap_results,\n  spiderfoot: spiderfoot_results,\n  summary: {\n    ports_found: nmap_results.open_ports?.length || 0,\n    vulnerabilities: spiderfoot_results.vulnerabilities?.length || 0\n  }\n};\n\nreturn { report };"
                    },
                },
            ],
            "connections": {
                "Webhook": {
                    "main": [[{"node": "Nmap Scan", "type": "main", "index": 0}]]
                },
                "Nmap Scan": {
                    "main": [[{"node": "SpiderFoot OSINT", "type": "main", "index": 0}]]
                },
                "SpiderFoot OSINT": {
                    "main": [[{"node": "Generate Report", "type": "main", "index": 0}]]
                },
            },
        }

        # 2. Vulnerability Assessment Workflow
        vuln_workflow = {
            "name": "LANCELOTT Vulnerability Assessment",
            "nodes": [
                {
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "position": [250, 300],
                    "parameters": {"httpMethod": "POST", "path": "vuln-assess"},
                },
                {
                    "name": "Argus Web Scan",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [450, 200],
                    "parameters": {
                        "url": "http://localhost:7777/api/v1/argus/scan",
                        "method": "POST",
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {"name": "target", "value": "={{$json.target}}"}
                            ]
                        },
                    },
                },
                {
                    "name": "Nmap Vuln Scan",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [450, 400],
                    "parameters": {
                        "url": "http://localhost:7777/api/v1/nmap/scan",
                        "method": "POST",
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {"name": "target", "value": "={{$json.target}}"},
                                {"name": "scan_type", "value": "vuln"},
                            ]
                        },
                    },
                },
                {
                    "name": "Merge Results",
                    "type": "n8n-nodes-base.merge",
                    "position": [650, 300],
                    "parameters": {"mode": "combine", "combineBy": "combineAll"},
                },
            ],
            "connections": {
                "Webhook": {
                    "main": [
                        [{"node": "Argus Web Scan", "type": "main", "index": 0}],
                        [{"node": "Nmap Vuln Scan", "type": "main", "index": 0}],
                    ]
                },
                "Argus Web Scan": {
                    "main": [[{"node": "Merge Results", "type": "main", "index": 0}]]
                },
                "Nmap Vuln Scan": {
                    "main": [[{"node": "Merge Results", "type": "main", "index": 1}]]
                },
            },
        }

        # 3. Social Engineering Workflow
        social_workflow = {
            "name": "LANCELOTT Social Engineering",
            "nodes": [
                {
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "position": [250, 300],
                    "parameters": {"httpMethod": "POST", "path": "social-eng"},
                },
                {
                    "name": "Social Analyzer",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [450, 300],
                    "parameters": {
                        "url": "http://localhost:7777/api/v1/social-analyzer/scan",
                        "method": "POST",
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {"name": "username", "value": "={{$json.username}}"}
                            ]
                        },
                    },
                },
                {
                    "name": "SHERLOCK",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [650, 300],
                    "parameters": {
                        "url": "http://localhost:7777/api/v1/sherlock/scan",
                        "method": "POST",
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {"name": "username", "value": "={{$json.username}}"}
                            ]
                        },
                    },
                },
            ],
            "connections": {
                "Webhook": {
                    "main": [[{"node": "Social Analyzer", "type": "main", "index": 0}]]
                },
                "Social Analyzer": {
                    "main": [[{"node": "SHERLOCK", "type": "main", "index": 0}]]
                },
            },
        }

        self.workflows = {
            "reconnaissance": recon_workflow,
            "vulnerability": vuln_workflow,
            "social": social_workflow,
        }

        return {
            name: f"{self.webhook_url}/{workflow['nodes'][0]['parameters']['path']}"
            for name, workflow in self.workflows.items()
        }

    async def install_workflow(self, workflow_name: str) -> bool:
        """Install a workflow to n8n instance"""
        if workflow_name not in self.workflows:
            self.logger.error(f"Unknown workflow: {workflow_name}")
            return False

        workflow = self.workflows[workflow_name]

        try:
            async with aiohttp.ClientSession() as session:
                auth = aiohttp.BasicAuth("admin", "lancelott")

                async with session.post(
                    f"{self.n8n_url}/rest/workflows", json=workflow, auth=auth
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        self.logger.info(
                            f"Workflow '{workflow_name}' installed with ID: {result.get('id')}"
                        )
                        return True
                    else:
                        error = await response.text()
                        self.logger.error(f"Failed to install workflow: {error}")
                        return False

        except Exception as e:
            self.logger.error(f"Error installing workflow: {e}")
            return False

    async def trigger_workflow(
        self, workflow_path: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Trigger a workflow via webhook"""
        try:
            async with aiohttp.ClientSession() as session:
                webhook_url = f"{self.webhook_url}/{workflow_path}"

                async with session.post(webhook_url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.logger.info(
                            f"Workflow triggered successfully: {workflow_path}"
                        )
                        return {"success": True, "data": result}
                    else:
                        error = await response.text()
                        self.logger.error(f"Failed to trigger workflow: {error}")
                        return {"success": False, "error": error}

        except Exception as e:
            self.logger.error(f"Error triggering workflow: {e}")
            return {"success": False, "error": str(e)}

    async def get_workflow_executions(self, workflow_id: str = None) -> List[Dict]:
        """Get workflow execution history"""
        try:
            async with aiohttp.ClientSession() as session:
                auth = aiohttp.BasicAuth("admin", "lancelott")
                url = f"{self.n8n_url}/rest/executions"

                if workflow_id:
                    url += f"?filter=%7B%22workflowId%22%3A%22{workflow_id}%22%7D"

                async with session.get(url, auth=auth) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("data", [])
                    else:
                        self.logger.error(
                            f"Failed to get executions: {response.status}"
                        )
                        return []

        except Exception as e:
            self.logger.error(f"Error getting executions: {e}")
            return []

    def export_workflows(self, output_path: str = None) -> str:
        """Export workflows to JSON file"""
        if output_path is None:
            output_path = (
                Path(__file__).parent / "workflows" / "lancelott_workflows.json"
            )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(output_path, "w") as f:
                json.dump(self.workflows, f, indent=2)

            self.logger.info(f"Workflows exported to {output_path}")
            return str(output_path)

        except Exception as e:
            self.logger.error(f"Failed to export workflows: {e}")
            raise

    async def setup_complete_integration(self) -> Dict[str, Any]:
        """Complete n8n integration setup"""
        self.logger.info("Setting up complete n8n integration...")

        results = {
            "n8n_healthy": False,
            "workflows_created": False,
            "workflows_installed": {},
            "webhook_urls": {},
        }

        # Check n8n health
        results["n8n_healthy"] = await self.check_n8n_health()

        if not results["n8n_healthy"]:
            self.logger.warning("n8n is not healthy, some features may not work")
            return results

        # Create workflows
        try:
            webhook_urls = await self.create_lancelott_workflows()
            results["workflows_created"] = True
            results["webhook_urls"] = webhook_urls

            # Install workflows
            for workflow_name in self.workflows.keys():
                success = await self.install_workflow(workflow_name)
                results["workflows_installed"][workflow_name] = success

            # Export workflows
            self.export_workflows()

            self.logger.info("n8n integration setup completed")

        except Exception as e:
            self.logger.error(f"Failed to setup n8n integration: {e}")
            results["error"] = str(e)

        return results


async def main():
    """CLI interface for n8n integration"""
    import argparse

    parser = argparse.ArgumentParser(description="LANCELOTT n8n Integration")
    parser.add_argument(
        "action",
        choices=["setup", "health", "trigger", "export", "start"],
        help="Action to perform",
    )
    parser.add_argument("--workflow", "-w", help="Workflow name or path")
    parser.add_argument("--data", "-d", help="JSON data for workflow trigger")
    parser.add_argument("--n8n-url", help="n8n instance URL")
    parser.add_argument("--tunnel", action="store_true", help="Start n8n with tunnel")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    try:
        integration = N8nIntegration(n8n_url=args.n8n_url)

        if args.action == "start":
            process = integration.start_n8n(tunnel=args.tunnel)
            print(f"n8n started with PID: {process.pid}")
            print(f"Access n8n at: {integration.n8n_url}")
            print("Press Ctrl+C to stop...")
            try:
                process.wait()
            except KeyboardInterrupt:
                process.terminate()
                print("n8n stopped")

        elif args.action == "health":
            healthy = await integration.check_n8n_health()
            print(f"n8n health: {'healthy' if healthy else 'unhealthy'}")

        elif args.action == "setup":
            results = await integration.setup_complete_integration()
            print("Setup Results:")
            print(json.dumps(results, indent=2, default=str))

        elif args.action == "trigger":
            if not args.workflow:
                print("--workflow is required for trigger action")
                sys.exit(1)

            data = json.loads(args.data) if args.data else {}
            result = await integration.trigger_workflow(args.workflow, data)
            print(json.dumps(result, indent=2))

        elif args.action == "export":
            path = integration.export_workflows(args.output)
            print(f"Workflows exported to: {path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
