"""
Search Formatter
"""


def format_search_results(results):

    formatted_context = ""

    sources = []

    for index, result in enumerate(results["results"], start=1):

        formatted_context += f"""
Source {index}

Title:
{result['title']}

Content:
{result['content']}

----------------------------------------

"""

        sources.append(result["url"])

    return formatted_context, sources