"""
Tests for Query Validator
"""

from app.utils.query_validator import validate_query


def test_valid_query():

    result = validate_query(
        "LangChain"
    )

    assert result == "LangChain"


def test_remove_spaces():

    result = validate_query(
        "   LangChain   "
    )

    assert result == "LangChain"


def test_empty_query():

    try:

        validate_query("")

        assert False

    except ValueError:

        assert True