"""
Planner Chain
"""

from langchain_ollama import ChatOllama

from app.config.settings import (
    OLLAMA_MODEL,
    OLLAMA_BASE_URL,
    TEMPERATURE,
)

from app.prompts import planner_prompt

from app.models import ResearchPlan


planner_chain = (

    planner_prompt

    |

    ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=TEMPERATURE,
    ).with_structured_output(
        ResearchPlan
    )

)