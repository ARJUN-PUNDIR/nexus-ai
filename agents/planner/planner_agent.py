"""
Planner Agent

Responsible for generating
research search queries.
"""

from app.planner.planner_chain import planner_chain
from app.planner.planner_parser import parse_plan


class PlannerAgent:

    def plan(self, query: str) -> list[str]:
        """
        Generate search queries.
        """

        plan = planner_chain.invoke(
            {
                "query": query
            }
        )

        queries = parse_plan(plan)

        return queries