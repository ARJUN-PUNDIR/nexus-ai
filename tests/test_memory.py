"""
Unit tests for Stateful Multi-Turn Conversation Memory & Summarization
"""

from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage
from app.graph.workflow import direct_responder_node, prepare_summarized_messages


@patch("langchain_ollama.ChatOllama.invoke")
def test_prepare_summarized_messages_short(mock_invoke):
    # Short history (< 6 messages) does not trigger LLM summarizer call
    state = {
        "messages": [
            HumanMessage(content="my name is arjun"),
            AIMessage(content="Hello Arjun!"),
        ],
        "summary": "",
    }
    prompt_seq, summary = prepare_summarized_messages(state)
    assert len(prompt_seq) == 3  # SystemMessage + 2 messages
    assert summary == ""


@patch("langchain_ollama.ChatOllama.invoke")
def test_prepare_summarized_messages_long(mock_invoke):
    # Long history (> 6 messages) triggers summary generation
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
    # SystemMessage + recent 4 messages
    assert len(prompt_seq) == 5
