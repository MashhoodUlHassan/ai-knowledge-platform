import pytest

from app.agents.guardrails import validate_query


def test_valid_query():
    result = validate_query("What is machine learning?")

    assert result == "What is machine learning?"


def test_empty_query():
    with pytest.raises(ValueError, match="Query cannot be empty."):
        validate_query("")