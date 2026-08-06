"""
Research Manager
"""

from app.agents import ResearchAgent
from app.services import save_report


class ResearchManager:

    def __init__(self):

        self.agent = ResearchAgent()

    def run(
        self,
        query: str,
    ) -> str:

        try:

            report = self.agent.run(query)

        except Exception as e:

            raise RuntimeError(
                f"Research Agent Failed : {e}"
            )

        try:

            save_report(
                report=report,
                query=query,
            )

        except Exception as e:

            raise RuntimeError(
                f"Report Saving Failed : {e}"
            )

        return report