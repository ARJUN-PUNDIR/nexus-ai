"""
Unit tests for LLM-as-a-Router Edge
"""

from unittest.mock import patch, MagicMock
from app.nodes.direct_nodes import route_query


@patch("langchain_ollama.ChatOllama.invoke")
def test_route_query_direct_knowledge(mock_invoke):
    mock_invoke.return_value = MagicMock(content="DIRECT")
    state = {"research_query": "What is photosynthesis?"}
    assert route_query(state) == "direct_responder"


@patch("langchain_ollama.ChatOllama.invoke")
def test_route_query_search_needed(mock_invoke):
    mock_invoke.return_value = MagicMock(content="SEARCH")
    state = {"research_query": "Latest stock prices today 2026"}
    assert route_query(state) == "planner"
