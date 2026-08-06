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

        print("\n========== RAW RESPONSE ==========\n")

        for message in response["messages"]:
            print(type(message))
            print(message)
            print("-" * 60)

        print("\n==================================\n")

        return response["messages"][-1].content