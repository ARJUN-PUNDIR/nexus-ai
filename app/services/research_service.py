"""
Research Service

Responsible for preparing
research context.
service isko prompt ke form mai bhi convert kar rhi hai 
"""

from app.tools.web_search import web_search


def build_context(query: str):

    results = web_search.invoke(
        {
            "query": query
        }
    )

    return {
        "query": query,
        "context": results
    }