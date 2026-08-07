"""
Unit tests for Reflection Quality Control Node and Re-Search Loop Router
"""

from unittest.mock import patch, MagicMock
from app.graph.workflow import reflection_node, route_reflection


@patch("langchain_ollama.ChatOllama.invoke")
def test_reflection_node_audit(mock_invoke):
    mock_invoke.return_value = MagicMock(
        content="Critique: Context provides comprehensive coverage of quantum computing principles.\nStatus: COMPLETE"
    )

    state = {
        "research_query": "Quantum Computing 2026",
        "search_results": [{"title": "Source 1", "content": "Quantum principles and superposition details."}],
    }

    res = reflection_node(state)

    assert "reflection" in res
    assert res["reflection"]["is_sufficient"] is True


def test_route_reflection_complete():
    state = {
        "reflection": {"is_sufficient": True},
        "search_loop_count": 1,
    }
    assert route_reflection(state) == "writer"


def test_route_reflection_incomplete_triggers_research():
    state = {
        "reflection": {"is_sufficient": False},
        "search_loop_count": 1,
    }
    assert route_reflection(state) == "searcher"


def test_route_reflection_max_loops():
    state = {
        "reflection": {"is_sufficient": False},
        "search_loop_count": 2,  # Max loops reached
    }
    assert route_reflection(state) == "writer"
