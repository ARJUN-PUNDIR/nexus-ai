from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from app.config.settings import (
    OLLAMA_MODEL,
    TEMPERATURE
)

from app.planner.planner_prompt import (
    planner_prompt
)

planner_chain = (

    planner_prompt

    |

    ChatOllama(

        model=OLLAMA_MODEL,

        temperature=TEMPERATURE

    )

    |

    StrOutputParser()

)