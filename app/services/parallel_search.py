from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
)

from app.tools.web_search import web_search


def perform_search(query: str):

    return web_search.invoke(
        {
            "query": query
        }
    )


def build_parallel_search(queries: list[str]):

    search_map = {}

    for index, query in enumerate(queries, start=1):

        search_map[f"search_{index}"] = RunnableLambda(

            lambda _, q=query: perform_search(q)

        )

    return RunnableParallel(**search_map)