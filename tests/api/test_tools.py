"""
Tests for core tools API endpoints
"""

import requests


class TestToolsAPI:
    """Test core tools API endpoints"""

    def test_health_check(self, api_base_url):
        """Test health check endpoint"""
        response = requests.get(f"{api_base_url}/health", timeout=10)

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_list_all_tools(self, api_base_url, auth_headers):
        """Test listing all integrated tools"""
        response = requests.get(
            f"{api_base_url}/tools", headers=auth_headers, timeout=10
        )

        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert isinstance(data["tools"], list)

        # Should include SuperTools
        tool_names = [tool["name"] for tool in data["tools"]]
        assert "SuperGateway" in tool_names
        assert "SuperCompat" in tool_names

    def test_get_tool_status_existing(self, api_base_url, auth_headers):
        """Test getting status of existing tool"""
        response = requests.get(
            f"{api_base_url}/tools/nmap/status", headers=auth_headers, timeout=10
        )

        assert response.status_code == 200
        data = response.json()
        assert "tool" in data
        assert "status" in data

    def test_get_tool_status_nonexistent(self, api_base_url, auth_headers):
        """Test getting status of non-existent tool"""
        response = requests.get(
            f"{api_base_url}/tools/nonexistent/status", headers=auth_headers, timeout=10
        )

        assert response.status_code == 404


class TestNmapAPI:
    """Test Nmap-specific API endpoints"""

    def test_nmap_presets(self, api_base_url, auth_headers):
        """Test getting Nmap scan presets"""
        response = requests.get(
            f"{api_base_url}/nmap/presets", headers=auth_headers, timeout=10
        )

        assert response.status_code == 200
        data = response.json()
        assert "presets" in data
        assert isinstance(data["presets"], list)

    def test_nmap_scan_list(self, api_base_url, auth_headers):
        """Test listing Nmap scans"""
        response = requests.get(
            f"{api_base_url}/nmap/scans", headers=auth_headers, timeout=10
        )

        assert response.status_code == 200
        data = response.json()
        assert "scans" in data
        assert isinstance(data["scans"], list)
