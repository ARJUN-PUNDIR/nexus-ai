"""
Planner Output Parser
"""


def parse_plan(plan: str) -> list[str]:
    """
    Converts planner output into a list.
    """

    queries = []

    for line in plan.split("\n"):

        line = line.strip()

        if line:
            queries.append(line)

    return queries