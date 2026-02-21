"""Pytest configuration and shared fixtures for the sample tests."""

import pytest


@pytest.fixture
def sample_strings():
    """Fixture providing sample string test values."""
    return {
        "json_object": '{"key": "value"}',
        "json_array": '[1, 2, 3]',
        "boolean": 'true',
        "number": '42',
        "float": '3.14',
        "regex": '/[a-z]+/',
        "plain_string": 'hello',
    }


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "json: mark test as testing JSON parsing"
    )
    config.addinivalue_line(
        "markers", "regex: mark test as testing regex parsing"
    )
    config.addinivalue_line(
        "markers", "number: mark test as testing number parsing"
    )
    config.addinivalue_line(
        "markers", "edge_case: mark test as testing edge cases"
    )
