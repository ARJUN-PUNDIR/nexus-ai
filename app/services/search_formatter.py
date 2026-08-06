"""
Search Formatter Service
"""

from typing import Any


def format_search_results(
    results: dict[str, Any],
) -> tuple[str, list[str]]:
    """
    Format search results into context string and extract sources list.
    """
    formatted = ""
    sources = []

    for index, result in enumerate(
        results.get("results", []),
        start=1,
    ):
        title = result.get("title", "")
        content = result.get("content", "")
        url = result.get("url", "")

        if url:
            sources.append(url)

        formatted += f"""
Source {index}

Title:
{title}

Content:
{content}

URL:
{url}

{"-" * 60}
"""

    return formatted, sources