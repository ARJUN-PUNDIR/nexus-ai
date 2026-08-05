"""
Research Agent

Responsible for collecting
research from the internet.
"""

from app.services.parallel_search import (
    build_parallel_search
)

from app.services.context_merger import (
    merge_search_results
)


class ResearchAgent:

    def research(
        self,
        queries: list[str]
    ) -> str:
        """
        Execute research.
        """

        parallel = build_parallel_search(
            queries
        )

        search_results = parallel.invoke(None)

        merged_context = merge_search_results(
            search_results
        )

        return merged_context