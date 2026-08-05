"""
Search Formatter

Converts Tavily response
into clean context.
"""


def format_search_results(results):

    formatted_text = ""

    for index, result in enumerate(results["results"], start=1):

        formatted_text += f"""
Source {index}

Title:
{result['title']}

Content:
{result['content']}

URL:
{result['url']}

----------------------------------------

"""

    return formatted_text