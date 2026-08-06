"""
Research Agent

Modern LangChain Agent
"""

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from app.prompts import SYSTEM_PROMPT
from app.config.settings import (
    OLLAMA_MODEL,
    OLLAMA_BASE_URL,
    TEMPERATURE,
)

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=TEMPERATURE,
)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=SYSTEM_PROMPT,
)


class ResearchAgent:

    def run(
        self,
        query: str,
    ) -> str:

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query,
                    }
                ]
            }
        )

        return response["messages"][-1].content