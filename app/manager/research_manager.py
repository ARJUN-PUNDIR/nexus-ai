"""
Research Manager
"""

from app.agents import ResearchAgent


class ResearchManager:

    def __init__(self):

        self.agent = ResearchAgent()

        # One session for now
        self.thread_id = "user_1"

    def run(
        self,
        query: str,
    ) -> str:

        return self.agent.run(
            query=query,
            thread_id=self.thread_id,
        )