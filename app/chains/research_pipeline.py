from app.utils.runnables import query_validator, query_mapper

from app.prompts.research_prompt import research_prompt

from langchain_ollama import ChatOllama

from langchain_core.output_parsers import StrOutputParser

from app.config.settings import (
    OLLAMA_MODEL,
    TEMPERATURE
)

llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=TEMPERATURE
)

parser = StrOutputParser()

research_pipeline = (
    query_validator
    | query_mapper
    | research_prompt
    | llm
    | parser
)