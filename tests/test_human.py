"""
Unit tests for Interactive Terminal Plan Approval Node
"""

from unittest.mock import patch
from app.nodes.human_nodes import plan_approval_node


@patch("builtins.input", return_value="y")
def test_plan_approval_approve(mock_input):
    state = {
        "research_query": "Test Topic",
        "search_queries": ["query 1", "query 2"],
    }
    res = plan_approval_node(state)
    assert res["search_queries"] == ["query 1", "query 2"]


@patch("builtins.input", return_value="n")
def test_plan_approval_cancel(mock_input):
    state = {
        "research_query": "Test Topic",
        "search_queries": ["query 1", "query 2"],
    }
    res = plan_approval_node(state)
    assert res["search_queries"] == []


@patch("builtins.input", side_effect=["e", "custom 1, custom 2"])
def test_plan_approval_edit(mock_input):
    state = {
        "research_query": "Test Topic",
        "search_queries": ["query 1", "query 2"],
    }
    res = plan_approval_node(state)
    assert res["search_queries"] == ["custom 1", "custom 2"]
