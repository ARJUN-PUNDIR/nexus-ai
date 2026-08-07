"""
Unit tests for LangChain Local Document RAG Service and Nodes
"""

from unittest.mock import patch, MagicMock
from app.nodes.rag_nodes import rag_search_node


@patch("app.nodes.rag_nodes.query_rag_index")
def test_rag_search_node_retrieval(mock_query):
    mock_item = MagicMock()
    mock_item.model_dump.return_value = {
        "title": "Document: sample.pdf",
        "content": "Sample PDF extracted context snippet.",
        "source_type": "document",
    }
    mock_query.return_value = [mock_item]

    state = {
        "research_query": "Sample test query",
        "search_results": [],
    }

    res = rag_search_node(state)

    assert "search_results" in res
    assert len(res["search_results"]) == 1
    assert res["search_results"][0]["source_type"] == "document"
