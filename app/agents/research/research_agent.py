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
from app.tools import web_search_tool


llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=TEMPERATURE,
)


agent = create_agent(
    model=llm,
    tools=[
        web_search_tool,
    ],
    system_prompt=SYSTEM_PROMPT,
)


class ResearchAgent:

    def run(
        self,
        messages: list,
    ) -> str:

        print("\n" + "=" * 60)
        print("MESSAGES RECEIVED")
        print("=" * 60)

        for msg in messages:
            print(msg)

        print("=" * 60)

        response = agent.invoke(
            {
                "messages": messages,
            }
        )

        print("\n========== RAW RESPONSE ==========\n")

        for message in response["messages"]:
            print(type(message))
            print(message)
            print("-" * 60)

        print("\n==================================\n")

        return response["messages"][-1].content