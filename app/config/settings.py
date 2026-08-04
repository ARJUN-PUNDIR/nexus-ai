"""
Project Configuration

This file stores all configurable values used across the project.

If a configuration changes in the future (for example changing
the LLM model), we only update this file.
"""

import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Default model if .env is missing
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
