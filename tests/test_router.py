"""
Unit tests for Smart 4-Way LLM-as-a-Router Edge
"""

from unittest.mock import patch, MagicMock
from app.nodes.direct_nodes import route_query


@patch("langchain_ollama.ChatOllama.invoke")
def test_route_query_direct(mock_invoke):
    mock_invoke.return_value = MagicMock(content="DIRECT")
    state = {"research_query": "What is photosynthesis?"}
    assert route_query(state) == "direct_responder"


@patch("langchain_ollama.ChatOllama.invoke")
def test_route_query_web(mock_invoke):
    mock_invoke.return_value = MagicMock(content="WEB")
    state = {"research_query": "Latest stock prices today 2026"}
    assert route_query(state) == "web_planner"


@patch("langchain_ollama.ChatOllama.invoke")
def test_route_query_doc(mock_invoke):
    mock_invoke.return_value = MagicMock(content="DOC")
    state = {"research_query": "Summarize my uploaded project PDF"}
    assert route_query(state) == "doc_searcher"


@patch("langchain_ollama.ChatOllama.invoke")
def test_route_query_hybrid(mock_invoke):
    mock_invoke.return_value = MagicMock(content="HYBRID")
    state = {"research_query": "Compare my uploaded CSV strategy with 2026 market news"}
    assert route_query(state) == "hybrid_planner"
