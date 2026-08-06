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

                "messages":[

                    {

                        "role":"user",

                        "content":query,

                    }

                ]

            },

            config={

                "configurable":{

                    "thread_id":"user_1",

                }

            }

        )
        return result["messages"][-1]["content"]