"""
Web Search & Quality Reflection Nodes for Nexus AI
"""

from typing import Any
from concurrent.futures import ThreadPoolExecutor
from langchain_ollama import ChatOllama

from app.graph.state import AgentState
from app.tools import web_search_tool
from app.config.settings import OLLAMA_MODEL, OLLAMA_BASE_URL, TEMPERATURE


# Initialize Ollama LLM
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=TEMPERATURE,
)


def planner_node(state: AgentState) -> dict[str, Any]:
    """
    Node: Autonomous Research Planner
    Decomposes a complex research topic into 2-3 specific sub-queries for parallel web search.
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
        "search_loop_count": 0,
    }


def fetch_single_search(sub_query: str) -> dict[str, Any]:
    """
    Helper function to execute a single web search for a sub-query concurrently.
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
    Executes web searches for all sub-queries concurrently using ThreadPoolExecutor.
    """
    search_queries = state.get("search_queries", [])
    existing_results = list(state.get("search_results", []))
    query = state.get("research_query", "")

    if not search_queries:
        search_queries = [query]

    print(f"\n⚡ [NODE: Searcher] Executing {len(search_queries)} web searches IN PARALLEL...")

    with ThreadPoolExecutor(max_workers=len(search_queries)) as executor:
        new_items = list(executor.map(fetch_single_search, search_queries))

    combined_results = existing_results + new_items
    print(f"   └─ ✅ {len(new_items)} searches finished concurrently. Total sources collected: {len(combined_results)}.")

    return {
        "search_results": combined_results,
    }


def reflection_node(state: AgentState) -> dict[str, Any]:
    """
    Node: Reflection & Quality Control Auditor
    Audits search result quality. If incomplete, generates targeted supplementary queries for re-search.
    """
    query = state.get("research_query", "")
    search_results = state.get("search_results", [])
    loop_count = state.get("search_loop_count", 0) + 1

    print(f"\n🧐 [NODE: Reflection] Auditing search result quality (Pass #{loop_count}) for: '{query}'")

    context_preview = "\n".join(item.get("content", "")[:300] for item in search_results[:3])

    audit_prompt = f"""You are a Quality Control Auditor for a research platform.
Analyze the retrieved search context for topic: "{query}"

Retrieved Context Preview:
{context_preview}

Critique the completeness of this context in 2 short sentences.
Format output as:
Critique: <2-sentence evaluation>
Status: COMPLETE (or INCOMPLETE)
"""

    try:
        response = llm.invoke(audit_prompt).content.strip()
        critique = response
        is_sufficient = "INCOMPLETE" not in response.upper()
    except Exception as err:
        critique = f"Audit completed ({err})."
        is_sufficient = True

    first_line = critique.splitlines()[0] if critique else "Search data inspected."
    print(f"   ├─ Audit Critique: {first_line}")
    print(f"   └─ Quality Status: {'ACCEPTED ✅' if is_sufficient else 'INCOMPLETE ⚠️ (Re-search requested)'}")

    supplementary_queries = []
    if not is_sufficient and loop_count < 2:
        print("   └─ 🔄 Generating targeted supplementary sub-queries for missing gaps...")
        supp_prompt = f"Topic: '{query}'. Search context is missing details. Output 2 specific sub-queries for web search, one per line:"
        try:
            supp_resp = llm.invoke(supp_prompt).content.strip()
            supplementary_queries = [q.strip("- *1234567890. ") for q in supp_resp.split("\n") if len(q.strip()) > 3][:2]
        except Exception:
            supplementary_queries = [f"{query} latest technical details"]

    return {
        "search_loop_count": loop_count,
        "search_queries": supplementary_queries if supplementary_queries else state.get("search_queries", []),
        "reflection": {
            "is_sufficient": is_sufficient,
            "critique": critique,
        },
    }


def route_reflection(state: AgentState) -> str:
    """
    Conditional Edge: Decides whether to trigger a supplementary re-search loop
    or proceed to the Writer Node.
    """
    reflection = state.get("reflection", {})
    loop_count = state.get("search_loop_count", 0)
    is_sufficient = reflection.get("is_sufficient", True)

    if not is_sufficient and loop_count < 2:
        print(f"\n🔄 [ROUTER: Reflection] Context INCOMPLETE after Pass #{loop_count}. Triggering Supplementary Search Loop! 🔄")
        return "searcher"

    print(f"\n✅ [ROUTER: Reflection] Quality criteria met (or max 2 loops reached). Proceeding to Report Writer.")
    return "writer"
