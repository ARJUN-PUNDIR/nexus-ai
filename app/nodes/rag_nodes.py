"""
Local Document RAG Search Nodes for Nexus AI
"""

from typing import Any
from app.graph.state import AgentState
from app.services.rag_service import query_rag_index


def rag_search_node(state: AgentState) -> dict[str, Any]:
    """
    Node: Local Document RAG Searcher
    Queries local FAISS vector index for relevant document chunks (PDFs, Word docs, CSVs, TXT)
    matching the research query.
    """
    query = state.get("research_query", "")
    existing_results = list(state.get("search_results", []))

    print(f"\n📚 [NODE: RAGSearcher] Querying local FAISS document index for: '{query}'...")

    try:
        doc_results = query_rag_index(query, top_k=4)
        print(f"   └─ ✅ Retrieved {len(doc_results)} relevant document chunks from local storage.")

        formatted_items = [item.model_dump() for item in doc_results]
    except Exception as err:
        print(f"   └─ ⚠️ Local RAG search info: {err}")
        formatted_items = []

    combined_results = existing_results + formatted_items

    return {
        "search_results": combined_results,
    }
