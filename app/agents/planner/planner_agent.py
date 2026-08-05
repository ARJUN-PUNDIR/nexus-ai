"""
Planner Agent
"""

from app.models import ResearchPlan

from .chain import planner_chain


class PlannerAgent:
    """
    Responsible for creating
    a research plan.
    """

    def plan(
        self,
        query: str,
    ) -> ResearchPlan:

        return planner_chain.invoke(
            {
                "query": query
            }
        )