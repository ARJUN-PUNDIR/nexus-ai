"""
Research Manager for Nexus AI
Orchestrates LangGraph execution and tracks step-by-step node outputs.
"""

from typing import Any
from langchain_core.messages import HumanMessage

from app.graph.workflow import graph
from app.services.report_service import save_report


class ResearchManager:
    """
    Manages stateful research workflows executed via LangGraph.
    """

    def __init__(self, thread_id: str = "user_1"):
        self.thread_id = thread_id

    def run(self, query: str) -> str:
        """
        Executes the LangGraph multi-node research pipeline.
        """
        config = {
            "configurable": {
                "thread_id": self.thread_id,
            }
        }

        initial_state = {
            "messages": [HumanMessage(content=query)],
            "research_query": query,
            "search_queries": [query],
            "search_results": [],
            "report": None,
        }

        print("\n" + "=" * 65)
        print(f"🚀 Starting Research Workflow for: '{query}'")
        print("=" * 65)

        final_report_content = ""

        # Stream graph node steps to display real-time node outputs
        for event in graph.stream(initial_state, config=config):
            for node_name, node_output in event.items():
                print(f"\n📌 Node Completed: [{node_name.upper()}]")
                if "search_results" in node_output:
                    print(f"   └─ Data Output: {len(node_output['search_results'])} search result items generated.")
                if "report" in node_output and node_output["report"]:
                    final_report_content = node_output["report"].get("content", "")
                    print(f"   └─ Data Output: Research report content generated successfully ({len(final_report_content)} bytes).")

        # Save Markdown report
        if final_report_content:
            try:
                saved_path = save_report(final_report_content, query)
                print(f"\n💾 Saved Report to: {saved_path}")
            except Exception as e:
                print(f"\n⚠️ Could not auto-save report: {e}")

        return final_report_content