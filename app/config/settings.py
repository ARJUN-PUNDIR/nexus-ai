"""
Centralized Configuration & Provider Settings for Nexus AI
Secrets are loaded strictly from .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# Secret API Keys (Loaded strictly from .env)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Output Folders
REPORT_FOLDER = os.getenv("REPORT_FOLDER", "reports")

# Ollama Base Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# =====================================================================
# ⚙️ MODEL PROVIDER SELECTION
# Change provider strings below to switch models project-wide!
# =====================================================================

# LLM Provider Options: "ollama", "openai", "anthropic"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

# LLM Model Name Options:
# - Ollama: "qwen3:4b", "llama3.1:8b", "mistral:7b"
# - OpenAI: "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"
# - Anthropic: "claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"
LLM_MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:4b")

# LLM Temperature (0.0 = deterministic/factual, 0.7 = creative)
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

# Embedding Provider Options: "huggingface", "ollama", "openai"
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface")

# Embedding Model Name Options:
# - HuggingFace: "sentence-transformers/all-MiniLM-L6-v2"
# - Ollama: "nomic-embed-text", "mxbai-embed-large"
# - OpenAI: "text-embedding-3-small", "text-embedding-3-large"
EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
)