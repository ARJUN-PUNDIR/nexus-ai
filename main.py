"""
Nexus AI - Autonomous Multi-Agent Research Platform Entry Point
"""

import sys
from app.manager import ResearchManager


def print_banner():
    banner = """
=================================================================
                 🤖 NEXUS AI RESEARCH PLATFORM 🤖
          Autonomous Multi-Agent Stateful Workflow Engine
=================================================================
"""
    print(banner)


def main():
    print_banner()
    manager = ResearchManager()

    while True:
        try:
            query = input("\n👉 Enter Research Query (or 'exit' to quit): ").strip()

            if query.lower() in {"exit", "quit"}:
                print("\n👋 Exiting Nexus AI. Happy researching!\n")
                sys.exit(0)

            if not query:
                print("⚠️ Query cannot be empty. Please enter a research topic.")
                continue

            # Run Multi-Agent Graph Workflow
            final_report = manager.run(query)

            # Display Final Formatted Report
            print("\n" + "=" * 65)
            print("                📄 FINAL GENERATED RESEARCH REPORT")
            print("=" * 65 + "\n")
            print(final_report)
            print("=" * 65)

        except KeyboardInterrupt:
            print("\n\n👋 Process interrupted by user. Goodbye!")
            sys.exit(0)
        except Exception as error:
            print(f"\n❌ An error occurred during graph execution:\n{error}\n")


if __name__ == "__main__":
    main()