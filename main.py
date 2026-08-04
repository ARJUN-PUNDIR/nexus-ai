# """
# Lecture 5B

# Nexus AI
# LCEL Research Chain
# """

# from app.chains.research_chain import research_chain


# def main():

#     print("=" * 50)
#     print("              NEXUS AI")
#     print("=" * 50)

#     query = input("\nEnter Research Query : ")

#     response = research_chain.invoke(
#         {
#             "query": query
#         }
#     )

#     print("\n========== RESEARCH RESPONSE ==========\n")

#     print(response)

#     print("\n=======================================\n")


# if __name__ == "__main__":
#     main()

# """
# Lecture 9

# Testing Tavily Search
# """

# from app.tools.web_search import web_search
# from app.utils.query_validator import validate_query


# def main():

#     print("=" * 50)
#     print("        NEXUS AI SEARCH")
#     print("=" * 50)

#     query = input("\nEnter Search Query : ")
#     query = validate_query(query)

#     result = web_search.invoke(query)

#     print("\n========== SEARCH RESULTS ==========\n")

#     print(result)

#     print("\n====================================\n")


# if __name__ == "__main__":
#     main()

"""
Lecture 11

Nexus AI
Research Pipeline
"""

from app.chains.research_pipeline import research_pipeline


def main():

    print("=" * 50)
    print("              NEXUS AI")
    print("=" * 50)

    query = input("\nEnter Research Query : ")

    try:

        response = research_pipeline.invoke(query)

        print("\n========== RESEARCH RESPONSE ==========\n")

        print(response)

        print("\n=======================================\n")

    except ValueError as error:

        print(f"\nError : {error}")


if __name__ == "__main__":
    main()