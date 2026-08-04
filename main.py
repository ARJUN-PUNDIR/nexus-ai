"""
Lecture 5B

Nexus AI
LCEL Research Chain
"""

from app.chains.research_chain import research_chain


def main():

    print("=" * 50)
    print("              NEXUS AI")
    print("=" * 50)

    query = input("\nEnter Research Query : ")

    response = research_chain.invoke(
        {
            "query": query
        }
    )

    print("\n========== RESEARCH RESPONSE ==========\n")

    print(response)

    print("\n=======================================\n")


if __name__ == "__main__":
    main()