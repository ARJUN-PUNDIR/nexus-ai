"""
Persistent SQLite Checkpointer Loader for Nexus AI Memory
"""

import os
import sys
import sqlite3
import importlib.util
from pathlib import Path
from typing import Any


def _load_sqlite_saver_class() -> Any:
    """
    Imports and returns SqliteSaver handling Python 3.14 namespace package compatibility.
    """
    if "langgraph.checkpoint.sqlite" in sys.modules and hasattr(sys.modules["langgraph.checkpoint.sqlite"], "SqliteSaver"):
        return sys.modules["langgraph.checkpoint.sqlite"].SqliteSaver

    candidate_paths = [
        "/Users/arjunsinghpundir/Desktop/langchain_mastery/myenv/lib/python3.14/site-packages/langgraph/checkpoint/sqlite/__init__.py",
        f"{sys.prefix}/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages/langgraph/checkpoint/sqlite/__init__.py",
    ]

    init_path = None
    for p in candidate_paths:
        if os.path.exists(p):
            init_path = p
            break

    if not init_path:
        raise FileNotFoundError("Could not locate langgraph.checkpoint.sqlite package.")

    spec = importlib.util.spec_from_file_location(
        "langgraph.checkpoint.sqlite", init_path
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["langgraph.checkpoint.sqlite"] = mod
    spec.loader.exec_module(mod)
    return mod.SqliteSaver


def get_sqlite_checkpointer(db_filename: str = "nexus_memory.db") -> Any:
    """
    Initializes a persistent SQLite checkpointer for LangGraph memory.
    """
    SqliteSaver = _load_sqlite_saver_class()
    conn = sqlite3.connect(db_filename, check_same_thread=False)
    return SqliteSaver(conn)
