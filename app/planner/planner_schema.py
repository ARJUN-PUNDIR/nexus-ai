"""
Planner Schema
"""

from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    """
    Planner Output Schema
    """

    queries: list[str] = Field(
        description="Exactly three search queries."
    )