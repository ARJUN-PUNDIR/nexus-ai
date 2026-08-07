"""
Centralized Model Factory for Nexus AI
Instantiates LLM models and Embedding models based on settings.py configuration.
"""

from typing import Any
from app.config.settings import (
    LLM_PROVIDER,
    LLM_MODEL_NAME,
    TEMPERATURE,
    OLLAMA_BASE_URL,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    EMBEDDING_PROVIDER,
    EMBEDDING_MODEL_NAME,
)


def get_llm() -> Any:
    """
    Factory function returning the configured Chat LLM instance.
    Supports: Ollama (Default), OpenAI, Anthropic Claude.
    """
    provider = LLM_PROVIDER.lower().strip()

    if provider == "openai":
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=LLM_MODEL_NAME if "gpt" in LLM_MODEL_NAME else "gpt-4o-mini",
                temperature=TEMPERATURE,
                api_key=OPENAI_API_KEY,
            )
        except ImportError:
            raise ImportError("langchain-openai package required for OpenAI. Run: pip install langchain-openai")

    elif provider == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=LLM_MODEL_NAME if "claude" in LLM_MODEL_NAME else "claude-3-5-sonnet-20241022",
                temperature=TEMPERATURE,
                api_key=ANTHROPIC_API_KEY,
            )
        except ImportError:
            raise ImportError("langchain-anthropic package required for Anthropic. Run: pip install langchain-anthropic")

    else:
        # Default: Local Ollama
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=LLM_MODEL_NAME,
            base_url=OLLAMA_BASE_URL,
            temperature=TEMPERATURE,
        )


def get_embedding_model() -> Any:
    """
    Factory function returning the configured Embedding model instance.
    Supports: HuggingFace (Local), Ollama, OpenAI.
    """
    provider = EMBEDDING_PROVIDER.lower().strip()

    if provider == "openai":
        try:
            from langchain_openai import OpenAIEmbeddings
            return OpenAIEmbeddings(
                model=EMBEDDING_MODEL_NAME if "text-embedding" in EMBEDDING_MODEL_NAME else "text-embedding-3-small",
                api_key=OPENAI_API_KEY,
            )
        except ImportError:
            raise ImportError("langchain-openai package required for OpenAI embeddings.")

    elif provider == "ollama":
        try:
            from langchain_ollama import OllamaEmbeddings
            return OllamaEmbeddings(
                model=EMBEDDING_MODEL_NAME if EMBEDDING_MODEL_NAME != "sentence-transformers/all-MiniLM-L6-v2" else "nomic-embed-text",
                base_url=OLLAMA_BASE_URL,
            )
        except ImportError:
            raise ImportError("langchain-ollama package required for Ollama embeddings.")

    else:
        # Default: Local HuggingFace or Ollama fallback
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        except ImportError:
            try:
                from langchain_community.embeddings import HuggingFaceEmbeddings
                return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
            except (ImportError, Exception):
                from langchain_ollama import OllamaEmbeddings
                return OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
