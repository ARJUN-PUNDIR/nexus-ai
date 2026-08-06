"""
Query Expander

Expands a user query into multiple
search queries using an LLM.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama

from app.config.settings import (
    OLLAMA_MODEL,
    OLLAMA_BASE_URL,
    TEMPERATURE,
)

# -----------------------------
# LLM
# -----------------------------

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=TEMPERATURE,
)

# -----------------------------
# Prompt
# -----------------------------

prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
You expand search queries.

Generate 3 different search queries.

Rules:

1. Keep them short.

2. Cover different aspects.

3. Return ONLY valid JSON.

Example:

{{
    "queries":[
        "...",
        "...",
        "..."
    ]
}}
            """

        ),

        (

            "human",

            "{query}"

        ),

    ]

)

# -----------------------------
# Chain
# -----------------------------

chain = (

    prompt

    |

    llm

    |

    JsonOutputParser()

)

# -----------------------------
# Public Function
# -----------------------------


def expand_query(
    query: str,
) -> list[str]:

    result = chain.invoke(

        {

            "query": query,

        }

    )

    return result["queries"]