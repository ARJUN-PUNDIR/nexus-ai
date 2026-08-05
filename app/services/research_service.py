"""
Research Service

Responsible for preparing
research context.
service isko prompt ke form mai bhi convert kar rhi hai 
"""

from app.tools.web_search import web_search
from app.services.search_formatter import format_search_results
from app.services.query_optimizer import optimize_query
def build_context(query: str):
    optimized_query = optimize_query(query)

    results = web_search.invoke(
    {
        "query": query
    }
    )

    formatted_context = format_search_results(results)

    return {
        "query": query,
        "context": formatted_context
    }