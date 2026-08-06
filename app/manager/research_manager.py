"""
Research Manager

Coordinates the complete research workflow.
"""

from app.agents.planner import PlannerAgent
from app.agents.research import ResearchAgent
from app.agents.writer import WriterAgent
from app.services.router import router
from app.services import save_report

from app.models import (
    ResearchReport,
)


class ResearchManager:

    """
    Main orchestrator of Nexus AI.
    """

    def __init__(self):

        self.planner = PlannerAgent()

        self.research = ResearchAgent()

        self.writer = WriterAgent()

    def run(
        self,
        query: str,
    ) -> ResearchReport:

        # -----------------------------
        # Step 1 : Decide Route
        # -----------------------------

        route = router.invoke(query)

        # -----------------------------
        # Step 2 : Research Path
        # -----------------------------

        if route["search"]:

            plan = self.planner.plan(query)

            context = self.research.research(
                plan=plan,
                query=query,
            )

            report = self.writer.write(
                context
            )

        # -----------------------------
        # Step 3 : Direct LLM Path
        # -----------------------------

        else:

            plan = self.planner.plan(query)

            context = self.research.research(
                plan=plan,
                query=query,
            )

            report = self.writer.write(
                context
            )

        save_report(
            report=report.report,
            query=query,
        )

        return report