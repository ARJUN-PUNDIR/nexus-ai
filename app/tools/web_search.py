"""
Web Search Tool

Uses Tavily Search API.
"""

from langchain_core.tools import tool
from tavily import TavilyClient
from app.config.settings import TAVILY_API_KEY
client = TavilyClient(api_key=TAVILY_API_KEY)

@tool
def web_search(query: str) -> str:
    """
    Search the web and return relevant information.
    """

    response = client.search(
        query=query,
        max_results=3
    )

    return str(response)