"""
Web Search Tool
"""

from typing import Annotated

from langchain.tools import tool
from langchain_tavily import TavilySearch

from app.config.settings import TAVILY_API_KEY


search = TavilySearch(
    tavily_api_key=TAVILY_API_KEY,
    max_results=5,
)


@tool
def web_search_tool(
    query: Annotated[
        str,
        "Search query requiring internet access.",
    ],
) -> str:
    """
    Search the internet and return useful context.
    """

    response = search.invoke(
        {
            "query": query,
        }
    )

    context = []

    for result in response["results"]:

        context.append(
            f"Title: {result['title']}"
        )

        context.append(
            f"Content: {result['content']}"
        )

        context.append("")

    return "\n".join(context)