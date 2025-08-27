# Test configuration and utilities for CERBERUS-FANGS LANCELOTT

import sys
from pathlib import Path

import pytest

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Test environment configuration
TEST_CONFIG = {
    "BASE_URL": "http://localhost:7777",
    "API_VERSION": "v1",
    "TEST_TOKEN": "test-token-123",
    "TIMEOUT": 30,
    "MAX_RETRIES": 3,
}


# Test fixtures and utilities
@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration"""
    return TEST_CONFIG


@pytest.fixture(scope="session")
def api_base_url():
    """Provide API base URL"""
    return f"{TEST_CONFIG['BASE_URL']}/api/{TEST_CONFIG['API_VERSION']}"


@pytest.fixture(scope="session")
def auth_headers():
    """Provide authentication headers for API tests"""
    return {"Authorization": f"Bearer {TEST_CONFIG['TEST_TOKEN']}"}
