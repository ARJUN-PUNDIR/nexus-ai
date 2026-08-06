"""
LangGraph Workflow
"""

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.graph.state import AgentState
from app.agents import ResearchAgent


agent = ResearchAgent()


def agent_node(
    state: AgentState,
):

    query = state["messages"][-1]["content"]

    answer = agent.run(query)

    return {

        "messages": [

            *state["messages"],

            {

                "role": "assistant",

                "content": answer,

            }

        ]

    }


builder = StateGraph(AgentState)

builder.add_node(
    "agent",
    agent_node,
)

builder.add_edge(
    START,
    "agent",
)

builder.add_edge(
    "agent",
    END,
)

graph = builder.compile()