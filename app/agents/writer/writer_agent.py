"""
Writer Agent
"""

from app.models import (
    ResearchContext,
    ResearchReport,
)

from .chain import writer_chain


class WriterAgent:
    """
    Responsible for writing
    the final report.
    """

    def write(
        self,
        context: ResearchContext,
    ) -> ResearchReport:

        report = writer_chain.invoke(

            {
                "query": context.query,
                "context": context.merged_context,
            }

        )

        source_count = sum(

    len(result["results"])

    for result in context.raw_results.values()

        )

        return ResearchReport(

        query=context.query,

        report=report,

        sources=source_count,

    )