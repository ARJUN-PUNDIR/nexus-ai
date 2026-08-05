"""
Search Formatter Service
"""


def format_search_results(
    results: dict,
) -> str:

    formatted = ""

    for index, result in enumerate(
        results["results"],
        start=1,
    ):

        formatted += f"""

Source {index}

Title:
{result["title"]}

Content:
{result["content"]}

URL:
{result["url"]}

{"-" * 60}

"""

    return formatted