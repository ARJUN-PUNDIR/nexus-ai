"""
Unit tests for Reflection Quality Control Node
"""

from unittest.mock import patch, MagicMock
from app.graph.workflow import reflection_node


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
    assert "Critique:" in res["reflection"]["critique"]
