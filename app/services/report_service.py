"""
Report Service

Responsible for saving research reports.
"""

from pathlib import Path
from datetime import datetime


def save_report(query: str, report: str):

    # Reports folder
    reports_folder = Path("reports")

    reports_folder.mkdir(exist_ok=True)

    # File name using current date & time
    filename = datetime.now().strftime(
        "research_%Y%m%d_%H%M%S.md"
    )

    report_file = reports_folder / filename

    content = f"""# Nexus AI Research Report

## Research Query

{query}

---

## Report

{report}
"""

    report_file.write_text(
        content,
        encoding="utf-8"
    )

    return report_file