"""
Query Mapper

Converts a validated string into the
dictionary expected by ChatPromptTemplate.
"""


def map_query(query: str) -> dict:

    return {
        "query": query
    }