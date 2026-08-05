"""
Context Merger

Combines multiple Tavily search results
into one clean context.
"""

from app.services.search_formatter import format_search_results


def merge_search_results(results: dict) -> str:
    """
    Merge all Tavily responses into one context.
    """

    merged_context = ""

    for search_name, search_result in results.items():

        merged_context += f"\n{'=' * 60}\n"
        merged_context += f"{search_name.upper()}\n"
        merged_context += f"{'=' * 60}\n\n"

        formatted_context, _ = format_search_results(search_result)

        merged_context += formatted_context
        merged_context += "\n"

    return merged_context