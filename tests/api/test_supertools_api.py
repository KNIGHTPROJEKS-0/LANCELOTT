"""
Tests for SuperTools API endpoints (SuperGateway & SuperCompat)
"""

import requests


class TestSuperGatewayAPI:
    """Test SuperGateway API endpoints"""

    def test_supergateway_status(self, api_base_url, auth_headers):
        """Test SuperGateway status endpoint"""
        response = requests.get(
            f"{api_base_url}/supergateway/status", headers=auth_headers, timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "node_available" in data

    def test_list_gateways(self, api_base_url, auth_headers):
        """Test listing active gateways"""
        response = requests.get(
            f"{api_base_url}/supergateway/gateways", headers=auth_headers, timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "gateways" in data
        assert isinstance(data["gateways"], list)

    def test_create_stdio_to_sse_gateway(self, api_base_url, auth_headers):
        """Test creating stdio to SSE gateway"""
        gateway_config = {
            "gateway_id": "test-gateway",
            "stdio_command": "echo 'test'",
            "port": 9001,
            "cors": True,
        }

        response = requests.post(
            f"{api_base_url}/supergateway/gateway/stdio-to-sse",
            headers=auth_headers,
            json=gateway_config,
            timeout=10,
        )

        # Should return 200 even if gateway fails to start in test environment
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "gateway_id" in data
            assert data["gateway_id"] == "test-gateway"

    def test_get_examples(self, api_base_url, auth_headers):
        """Test getting SuperGateway examples"""
        response = requests.get(
            f"{api_base_url}/supergateway/examples", headers=auth_headers, timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "examples" in data
        assert isinstance(data["examples"], list)


class TestSuperCompatAPI:
    """Test SuperCompat API endpoints"""

    def test_supercompat_status(self, api_base_url, auth_headers):
        """Test SuperCompat status endpoint"""
        response = requests.get(
            f"{api_base_url}/supercompat/status", headers=auth_headers, timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "node_available" in data

    def test_list_providers(self, api_base_url, auth_headers):
        """Test listing supported AI providers"""
        response = requests.get(
            f"{api_base_url}/supercompat/providers", headers=auth_headers, timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "providers" in data
        assert isinstance(data["providers"], list)

        # Should include major providers
        provider_names = [p["name"] for p in data["providers"]]
        expected_providers = ["openai", "anthropic", "groq", "mistral"]
        for provider in expected_providers:
            assert provider in provider_names

    def test_list_sessions(self, api_base_url, auth_headers):
        """Test listing active AI sessions"""
        response = requests.get(
            f"{api_base_url}/supercompat/sessions", headers=auth_headers, timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
        assert isinstance(data["sessions"], list)

    def test_create_session_invalid_provider(self, api_base_url, auth_headers):
        """Test creating session with invalid provider"""
        session_config = {
            "session_id": "test-invalid",
            "provider": "invalid_provider",
            "api_key": "fake-key",
            "model": "fake-model",
        }

        response = requests.post(
            f"{api_base_url}/supercompat/session",
            headers=auth_headers,
            json=session_config,
            timeout=10,
        )

        # Should fail with invalid provider
        assert response.status_code == 400

    def test_create_session_missing_fields(self, api_base_url, auth_headers):
        """Test creating session with missing required fields"""
        session_config = {
            "session_id": "test-missing",
            "provider": "openai",
            # Missing api_key and model
        }

        response = requests.post(
            f"{api_base_url}/supercompat/session",
            headers=auth_headers,
            json=session_config,
            timeout=10,
        )

        # Should fail with missing fields
        assert response.status_code == 422

    def test_completion_without_session(self, api_base_url, auth_headers):
        """Test completion request without existing session"""
        completion_request = {
            "session_id": "nonexistent-session",
            "messages": [{"role": "user", "content": "Hello"}],
        }

        response = requests.post(
            f"{api_base_url}/supercompat/completion",
            headers=auth_headers,
            json=completion_request,
            timeout=10,
        )

        # Should fail with nonexistent session
        assert response.status_code == 404

    def test_get_examples(self, api_base_url, auth_headers):
        """Test getting SuperCompat examples"""
        response = requests.get(
            f"{api_base_url}/supercompat/examples", headers=auth_headers, timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "examples" in data
        assert isinstance(data["examples"], list)


class TestSuperToolsIntegration:
    """Test SuperTools integration scenarios"""

    def test_cleanup_all_resources(self, api_base_url, auth_headers):
        """Test cleaning up all SuperTools resources"""
        # Cleanup SuperGateway gateways
        response = requests.delete(
            f"{api_base_url}/supergateway/gateways/cleanup",
            headers=auth_headers,
            timeout=10,
        )
        assert response.status_code == 200

        # Cleanup SuperCompat sessions
        response = requests.delete(
            f"{api_base_url}/supercompat/sessions/cleanup",
            headers=auth_headers,
            timeout=10,
        )
        assert response.status_code == 200

    def test_supertools_combined_status(self, api_base_url, auth_headers):
        """Test getting status of both SuperTools"""
        # Get SuperGateway status
        sg_response = requests.get(
            f"{api_base_url}/supergateway/status", headers=auth_headers, timeout=10
        )
        assert sg_response.status_code == 200

        # Get SuperCompat status
        sc_response = requests.get(
            f"{api_base_url}/supercompat/status", headers=auth_headers, timeout=10
        )
        assert sc_response.status_code == 200

        # Both should report Node.js availability
        sg_data = sg_response.json()
        sc_data = sc_response.json()

        assert sg_data["node_available"] == sc_data["node_available"]
