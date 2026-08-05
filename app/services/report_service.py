"""
Report Service
"""

from pathlib import Path
from datetime import datetime

from app.config.settings import (
    REPORT_FOLDER,
)


def save_report(
    report: str,
    query: str,
) -> str:

    reports_dir = Path(REPORT_FOLDER)

    reports_dir.mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = f"research_{timestamp}.md"

    filepath = reports_dir / filename

    with open(
        filepath,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            f"# {query}\n\n"
        )

        file.write(report)

    return str(filepath)