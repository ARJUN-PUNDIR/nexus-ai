"""
Human-in-the-Loop Plan Approval Node for Nexus AI Terminal CLI
Waits for user in terminal to Approve [y], Edit [e], or Cancel [n].
"""

from typing import Any
from app.graph.state import AgentState


def plan_approval_node(state: AgentState) -> dict[str, Any]:
    """
    Human-in-the-Loop Node:
    Displays proposed sub-queries in terminal and pauses until the user inputs y, e, or n.
    """
    sub_queries = state.get("search_queries", [])
    query = state.get("research_query", "")

    if not sub_queries:
        return {"search_queries": [query]}

    print("\n" + "=" * 65)
    print(f"🎯 [HUMAN REVIEW] Research Plan for: '{query}'")
    print("=" * 65)
    print("Nexus AI proposes searching the web for these sub-queries:")

    for idx, sq in enumerate(sub_queries, start=1):
        print(f"  {idx}. '{sq}'")

    print("-" * 65)

    try:
        user_choice = input("👉 Approve plan? [y = Yes / e = Edit / n = Cancel]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        user_choice = "y"

    if user_choice == "n":
        print("   └─ ❌ Research plan cancelled by user.")
        return {
            "search_queries": [],
            "report": {
                "title": query,
                "content": "Research was cancelled by the user during plan approval.",
            },
        }
    elif user_choice == "e":
        print("\n✏️  [EDIT PLAN] Type custom sub-queries (comma separated):")
        try:
            custom_input = input("👉 Enter queries: ").strip()
            if custom_input:
                edited = [q.strip() for q in custom_input.split(",") if q.strip()]
                print(f"   └─ ✅ Updated sub-queries: {edited}")
                return {"search_queries": edited}
        except (EOFError, KeyboardInterrupt):
            pass

    print("   └─ ✅ Research plan APPROVED by user. Proceeding to search...")
    return {"search_queries": sub_queries}
