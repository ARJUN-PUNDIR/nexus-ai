"""
Planner Chain
"""

from langchain_ollama import ChatOllama

from app.config.settings import OLLAMA_MODEL

from app.planner.planner_prompt import (
    planner_prompt
)

from app.planner.planner_schema import (
    ResearchPlan
)

planner_chain = (

    planner_prompt

    |

    ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0
    ).with_structured_output(
        ResearchPlan
    )

)