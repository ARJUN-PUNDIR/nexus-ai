"""
Research Agent
"""

from app.models import (
    ResearchPlan,
    ResearchContext,
)

from app.services import (
    build_parallel_search,
    merge_results,
)

class ResearchAgent:

    """
    Responsible for collecting
    information from the web.
    """

    def research(
        self,
        plan: ResearchPlan,
        query: str,
    ) -> ResearchContext:

        parallel = build_parallel_search(
            plan.queries
        )

        search_results = parallel.invoke(
            None
        )

        merged_context = merge_results(
            search_results
        )

        return ResearchContext(

            query=query,

            search_queries=plan.queries,
            raw_results=search_results,

            merged_context=merged_context,

        )