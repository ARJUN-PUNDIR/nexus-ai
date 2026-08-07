"""
Nexus AI Multi-Node Graph Workflow Definition with Smart 4-Way Intent Router
"""

from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState
from app.utils.memory_saver import get_sqlite_checkpointer

from app.nodes.direct_nodes import route_query, direct_responder_node
from app.nodes.web_search_nodes import (
    planner_node,
    searcher_node,
    reflection_node,
    route_reflection,
)
from app.nodes.rag_nodes import rag_search_node
from app.nodes.writer_node import writer_node


# Initialize Persistent SQLite Checkpointer Memory
memory = get_sqlite_checkpointer("nexus_memory.db")


def route_searcher(state: AgentState) -> str:
    """
    Conditional Edge after Web Searcher Node:
    - If research_mode == 'hybrid' -> Route to Local RAG Searcher Node next.
    - Else (web only) -> Route straight to Reflection Audit Node.
    """
    mode = state.get("research_mode", "web")
    if mode == "hybrid":
        return "rag_searcher"
    return "reflection"


# ---------------------------------------------------------
# Build LangGraph Multi-Agent Workflow
# ---------------------------------------------------------

builder = StateGraph(AgentState)

# Add Nodes
builder.add_node("direct_responder", direct_responder_node)
builder.add_node("planner", planner_node)
builder.add_node("searcher", searcher_node)
builder.add_node("rag_searcher", rag_search_node)
builder.add_node("reflection", reflection_node)
builder.add_node("writer", writer_node)

# Conditional 4-Way Router Edge from START
builder.add_conditional_edges(
    START,
    route_query,
    {
        "direct_responder": "direct_responder",
        "doc_searcher": "rag_searcher",
        "web_planner": "planner",
        "hybrid_planner": "planner",
    },
)

# Planner -> Searcher
builder.add_edge("planner", "searcher")

# Conditional Edge after Searcher: Hybrid goes to rag_searcher, Web goes to reflection
builder.add_conditional_edges(
    "searcher",
    route_searcher,
    {
        "rag_searcher": "rag_searcher",
        "reflection": "reflection",
    },
)

# Local RAG Searcher -> Reflection
builder.add_edge("rag_searcher", "reflection")

# Conditional Reflection Edge: Loop back to Searcher if INCOMPLETE, else proceed to Writer
builder.add_conditional_edges(
    "reflection",
    route_reflection,
    {
        "searcher": "searcher",
        "writer": "writer",
    },
)

builder.add_edge("writer", END)
builder.add_edge("direct_responder", END)

# Compile Graph with Persistent SQLite Memory
graph = builder.compile(checkpointer=memory)