"""
Unit tests for Centralized Model Factory and Settings
"""

from unittest.mock import patch
from app.config.model_factory import get_llm, get_embedding_model


def test_get_llm_ollama_default():
    llm = get_llm()
    assert llm is not None


@patch("app.config.model_factory.LLM_PROVIDER", "openai")
@patch("app.config.model_factory.OPENAI_API_KEY", "sk-test-key")
def test_get_llm_openai():
    try:
        llm = get_llm()
        assert llm is not None
    except ImportError:
        pass


@patch("app.config.model_factory.EMBEDDING_PROVIDER", "ollama")
def test_get_embedding_model_ollama():
    embeddings = get_embedding_model()
    assert embeddings is not None
