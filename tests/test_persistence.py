"""
Unit tests for Persistent SQLite Checkpointer Memory
"""

import os
from app.utils.memory_saver import get_sqlite_checkpointer


def test_sqlite_checkpointer_initialization(tmp_path):
    test_db = str(tmp_path / "test_memory.db")
    checkpointer = get_sqlite_checkpointer(test_db)

    assert os.path.exists(test_db)
    assert checkpointer is not None
