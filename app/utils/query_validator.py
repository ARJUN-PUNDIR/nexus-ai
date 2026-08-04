"""
Query Validator 
means kuch na likhe bina click akr dia , isse llm ko kuch bhi empty nhi jayega 
"""


def validate_query(query: str) -> str:

    query = query.strip()

    if not query:
        raise ValueError(
            "Research query cannot be empty."
        )

    return query