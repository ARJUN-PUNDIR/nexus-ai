"""
Unit tests for Stateful Multi-Turn Conversation Memory & Summarization
"""

from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage
from app.nodes.direct_nodes import direct_responder_node
from app.utils.memory_summarizer import prepare_summarized_messages


@patch("langchain_ollama.ChatOllama.invoke")
def test_prepare_summarized_messages_short(mock_invoke):
    state = {
        "messages": [
            HumanMessage(content="my name is arjun"),
            AIMessage(content="Hello Arjun!"),
        ],
        "summary": "",
    }
    prompt_seq, summary = prepare_summarized_messages(state)
    assert len(prompt_seq) == 3
    assert summary == ""


@patch("langchain_ollama.ChatOllama.invoke")
def test_prepare_summarized_messages_long(mock_invoke):
    mock_invoke.return_value = MagicMock(content="User's name is Arjun. User works on Nexus AI.")

    messages = [
        HumanMessage(content="hi"),
        AIMessage(content="Hello!"),
        HumanMessage(content="my name is arjun"),
        AIMessage(content="Nice to meet you Arjun!"),
        HumanMessage(content="I am building Nexus AI"),
        AIMessage(content="Awesome platform!"),
        HumanMessage(content="what is my name"),
    ]

    state = {
        "messages": messages,
        "summary": "",
    }

    prompt_seq, summary = prepare_summarized_messages(state)
    assert summary == "User's name is Arjun. User works on Nexus AI."
    assert len(prompt_seq) == 5
