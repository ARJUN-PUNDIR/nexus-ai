"""
Direct Chat & Intent Classifier Nodes for Nexus AI
"""

from typing import Any
from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama

from app.graph.state import AgentState
from app.utils.memory_summarizer import prepare_summarized_messages
from app.config.settings import OLLAMA_MODEL, OLLAMA_BASE_URL, TEMPERATURE


# Initialize Ollama LLM
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=TEMPERATURE,
)


def route_query(state: AgentState) -> str:
    """
    Step 1: LLM-as-a-Router Edge
    Decides whether the query requires external web search, local document RAG, or direct response.
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
    Uses token-efficient conversation memory (System Prompt + Summary + Recent 4 Messages).
    """
    query = state.get("research_query", "")
    print(f"\n💬 [NODE: DirectResponder] Generating answer using summarized conversation memory...")

    full_conversation, new_summary = prepare_summarized_messages(state)

    response = llm.invoke(full_conversation)
    answer = response.content
    print("   └─ ✅ Direct answer generation complete.")

    return {
        "summary": new_summary,
        "report": {"title": query, "content": answer},
        "messages": [AIMessage(content=answer)],
    }
