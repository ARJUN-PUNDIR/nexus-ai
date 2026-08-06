"""
Nexus AI Multi-Node Graph Workflow with State Memory & LLM-as-a-Router
"""

from typing import Any
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from app.graph.state import AgentState
from app.tools import web_search_tool
from app.config.settings import OLLAMA_MODEL, OLLAMA_BASE_URL, TEMPERATURE


llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=TEMPERATURE,
)

memory = MemorySaver()

SYSTEM_PROMPT = """You are Nexus AI, an autonomous multi-agent research assistant.
You have stateful conversational memory. Always remember user details, facts, and context from previous turns in the conversation thread."""


def route_query(state: AgentState) -> str:
    """
    LLM-as-a-Router: Uses the LLM to decide if the query requires external
    real-time web search or if the LLM can answer directly using general knowledge/memory.
    """
    messages = state.get("messages", [])
    query = state.get("research_query", "")

    if not query and messages:
        last_msg = messages[-1]
        query = getattr(last_msg, "content", str(last_msg))

    print(f"\n🤔 [ROUTER: LLM] Analyzing intent for: '{query}'")

    router_prompt = f"""You are a query classifier for an AI research platform.
Analyze the user prompt below and decide if answering it REQUIRES real-time external web search (e.g. current news, stock prices, live weather, latest tech announcements, specific external articles).

If the prompt is a greeting, personal detail (e.g. telling name), memory recall, general knowledge, math, or coding, choose 'DIRECT'.
If the prompt explicitly requires up-to-date web search or recent external information, choose 'SEARCH'.

User Prompt: "{query}"

Output ONLY a single word: either SEARCH or DIRECT. Do not output anything else.
"""

    try:
        decision = llm.invoke(router_prompt).content.strip().upper()
        if "SEARCH" in decision:
            print("   └─ 🌐 Decision: SEARCH required. Routing to Web Searcher Node.")
            return "searcher"
        else:
            print("   └─ 💡 Decision: DIRECT answer sufficient. Routing to Direct Responder Node.")
            return "direct_responder"
    except Exception as err:
        print(f"   └─ ⚠️ Router warning ({err}). Defaulting to SEARCH.")
        return "searcher"


def direct_responder_node(state: AgentState) -> dict[str, Any]:
    """
    Direct Responder Node: Answers general knowledge, memory recall, and chat queries
    passing full conversation history to the LLM.
    """
    messages = list(state.get("messages", []))
    query = state.get("research_query", "")

    print(f"\n💬 [NODE: DirectResponder] Generating answer with full conversation history...")

    # Build full prompt sequence including system prompt + conversation history
    full_conversation = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm.invoke(full_conversation)
    answer = response.content
    print("   └─ ✅ Direct answer generation complete.")

    return {
        "report": {"title": query, "content": answer},
        "messages": [AIMessage(content=answer)],
    }


def searcher_node(state: AgentState) -> dict[str, Any]:
    """
    Searcher Node: Executes web search to gather external context.
    """
    query = state.get("research_query", "")
    print(f"\n🔍 [NODE: Searcher] Processing query: '{query}'")
    print("   └─ Calling Tavily Search API...")

    try:
        raw_results = web_search_tool.invoke(query)
        print("   └─ ✅ Web search completed successfully.")
        search_items = [
            {
                "title": "Web Search Results",
                "content": raw_results,
                "source_type": "web",
            }
        ]
    except Exception as err:
        print(f"   └─ ⚠️ Web search warning: {err}")
        search_items = [
            {
                "title": "Web Search Failed",
                "content": "No external context retrieved.",
                "source_type": "web",
            }
        ]

    return {
        "research_query": query,
        "search_results": search_items,
    }


def writer_node(state: AgentState) -> dict[str, Any]:
    """
    Writer Node: Synthesizes gathered context into a structured research report,
    taking into account the full conversation history.
    """
    query = state.get("research_query", "Research Topic")
    search_results = state.get("search_results", [])
    messages = list(state.get("messages", []))

    print(f"\n✍️  [NODE: Writer] Synthesizing research report for: '{query}'")
    print("   └─ Formatting context from search results...")

    context_str = "\n\n".join(
        f"--- Source ({item.get('source_type', 'web')}) ---\n{item.get('content', '')}"
        for item in search_results
    )

    synthesis_instruction = SystemMessage(
        content=f"""You are Nexus AI, an expert research assistant.

Retrieved Web Search Context:
{context_str}

Please generate a comprehensive, structured research report in Markdown format.
Include:
# Executive Summary
# Key Findings
# Detailed Analysis
# Sources & References
"""
    )

    full_conversation = [synthesis_instruction] + messages

    print("   └─ Invoking Ollama LLM to write report...")
    response = llm.invoke(full_conversation)
    report_content = response.content
    print("   └─ ✅ Research report generation complete.")

    return {
        "report": {"title": query, "content": report_content},
        "messages": [AIMessage(content=report_content)],
    }


# Build LangGraph Workflow with Memory Saver and LLM Router Edge
builder = StateGraph(AgentState)

builder.add_node("direct_responder", direct_responder_node)
builder.add_node("searcher", searcher_node)
builder.add_node("writer", writer_node)

# Conditional LLM Routing from START
builder.add_conditional_edges(
    START,
    route_query,
    {
        "searcher": "searcher",
        "direct_responder": "direct_responder",
    },
)

builder.add_edge("searcher", "writer")
builder.add_edge("writer", END)
builder.add_edge("direct_responder", END)

graph = builder.compile(checkpointer=memory)