"""
Research Service
"""

from app.planner.planner_chain import planner_chain
from app.planner.planner_parser import parse_plan

from app.services.parallel_search import (
    build_parallel_search,
)

from app.services.context_merger import (
    merge_search_results,
)


def build_context(query: str) -> str:
    """
    Complete research pipeline.

    Query
        ↓
    Planner
        ↓
    Parallel Search
        ↓
    Context Merger
    """

    # Step 1
    plan = planner_chain.invoke(
        {
            "query": query
        }
    )

    print("\n========== RESEARCH PLAN ==========\n")
    print(plan)

    # Step 2
    search_queries = parse_plan(plan)

    # Step 3
    parallel = build_parallel_search(
        search_queries
    )

    search_results = parallel.invoke(None)

    # Step 4
    merged_context = merge_search_results(
        search_results
    )

    return merged_context