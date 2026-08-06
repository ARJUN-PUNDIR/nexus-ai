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

        report = self.agent.run(query)

        save_report(
            report=report,
            query=query,
        )

        return report