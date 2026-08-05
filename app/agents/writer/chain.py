"""
Writer Chain
"""

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from app.prompts import writer_prompt

from app.config.settings import (
    OLLAMA_MODEL,
    OLLAMA_BASE_URL,
    TEMPERATURE,
)


writer_chain = (

    writer_prompt

    |

    ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=TEMPERATURE,
    )

    |

    StrOutputParser()

)