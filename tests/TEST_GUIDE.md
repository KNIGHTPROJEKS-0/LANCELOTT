# 🧪 LANCELOTT Test Suite Guide

## Overview

The LANCELOTT framework includes a comprehensive test suite organized into multiple categories to ensure system reliability and functionality.

## 📂 Test Directory Structure

```
tests/
├── TEST_GUIDE.md           # This guide
├── README.md               # Test suite overview
├── conftest.py            # Pytest configuration
├── run_all_tests.py       # Main test runner
├── framework/             # Framework core tests
│   ├── test_framework.py  # Framework structure validation
│   └── __init__.py
├── tools/                 # Tool integration tests
│   ├── test_crush_integration.py  # Crush + CliWrap tests
│   └── __init__.py
├── integration/           # Integration tests
│   ├── test_integration.py       # Comprehensive integration
│   ├── test_langchain_integration.py  # LangChain AI tests
│   └── __init__.py
├── api/                   # API endpoint tests
│   ├── test_api_endpoints.py     # API functionality
│   ├── test_authentication.py   # Auth system tests
│   └── test_tool_routers.py     # Tool router tests
└── unit/                  # Unit tests
    ├── test_config.py     # Configuration tests
    ├── test_utils.py      # Utility function tests
    └── __init__.py
```

## 🚀 Running Tests

### Quick Test Commands

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific test categories
pytest tests/framework/     # Framework tests
pytest tests/tools/         # Tool integration tests
pytest tests/integration/   # Integration tests
pytest tests/api/          # API tests
pytest tests/unit/         # Unit tests

# Run with verbose output
pytest -v tests/

# Run with coverage
pytest --cov=. tests/
```

### Using Make Commands

```bash
make test          # Run complete test suite
make check         # Run health checks
make lint          # Run code linting
```

## 📊 Test Categories

### 1. Framework Tests (`framework/`)

**Purpose**: Validate core framework structure and functionality

**Tests Include**:

- Project structure validation
- Configuration system testing
- Core module imports
- Build system validation
- Documentation checks

**Key File**: `test_framework.py`

### 2. Tool Integration Tests (`tools/`)

**Purpose**: Test security tool integrations and wrappers

**Tests Include**:

- Crush CLI orchestrator integration
- CliWrap command wrapper integration
- Tool wrapper functionality
- Dependency validation
- Tool communication

**Key File**: `test_crush_integration.py`

### 3. Integration Tests (`integration/`)

**Purpose**: Test complete system integration scenarios

**Tests Include**:

- End-to-end workflow testing
- Multi-tool orchestration
- API integration testing
- LangChain AI integration
- N8N workflow testing
- Cross-component communication

**Key Files**:

- `test_integration.py`
- `test_langchain_integration.py`

### 4. API Tests (`api/`)

**Purpose**: Validate REST API endpoints and functionality

**Tests Include**:

- Endpoint accessibility
- Authentication and authorization
- Request/response validation
- Error handling
- Tool router functionality

**Key Files**:

- `test_api_endpoints.py`
- `test_authentication.py`
- `test_tool_routers.py`

### 5. Unit Tests (`unit/`)

**Purpose**: Test individual components and functions

**Tests Include**:

- Configuration parsing
- Utility functions
- Data models
- Helper methods
- Error handling

**Key Files**:

- `test_config.py`
- `test_utils.py`

## 🔧 Test Configuration

### Pytest Configuration (`conftest.py`)

```python
# Test fixtures and configuration
@pytest.fixture
def app():
    # FastAPI test app setup

@pytest.fixture
def client():
    # Test client setup

@pytest.fixture
def mock_tool():
    # Mock tool integration
```

### Test Runner (`run_all_tests.py`)

The main test runner provides:

- Comprehensive test execution
- Progress reporting
- Success/failure statistics
- Integration with framework components
- Automated test discovery

## 📈 Test Coverage Goals

### Coverage Targets

- **Framework Core**: >90% coverage
- **Tool Integrations**: >80% coverage
- **API Endpoints**: >95% coverage
- **Critical Paths**: 100% coverage

### Coverage Commands

```bash
# Generate coverage report
pytest --cov=. --cov-report=html tests/

# View coverage in terminal
pytest --cov=. --cov-report=term-missing tests/

# Coverage for specific modules
pytest --cov=api --cov=core tests/
```

## 🧩 Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

### Example Test Structure

```python
import pytest
from fastapi.testclient import TestClient
from app import app

class TestToolIntegration:

    def setup_method(self):
        """Setup before each test"""
        self.client = TestClient(app)

    def test_tool_health_endpoint(self):
        """Test tool health endpoint"""
        response = self.client.get("/api/v1/tools/nmap/health")
        assert response.status_code == 200

    async def test_async_tool_execution(self):
        """Test async tool execution"""
        # Async test implementation
        pass
```

### Mocking Guidelines

```python
from unittest.mock import Mock, patch

@patch('integrations.tools.nmap_wrapper.NmapWrapper')
def test_nmap_integration(mock_nmap):
    """Test with mocked tool"""
    mock_nmap.return_value.execute.return_value = {"success": True}
    # Test implementation
```

## 🔍 Test Data Management

### Test Data Location

- Test fixtures: `tests/fixtures/`
- Mock data: `tests/data/`
- Sample configurations: `tests/config/`

### Environment Variables

```bash
# Test environment variables
TESTING=true
DATABASE_URL=sqlite:///./test.db
LOG_LEVEL=DEBUG
```

## 📋 Test Checklist

### Before Running Tests

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Configuration files present
- [ ] Test database available
- [ ] Required tools accessible

### Test Execution

- [ ] All test categories pass
- [ ] No critical errors
- [ ] Coverage targets met
- [ ] Performance within limits
- [ ] No memory leaks

### After Tests

- [ ] Clean up test data
- [ ] Review coverage report
- [ ] Update documentation
- [ ] Commit test improvements

## 🚨 Continuous Integration

### CI Pipeline Integration

```yaml
# GitHub Actions example
- name: Run Tests
  run: |
    python tests/run_all_tests.py
    pytest --cov=. tests/
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🎯 Test Best Practices

### Guidelines

1. **Isolation**: Tests should be independent
2. **Speed**: Fast execution for frequent running
3. **Reliability**: Consistent results across environments
4. **Clarity**: Clear test names and documentation
5. **Coverage**: Aim for high code coverage

### Common Patterns

- Use fixtures for test setup
- Mock external dependencies
- Test both success and failure cases
- Include edge case testing
- Validate error messages

## 📞 Troubleshooting

### Common Issues

- **Import Errors**: Check PYTHONPATH and virtual environment
- **Database Issues**: Ensure test database is accessible
- **Tool Dependencies**: Verify security tools are installed
- **Permission Errors**: Check file and directory permissions

### Debug Commands

```bash
# Run tests with debugging
pytest -s -v tests/

# Run specific test with output
pytest -s tests/integration/test_integration.py::test_specific_function

# Debug with pdb
pytest --pdb tests/
```

---

**Happy Testing!** 🧪✨

For questions or issues, refer to the main documentation or create an issue in the project repository.
