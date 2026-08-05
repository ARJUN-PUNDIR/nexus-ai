"""
Tests for Search Formatter
"""

from app.services.search_formatter import (
    format_search_results
)


def test_formatter():

    sample_data = {

        "results": [

            {

                "title": "LangChain",

                "content": "Framework",

                "url": "https://langchain.com"

            }

        ]

    }

    context, sources = format_search_results(
        sample_data
    )

    assert "LangChain" in context

    assert len(sources) == 1

    assert sources[0] == "https://langchain.com"