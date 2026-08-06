"""
Unit tests for Stateful Multi-Turn Conversation Memory
"""

from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage
from app.graph.workflow import direct_responder_node, graph


@patch("langchain_ollama.ChatOllama.invoke")
def test_direct_responder_memory_preservation(mock_invoke):
    mock_invoke.return_value = MagicMock(content="Your name is Arjun!")

    state = {
        "messages": [
            HumanMessage(content="my name is arjun"),
            AIMessage(content="Hello Arjun!"),
            HumanMessage(content="what is my name"),
        ],
        "research_query": "what is my name",
    }

    res = direct_responder_node(state)
    assert len(mock_invoke.call_args[0][0]) == 4  # SystemMessage + 3 messages
    assert res["report"]["content"] == "Your name is Arjun!"
