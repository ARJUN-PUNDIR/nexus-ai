"""
Parallel Search Service
"""

from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
)

from app.tools import web_search


def build_parallel_search(
    queries: list[str],
) -> RunnableParallel:

    search_map = {}

    for index, query in enumerate(
        queries,
        start=1,
    ):

        search_map[f"search_{index}"] = RunnableLambda(

            lambda _, q=query: web_search.invoke(
                {
                    "query": q
                }
            )

        )

    return RunnableParallel(
        **search_map
    )