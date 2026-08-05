"""
Query Optimizer

Improves user queries before
sending them to web search.
"""


def optimize_query(query: str) -> str:
    """
    Improves the search query.
    """

    query = query.strip()

    return (
        f"{query} "
        "Provide latest reliable information "
        "with factual sources."
    )