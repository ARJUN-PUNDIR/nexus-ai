"""
Report Writer Node for Nexus AI
"""

from typing import Any
from langchain_core.messages import SystemMessage, AIMessage
from app.graph.state import AgentState
from app.config import get_llm
from app.utils.memory_summarizer import prepare_summarized_messages


# Initialize LLM via central Model Factory
llm = get_llm()


def writer_node(state: AgentState) -> dict[str, Any]:
    """
    Node: Report Writer
    Synthesizes search results (web + document RAG) and reflection audit feedback into a Markdown report.
    """
    query = state.get("research_query", "Research Topic")
    search_results = state.get("search_results", [])
    reflection = state.get("reflection", {})

    print(f"\n✍️  [NODE: Writer] Synthesizing comprehensive research report for: '{query}'")
    print(f"   └─ Combining context from {len(search_results)} search sources...")

    context_blocks = []
    for item in search_results:
        title = item.get("title", "Source")
        content = item.get("content", "")
        source_type = item.get("source_type", "web")
        context_blocks.append(f"=== {title} (Type: {source_type}) ===\n{content}")

    context_str = "\n\n".join(context_blocks)
    critique_str = reflection.get("critique", "No audit critique available.")

    synthesis_instruction = SystemMessage(
        content=f"""You are Nexus AI, an expert research assistant.

Quality Audit Critique:
{critique_str}

Retrieved Multi-Source Context:
{context_str}

Please generate a comprehensive, structured research report in Markdown format based on the retrieved context above.
Include:
# Executive Summary
# Key Findings
# Detailed Analysis
# Sources & References
"""
    )

    full_conversation, new_summary = prepare_summarized_messages(state)
    full_prompt = [synthesis_instruction] + full_conversation[1:]

    print("   └─ Invoking configured LLM model to synthesize final report...")
    response = llm.invoke(full_prompt)
    report_content = response.content
    print("   └─ ✅ Research report generation complete.")

    return {
        "summary": new_summary,
        "report": {"title": query, "content": report_content},
        "messages": [AIMessage(content=report_content)],
    }
