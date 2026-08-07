"""
Graph State for Nexus AI Multi-Agent Workflow
"""

from typing import Annotated, Any, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """
    Unified state dictionary passed between LangGraph nodes.
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
    summary: str
    research_query: str
    search_queries: list[str]
    search_results: list[dict[str, Any]]
    reflection: dict[str, Any] | None
    report: dict[str, Any] | None