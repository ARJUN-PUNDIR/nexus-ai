"""
Project Configuration

This file stores all configurable values used across the project.

If a configuration changes in the future (for example changing
the LLM model), we only update this file.
"""

"""
Project Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

TEMPERATURE = float(
    os.getenv("TEMPERATURE", "0")
)

APP_NAME = os.getenv(
    "APP_NAME",
    "Nexus AI"
)
TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY"
)