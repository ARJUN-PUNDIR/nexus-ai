"""
Web Search Tool

Uses Tavily Search API.
"""

from langchain_tavily import TavilySearch

from app.config.settings import (
    TAVILY_API_KEY,
    MAX_SEARCH_RESULTS,
)


web_search = TavilySearch(
    max_results=MAX_SEARCH_RESULTS,
    topic="general",
    tavily_api_key=TAVILY_API_KEY,
)