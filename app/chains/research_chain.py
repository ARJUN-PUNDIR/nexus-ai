"""
Research Chain

This file connects the prompt,
LLM and output parser.
"""

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from app.config.settings import OLLAMA_MODEL
from app.prompts.research_prompt import research_prompt

llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0
)

parser = StrOutputParser()

research_chain = research_prompt | llm | parser