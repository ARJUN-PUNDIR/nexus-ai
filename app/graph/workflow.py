"""
Nexus AI Workflow
"""

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.checkpoint.memory import MemorySaver

from app.graph.state import AgentState
from app.agents import ResearchAgent


memory = MemorySaver()

research_agent = ResearchAgent()


def research_node(
    state: AgentState,
) -> AgentState:

    answer = research_agent.run(
        state["messages"]
    )

    return {
        "messages": [
            {
                "role": "assistant",
                "content": answer,
            }
        ]
    }


builder = StateGraph(AgentState)

builder.add_node(
    "research",
    research_node,
)

builder.add_edge(
    START,
    "research",
)

builder.add_edge(
    "research",
    END,
)

graph = builder.compile(
    checkpointer=memory,
)