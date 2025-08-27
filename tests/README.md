# CERBERUS-FANGS LANCELOTT Test Suite

This directory contains all test files for the CERBERUS-FANGS LANCELOTT security platform.

## Directory Structure

```
tests/
├── conftest.py           # Test configuration and fixtures
├── unit/                 # Unit tests for individual components
│   ├── test_supertools.py    # SuperGateway & SuperCompat tests
│   └── test_setup.py         # Setup and configuration tests
├── integration/          # Integration tests for API endpoints
│   └── test_simple_integration.py  # Basic integration tests
└── api/                  # API-specific tests
    ├── test_auth.py          # Authentication tests
    ├── test_tools.py         # Tool API tests
    └── test_supertools_api.py # SuperTools API tests
```

## Running Tests

### All Tests

```bash
# From project root
python -m pytest tests/

# With coverage
python -m pytest tests/ --cov=core --cov=api
```

### Specific Test Categories

```bash
# Unit tests only
python -m pytest tests/unit/

# Integration tests only
python -m pytest tests/integration/

# API tests only
python -m pytest tests/api/
```

### Individual Test Files

```bash
python -m pytest tests/unit/test_supertools.py
python -m pytest tests/integration/test_simple_integration.py
```

## Test Configuration

Tests use the configuration defined in `conftest.py`:

- **Base URL**: <http://localhost:7777>
- **API Version**: v1
- **Test Token**: test-token-123
- **Timeout**: 30 seconds

## Prerequisites

Ensure the following are installed:

```bash
pip install pytest pytest-cov requests
```

And that the server is running:

```bash
python main.py
```
