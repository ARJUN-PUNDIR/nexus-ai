"""
Nexus AI

Entry Point
"""

from app.manager import ResearchManager


def main():

    print("=" * 60)
    print(" " * 22 + "NEXUS AI")
    print("=" * 60)

    manager = ResearchManager()

    while True:

        query = input(
            "\nEnter Research Query (or 'exit'): "
        ).strip()

        if query.lower() in {
            "exit",
            "quit",
        }:
            print("\nGoodbye!\n")
            break

        if not query:
            print("\nQuery cannot be empty.")
            continue

        try:

            report = manager.run(query)

            print("\n")
            print("=" * 60)
            print("FINAL REPORT")
            print("=" * 60)

            print(report.report)

            print("\n")
            print("=" * 60)
            print(f"Sources Used : {report.sources}")
            print("=" * 60)

        except Exception as error:

            print("\nAn error occurred.\n")

            print(error)


if __name__ == "__main__":
    main()