"""
Nexus AI Multi-Node Graph Workflow with Parallel Web Searches
"""

from typing import Any
from concurrent.futures import ThreadPoolExecutor
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from app.graph.state import AgentState
from app.tools import web_search_tool
from app.config.settings import OLLAMA_MODEL, OLLAMA_BASE_URL, TEMPERATURE


# Initialize Ollama LLM
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=TEMPERATURE,
)

# Initialize LangGraph Checkpointer Memory
memory = MemorySaver()

# Default System Prompt for Nexus AI
SYSTEM_PROMPT = """You are Nexus AI, an autonomous multi-agent research assistant.
You have stateful conversational memory. Always remember user details, facts, and context from previous turns in the conversation thread."""


def route_query(state: AgentState) -> str:
    """
    Step 1: LLM-as-a-Router Edge
    Decides whether the query requires external web search or if the LLM can answer directly.
    """
    messages = state.get("messages", [])
    query = state.get("research_query", "")

    # If research_query is empty, extract latest user message content
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
            print("   └─ 🌐 Decision: SEARCH required. Routing to Autonomous Planner Node.")
            return "planner"
        else:
            print("   └─ 💡 Decision: DIRECT answer sufficient. Routing to Direct Responder Node.")
            return "direct_responder"
    except Exception as err:
        print(f"   └─ ⚠️ Router warning ({err}). Defaulting to PLANNER.")
        return "planner"


def direct_responder_node(state: AgentState) -> dict[str, Any]:
    """
    Node: Direct Responder
    Handles simple chat, greetings, and general knowledge directly without calling Tavily Search API.
    """
    messages = list(state.get("messages", []))
    query = state.get("research_query", "")

    print(f"\n💬 [NODE: DirectResponder] Generating direct LLM response...")

    # Pass full conversation history to maintain memory
    full_conversation = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm.invoke(full_conversation)
    answer = response.content
    print("   └─ ✅ Direct answer generation complete.")

    return {
        "report": {"title": query, "content": answer},
        "messages": [AIMessage(content=answer)],
    }


def planner_node(state: AgentState) -> dict[str, Any]:
    """
    Node: Autonomous Research Planner
    Decomposes a complex research topic into 2-3 specific sub-queries for parallel search.
    """
    query = state.get("research_query", "")
    print(f"\n🎯 [NODE: Planner] Planning research strategy for: '{query}'")

    planner_prompt = f"""You are an Autonomous Research Planner.
Break down the research topic below into 2 to 3 specific, focused sub-queries for web search.

Topic: "{query}"

Rules:
1. Output ONLY 2 to 3 search queries, one per line.
2. Do not include numbers, bullet points, or extra text.
"""

    try:
        response = llm.invoke(planner_prompt).content.strip()
        # Clean lines to get list of search queries
        lines = [line.strip("- *1234567890. ") for line in response.split("\n") if line.strip()]
        sub_queries = [q for q in lines if len(q) > 3][:3]

        if not sub_queries:
            sub_queries = [query]
    except Exception as err:
        print(f"   └─ ⚠️ Planner warning ({err}). Using original query.")
        sub_queries = [query]

    print(f"   └─ Generated {len(sub_queries)} sub-queries:")
    for idx, sq in enumerate(sub_queries, start=1):
        print(f"      ├─ Sub-query {idx}: '{sq}'")

    return {
        "search_queries": sub_queries,
    }


def fetch_single_search(sub_query: str) -> dict[str, Any]:
    """
    Helper function to execute a single web search for a sub-query.
    Used concurrently in ThreadPoolExecutor.
    """
    try:
        raw_results = web_search_tool.invoke(sub_query)
        return {
            "title": f"Results for: {sub_query}",
            "content": raw_results,
            "source_type": "web",
        }
    except Exception as err:
        return {
            "title": f"Search Error for: {sub_query}",
            "content": f"Search failed: {err}",
            "source_type": "web",
        }


def searcher_node(state: AgentState) -> dict[str, Any]:
    """
    Node: Web Searcher (PARALLEL EXECUTION)
    Executes web searches for all sub-queries concurrently using ThreadPoolExecutor
    to cut latency by ~70%.
    """
    search_queries = state.get("search_queries", [])
    query = state.get("research_query", "")

    if not search_queries:
        search_queries = [query]

    print(f"\n⚡ [NODE: Searcher] Executing {len(search_queries)} web searches IN PARALLEL...")

    # Run all sub-query searches concurrently across parallel worker threads
    with ThreadPoolExecutor(max_workers=len(search_queries)) as executor:
        search_items = list(executor.map(fetch_single_search, search_queries))

    print(f"   └─ ✅ All {len(search_items)} parallel searches finished concurrently.")

    return {
        "search_results": search_items,
    }


def writer_node(state: AgentState) -> dict[str, Any]:
    """
    Node: Report Writer
    Synthesizes all search results from all sub-queries into a comprehensive Markdown report.
    """
    query = state.get("research_query", "Research Topic")
    search_results = state.get("search_results", [])
    messages = list(state.get("messages", []))

    print(f"\n✍️  [NODE: Writer] Synthesizing comprehensive research report for: '{query}'")
    print(f"   └─ Combining context from {len(search_results)} search sources...")

    # Combine context strings from all sub-query searches
    context_blocks = []
    for item in search_results:
        title = item.get("title", "Web Source")
        content = item.get("content", "")
        context_blocks.append(f"=== {title} ===\n{content}")

    context_str = "\n\n".join(context_blocks)

    synthesis_instruction = SystemMessage(
        content=f"""You are Nexus AI, an expert research assistant.

Retrieved Multi-Query Search Context:
{context_str}

Please generate a comprehensive, structured research report in Markdown format based on the retrieved context above.
Include:
# Executive Summary
# Key Findings
# Detailed Analysis
# Sources & References
"""
    )

    full_conversation = [synthesis_instruction] + messages

    print("   └─ Invoking Ollama LLM to synthesize final report...")
    response = llm.invoke(full_conversation)
    report_content = response.content
    print("   └─ ✅ Research report generation complete.")

    return {
        "report": {"title": query, "content": report_content},
        "messages": [AIMessage(content=report_content)],
    }


# ---------------------------------------------------------
# Build LangGraph Workflow
# ---------------------------------------------------------

builder = StateGraph(AgentState)

# Add all nodes to graph
builder.add_node("direct_responder", direct_responder_node)
builder.add_node("planner", planner_node)
builder.add_node("searcher", searcher_node)
builder.add_node("writer", writer_node)

# Conditional LLM Router Edge from START
builder.add_conditional_edges(
    START,
    route_query,
    {
        "planner": "planner",
        "direct_responder": "direct_responder",
    },
)

# Connect Research Pipeline Edges: Planner -> Searcher -> Writer -> END
builder.add_edge("planner", "searcher")
builder.add_edge("searcher", "writer")
builder.add_edge("writer", END)
builder.add_edge("direct_responder", END)

# Compile graph with MemorySaver checkpointer
graph = builder.compile(checkpointer=memory)