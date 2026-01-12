"""
Base Test Classes

Provides base classes for different types of tests.
"""

import pytest
import time
from typing import Any, Dict, Optional
from pathlib import Path


class BaseTest:
    """Base class for all tests."""

    @staticmethod
    def setup_method():
        """Setup method called before each test."""
        pass

    @staticmethod
    def teardown_method():
        """Teardown method called after each test."""
        pass

    def assert_almost_equal(self, a: float, b: float, delta: float = 0.001):
        """Assert two floats are almost equal."""
        assert abs(a - b) < delta, f"{a} != {b} (delta: {delta})"

    def assert_in_range(self, value: float, min_val: float, max_val: float):
        """Assert value is in range [min_val, max_val]."""
        assert min_val <= value <= max_val, \
            f"{value} not in range [{min_val}, {max_val}]"

    def assert_valid_percentage(self, value: float):
        """Assert value is a valid percentage (0-100)."""
        self.assert_in_range(value, 0, 100)


class SkillTestBase(BaseTest):
    """Base class for skill-related tests."""

    def assert_valid_skill_metadata(self, metadata: Dict[str, Any]):
        """Assert skill metadata has required fields."""
        required_fields = ["name", "description", "version", "category"]
        for field in required_fields:
            assert field in metadata, f"Missing required field: {field}"

    def assert_valid_skill_name(self, name: str):
        """Assert skill name is valid."""
        assert name, "Skill name cannot be empty"
        assert isinstance(name, str), "Skill name must be a string"

    def assert_valid_category(self, category: str):
        """Assert category is valid."""
        valid_categories = ["design", "code", "analysis", "testing", "documentation"]
        assert category in valid_categories, \
            f"Invalid category: {category}. Must be one of {valid_categories}"


class RouterTestBase(BaseTest):
    """Base class for router tests."""

    def assert_valid_route_result(self, result: Any):
        """Assert route result has required attributes."""
        assert hasattr(result, "primary"), "Route result must have 'primary' attribute"
        assert hasattr(result, "confidence"), "Route result must have 'confidence' attribute"
        self.assert_valid_percentage(result.confidence)

    def assert_route_succeeded(self, result: Any):
        """Assert route operation succeeded."""
        assert result.primary, "Route result should not be empty"
        assert result.confidence > 0, "Confidence should be greater than 0"


class PerformanceTestBase(BaseTest):
    """Base class for performance tests."""

    @staticmethod
    def measure_execution_time(func, *args, **kwargs) -> tuple:
        """Measure execution time of a function."""
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        return result, elapsed

    def assert_performance_threshold(self, elapsed: float, threshold: float):
        """Assert execution time is within threshold."""
        assert elapsed <= threshold, \
            f"Performance threshold exceeded: {elapsed:.4f}s > {threshold:.4f}s"

    def assert_memory_usage_reasonable(self, memory_mb: float, max_mb: float = 500):
        """Assert memory usage is reasonable."""
        assert memory_mb < max_mb, \
            f"Memory usage too high: {memory_mb}MB > {max_mb}MB"


class IntegrationTestBase(BaseTest):
    """Base class for integration tests."""

    def assert_system_integration(self, component_a: Any, component_b: Any):
        """Assert two components can integrate."""
        # Placeholder for integration assertions
        assert component_a is not None, "Component A should not be None"
        assert component_b is not None, "Component B should not be None"

    def assert_data_flow(self, input_data: Any, output_data: Any):
        """Assert data flows correctly through the system."""
        assert input_data is not None, "Input data should not be None"
        assert output_data is not None, "Output data should not be None"


class E2ETestBase(BaseTest):
    """Base class for end-to-end tests."""

    def assert_complete_workflow(self, result: Any):
        """Assert a complete workflow executed successfully."""
        assert result is not None, "Workflow result should not be None"
        if hasattr(result, "success"):
            assert result.success, "Workflow should report success"

    def assert_user_satisfied(self, result: Any):
        """Assert result meets user expectations."""
        # Placeholder for user satisfaction assertions
        assert result is not None, "Result should not be None"
