"""
Tests for Report Service
"""

from pathlib import Path

from app.services.report_service import (
    save_report
)


def test_report_creation():

    report = save_report(

        query="Test",

        report="Hello World"

    )

    assert Path(report).exists()