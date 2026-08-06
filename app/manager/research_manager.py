"""
Research Manager
"""

from app.graph import graph


class ResearchManager:

    def run(
        self,
        query: str,
    ) -> str:

        result = graph.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query,
                    }
                ]
            }
        )

        return result["messages"][-1]["content"]