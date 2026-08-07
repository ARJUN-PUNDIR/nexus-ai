"""
Nexus AI Configuration Package
"""

from .settings import (
    TAVILY_API_KEY,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    REPORT_FOLDER,
    OLLAMA_BASE_URL,
    LLM_PROVIDER,
    LLM_MODEL_NAME,
    TEMPERATURE,
    EMBEDDING_PROVIDER,
    EMBEDDING_MODEL_NAME,
)
from .model_factory import get_llm, get_embedding_model

__all__ = [
    "TAVILY_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "REPORT_FOLDER",
    "OLLAMA_BASE_URL",
    "LLM_PROVIDER",
    "LLM_MODEL_NAME",
    "TEMPERATURE",
    "EMBEDDING_PROVIDER",
    "EMBEDDING_MODEL_NAME",
    "get_llm",
    "get_embedding_model",
]
