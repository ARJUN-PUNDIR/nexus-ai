"""
Context Merger Service
"""

from .search_formatter import (
    format_search_results,
)


def merge_results(
    search_results: dict,
) -> str:

    merged_context = ""

    for search_name, result in search_results.items():

        merged_context += f"""

{"=" * 60}

{search_name.upper()}

{"=" * 60}

"""

        merged_context += format_search_results(
            result
        )

    return merged_context