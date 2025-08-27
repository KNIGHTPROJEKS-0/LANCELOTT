"""
Tests for authentication endpoints
"""

import requests


class TestAuthentication:
    """Test authentication system"""

    def test_get_token_valid_credentials(self, api_base_url):
        """Test getting token with valid credentials"""
        credentials = {"username": "admin", "password": "admin123"}

        response = requests.post(
            f"{api_base_url}/auth/token", json=credentials, timeout=10
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_get_token_invalid_credentials(self, api_base_url):
        """Test getting token with invalid credentials"""
        credentials = {"username": "invalid", "password": "invalid"}

        response = requests.post(
            f"{api_base_url}/auth/token", json=credentials, timeout=10
        )

        assert response.status_code == 401

    def test_protected_endpoint_without_token(self, api_base_url):
        """Test accessing protected endpoint without token"""
        response = requests.get(f"{api_base_url}/tools", timeout=10)

        assert response.status_code == 401

    def test_protected_endpoint_with_invalid_token(self, api_base_url):
        """Test accessing protected endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid-token"}

        response = requests.get(f"{api_base_url}/tools", headers=headers, timeout=10)

        assert response.status_code == 401

    def test_protected_endpoint_with_valid_token(self, api_base_url, auth_headers):
        """Test accessing protected endpoint with valid token"""
        response = requests.get(
            f"{api_base_url}/tools", headers=auth_headers, timeout=10
        )

        assert response.status_code == 200
