"""
Application Settings
"""

import os

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:4b"
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

# ---------------------------------------------------------
# Tavily
# ---------------------------------------------------------

TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY"
)

# ---------------------------------------------------------
# Research
# ---------------------------------------------------------

MAX_SEARCH_RESULTS = 3

MAX_PLANNER_QUERIES = 3

TEMPERATURE = 0

# ---------------------------------------------------------
# Report
# ---------------------------------------------------------

REPORT_FOLDER = "reports"