"""
Unit tests for Nexus AI Pydantic Data Schemas
"""

import pytest
from pydantic import ValidationError
from app.models.schemas import SearchResultItem, ResearchPlan, ResearchReport


def test_search_result_item_valid():
    item = SearchResultItem(
        title="LangGraph Documentation",
        url="https://langchain.com/langgraph",
        content="LangGraph allows building stateful multi-agent workflows.",
        source_type="web",
    )
    assert item.title == "LangGraph Documentation"
    assert item.source_type == "web"
    assert item.url == "https://langchain.com/langgraph"


def test_search_result_item_defaults():
    item = SearchResultItem(
        title="Local Document Chunk",
        content="This is extracted context from a PDF.",
    )
    assert item.url == ""
    assert item.source_type == "web"
    assert item.metadata == {}


def test_research_plan_validation():
    plan = ResearchPlan(
        original_query="What is quantum computing?",
        search_queries=[
            "Quantum computing principles",
            "Quantum superposition applications 2026",
        ],
        research_depth="deep",
    )
    assert len(plan.search_queries) == 2
    assert plan.research_depth == "deep"


def test_research_report_valid():
    report = ResearchReport(
        title="Quantum Computing Research Overview",
        executive_summary="Quantum computing leverages qubits for exponential speedups.",
        key_findings=[
            "Superposition enables parallel state evaluation.",
            "Post-quantum cryptography is becoming critical.",
        ],
        detailed_analysis="# Quantum Analysis\nFull detailed report content here.",
        sources=["https://quantum.example.com"],
        confidence_score=95,
    )
    assert report.confidence_score == 95
    assert len(report.key_findings) == 2


def test_research_report_invalid_confidence():
    with pytest.raises(ValidationError):
        ResearchReport(
            title="Test Report",
            executive_summary="Summary",
            key_findings=["Finding 1"],
            detailed_analysis="Analysis",
            confidence_score=150,  # Invalid: must be <= 100
        )
