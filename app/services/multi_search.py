"""
Multi Search Service
"""

from app.tools.web_search import web_search


def search_gpt(query: str):

    return web_search.invoke(
        {
            "query": f"{query} GPT"
        }
    )


def search_claude(query: str):

    return web_search.invoke(
        {
            "query": f"{query} Claude"
        }
    )


def search_general(query: str):

    return web_search.invoke(
        {
            "query": query
        }
    )