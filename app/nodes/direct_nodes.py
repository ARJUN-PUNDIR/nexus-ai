"""
Direct Chat & 4-Way Intent Classifier Nodes for Nexus AI
"""

from typing import Any
from langchain_core.messages import AIMessage
from app.graph.state import AgentState
from app.config import get_llm
from app.utils.memory_summarizer import prepare_summarized_messages


# Initialize LLM via central Model Factory
llm = get_llm()


def route_query(state: AgentState) -> str:
    """
    Step 1: Smart 4-Way LLM Router Edge
    Classifies prompt into 1 of 4 clean routes:
    - DIRECT: Greetings, personal details, memory recall, general knowledge, math, coding.
    - WEB: Current news, live web data, online research.
    - DOC: Questions about local uploaded files, PDFs, CSVs, documents.
    - HYBRID: Prompts needing BOTH local uploaded docs AND live web news.
    """
    messages = state.get("messages", [])
    query = state.get("research_query", "")

    if not query and messages:
        last_msg = messages[-1]
        query = getattr(last_msg, "content", str(last_msg))

    print(f"\n🤔 [ROUTER: LLM] Analyzing intent for: '{query}'")

    router_prompt = f"""You are an intent classifier for an AI research platform.
Analyze the user prompt below and choose the SINGLE BEST route:

- 'DIRECT': Greeting, telling name, memory recall, general knowledge, math, coding.
- 'WEB': Requires current news, stock prices, live weather, external tech articles, internet search.
- 'DOC': Asks specifically about local uploaded files, PDFs, CSVs, data documents.
- 'HYBRID': Asks to compare/combine local uploaded files WITH external live web news.

User Prompt: "{query}"

Output ONLY a single word: DIRECT, WEB, DOC, or HYBRID. Do not output anything else.
"""

    try:
        decision = llm.invoke(router_prompt).content.strip().upper()
        if "DOC" in decision:
            print("   └─ 📚 Decision: DOC required (Local RAG). Routing directly to RAG Node (0 Web API calls).")
            state["research_mode"] = "doc"
            return "doc_searcher"
        elif "HYBRID" in decision:
            print("   └─ 🔀 Decision: HYBRID required (Web + Local Docs). Routing to Planner Node.")
            state["research_mode"] = "hybrid"
            return "hybrid_planner"
        elif "WEB" in decision or "SEARCH" in decision:
            print("   └─ 🌐 Decision: WEB required. Routing to Planner Node.")
            state["research_mode"] = "web"
            return "web_planner"
        else:
            print("   └─ 💡 Decision: DIRECT answer sufficient. Routing to Direct Responder Node.")
            state["research_mode"] = "direct"
            return "direct_responder"
    except Exception as err:
        print(f"   └─ ⚠️ Router warning ({err}). Defaulting to WEB.")
        state["research_mode"] = "web"
        return "web_planner"


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
