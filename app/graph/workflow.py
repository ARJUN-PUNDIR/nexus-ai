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
from app.memory import conversation


agent = ResearchAgent()


def agent_node(
    state: AgentState,
):

    messages = [

        *state["history"],

        *state["messages"],

    ]

    query = messages[-1]["content"]


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


def load_memory_node(
    state: AgentState,
):

    return {

        "history": conversation,

        "messages": state["messages"],

    }



def save_memory_node(
    state: AgentState,
):

    conversation.extend(

        state["messages"]

    )
    print()

    print("="*60)

    print("MEMORY")

    print("="*60)

    print(conversation)

    print("="*60)

    return state


builder = StateGraph(AgentState)

builder.add_node(
    "load_memory",
    load_memory_node,
)

builder.add_node(
    "agent",
    agent_node,
)

builder.add_node(
    "save_memory",
    save_memory_node,
)

builder.add_edge(
    START,
    "load_memory",
)

builder.add_edge(
    "load_memory",
    "agent",
)

builder.add_edge(
    "agent",
    "save_memory",
)

builder.add_edge(
    "save_memory",
    END,
)

graph = builder.compile()