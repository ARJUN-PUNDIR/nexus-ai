"""
Query Router

Decides whether a web search
is required.
"""

from langchain_core.runnables import RunnableBranch


def needs_web_search(query: str) -> bool:
    """
    Simple routing logic.

    Returns True if web search is needed.
    """

    query = query.lower()

    keywords = [

        "today",

        "latest",

        "current",

        "news",

        "price",

        "stock",

        "weather",

        "2026",

        "recent",

    ]

    return any(

        word in query

        for word in keywords

    )


router = RunnableBranch(

    (
        needs_web_search,

        lambda query: {

            "query": query,

            "search": True,

        },

    ),

    lambda query: {

        "query": query,

        "search": False,

    },

)