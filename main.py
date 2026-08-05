"""
Debug Version

This file prints every step of the project.
"""

from app.planner.planner_chain import planner_chain
from app.planner.planner_parser import parse_plan

from app.services.parallel_search import (
    build_parallel_search
)

from app.services.context_merger import (
    merge_search_results
)

from app.chains.research_pipeline import (
    research_pipeline
)

from app.services.report_service import (
    save_report
)


def main():

    print("=" * 60)
    print("               NEXUS AI (DEBUG MODE)")
    print("=" * 60)

    query = input("\nEnter Research Query : ")

    # -------------------------------------------------
    # STEP 1
    # -------------------------------------------------

    print("\n")
    print("=" * 60)
    print("STEP 1 : USER QUERY")
    print("=" * 60)

    print(query)

    # -------------------------------------------------
    # STEP 2
    # -------------------------------------------------

    print("\n")
    print("=" * 60)
    print("STEP 2 : PLANNER OUTPUT")
    print("=" * 60)

    plan = planner_chain.invoke(
        {
            "query": query
        }
    )

    print(plan)

    # -------------------------------------------------
    # STEP 3
    # -------------------------------------------------

    # print("\n")
    # print("=" * 60)
    # print("STEP 3 : PARSED PLAN")
    # print("=" * 60)

    # queries = parse_plan(plan)

    # print(queries)

    # # -------------------------------------------------
    # # STEP 4
    # # -------------------------------------------------

    # print("\n")
    # print("=" * 60)
    # print("STEP 4 : RUNNING PARALLEL SEARCH")
    # print("=" * 60)

    # parallel = build_parallel_search(
    #     queries
    # )

    # search_results = parallel.invoke(None)

    # print(search_results)

    # # -------------------------------------------------
    # # STEP 5
    # # -------------------------------------------------

    # print("\n")
    # print("=" * 60)
    # print("STEP 5 : MERGED CONTEXT")
    # print("=" * 60)

    # merged_context = merge_search_results(
    #     search_results
    # )

    # print(merged_context)

    # # -------------------------------------------------
    # # STEP 6
    # # -------------------------------------------------

    # print("\n")
    # print("=" * 60)
    # print("STEP 6 : FINAL LLM REPORT")
    # print("=" * 60)

    # report = research_pipeline.invoke(query)

    # print(report)

    # # -------------------------------------------------
    # # STEP 7
    # # -------------------------------------------------

    # print("\n")
    # print("=" * 60)
    # print("STEP 7 : SAVING REPORT")
    # print("=" * 60)

    # report_path = save_report(
    #     query=query,
    #     report=report
    # )

    # print("Saved At :")
    # print(report_path)

    # print("\n")
    # print("=" * 60)
    # print("PROJECT FINISHED")
    # print("=" * 60)w


if __name__ == "__main__":
    main()