# AI Agent Testing Framework

A comprehensive testing framework for the AI Agent skills, routing, and collaboration systems.

## 📋 Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Types](#test-types)
- [Writing Tests](#writing-tests)
- [Configuration](#configuration)
- [Reports](#reports)

## 🎯 Overview

This testing framework provides:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Benchmark and validate performance
- **Comprehensive Fixtures**: Shared test utilities and data
- **Flexible Configuration**: Customize test behavior
- **Detailed Reports**: Generate test and coverage reports

## 📁 Directory Structure

```
tests/
├── __init__.py           # Package initialization
├── conftest.py           # Pytest configuration and fixtures
├── config/               # Test configuration files
│   ├── test_config.json  # Test settings
│   └── pytest.ini        # Pytest configuration
├── unit/                 # Unit tests
│   ├── test_skill_discovery.py
│   └── test_skill_router.py
├── integration/          # Integration tests
│   └── test_skill_integration.py
├── e2e/                  # End-to-end tests
├── performance/          # Performance tests
│   └── test_performance.py
├── fixtures/             # Test fixtures and mock data
├── utils/                # Test utilities and helpers
│   └── base_test.py      # Base test classes
├── reports/              # Test reports
│   ├── coverage/         # Coverage reports
│   ├── metrics/          # Performance metrics
│   └── logs/             # Test logs
├── run_all_tests.sh      # Bash test runner
└── README.md             # This file
```

## 🚀 Installation

### Prerequisites

```bash
pip install pytest pytest-cov pytest-html pytest-timeout
```

### Setup

The test framework is already configured. Just ensure you have the dependencies installed:

```bash
cd /d/claudecode
pip install -r requirements.txt  # If available
```

## 🏃 Running Tests

### Quick Start

Run all tests:

```bash
# Using Python script
python run_tests.py

# Using bash script
./tests/run_all_tests.sh

# Direct pytest
python -m pytest tests/ -v
```

### Run Specific Test Types

```bash
# Unit tests only
python run_tests.py unit

# Integration tests only
python run_tests.py integration

# Performance tests only
python run_tests.py performance
```

### Run with Options

```bash
# Verbose output
python run_tests.py all -v

# Filter by keyword
python run_tests.py all -k "test_route"

# With coverage
python run_tests.py all --cov

# Generate HTML report
python run_tests.py all --report
```

### Direct Pytest Commands

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/unit/test_skill_router.py -v

# Run specific test
python -m pytest tests/unit/test_skill_router.py::TestSkillRouter::test_router_creation -v

# Run with markers
python -m pytest -m unit -v
python -m pytest -m "not slow" -v
```

## 📝 Test Types

### Unit Tests (`tests/unit/`)

Test individual components in isolation:

```bash
python -m pytest tests/unit/ -v
```

### Integration Tests (`tests/integration/`)

Test component interactions:

```bash
python -m pytest tests/integration/ -v
```

### End-to-End Tests (`tests/e2e/`)

Test complete workflows:

```bash
python -m pytest tests/e2e/ -v
```

### Performance Tests (`tests/performance/`)

Benchmark and validate performance:

```bash
python -m pytest tests/performance/ -v
```

## ✍️ Writing Tests

### Base Test Classes

Import base classes from `utils/base_test.py`:

```python
from utils.base_test import SkillTestBase, RouterTestBase

class MyTest(SkillTestBase):
    def test_skill_metadata(self):
        metadata = {"name": "test", "description": "Test skill"}
        self.assert_valid_skill_metadata(metadata)
```

### Using Fixtures

Fixtures are defined in `conftest.py`:

```python
def test_with_fixture(skills_root):
    # skills_root is automatically provided
    assert skills_root.exists()
```

### Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit
def test_unit_functionality():
    pass

@pytest.mark.slow
def test_slow_operation():
    pass
```

## ⚙️ Configuration

### Test Configuration

Edit `tests/config/test_config.json`:

```json
{
  "test_settings": {
    "timeout": 30,
    "max_retries": 3,
    "parallel_workers": 4
  },
  "performance": {
    "thresholds": {
      "skill_loading": 5.0,
      "single_route": 1.0
    }
  }
}
```

### Pytest Configuration

Edit `tests/config/pytest.ini` or use command-line options.

## 📊 Reports

### Generate Reports

```bash
# HTML report
python -m pytest tests/ --html=tests/reports/report.html

# Coverage report
python -m pytest tests/ --cov=skills --cov-report=html

# Both
python run_tests.py all --cov --report
```

### Report Locations

- HTML Report: `tests/reports/test_report.html`
- Coverage Report: `tests/reports/coverage/index.html`
- Performance Metrics: `tests/reports/metrics/`
- Test Logs: `tests/reports/logs/`

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure skill_discovery is in your Python path
2. **Missing Fixtures**: Check that `conftest.py` is properly configured
3. **Timeout Errors**: Increase timeout in `test_config.json`

### Debug Mode

Run with extra output:

```bash
python -m pytest tests/ -vv --tb=long
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Coverage](https://pytest-cov.readthedocs.io/)
- Project Documentation: See project root docs/

## 🤝 Contributing

When adding new tests:

1. Place in appropriate directory (unit/integration/e2e/performance)
2. Use appropriate base test class
3. Add descriptive docstrings
4. Use markers for categorization
5. Update this README if needed

## 📄 License

Same as parent project.
