"""
Unit tests for Autonomous Research Planner Node
"""

from unittest.mock import patch, MagicMock
from app.graph.workflow import planner_node


@patch("langchain_ollama.ChatOllama.invoke")
def test_planner_node_decomposition(mock_invoke):
    mock_invoke.return_value = MagicMock(
        content="""Quantum computing principles 2026
NIST post-quantum cryptography standards
Quantum key distribution real world deployment"""
    )

    state = {"research_query": "Quantum Computing Cybersecurity 2026"}
    res = planner_node(state)

    assert "search_queries" in res
    assert len(res["search_queries"]) == 3
    assert "NIST post-quantum cryptography standards" in res["search_queries"]
