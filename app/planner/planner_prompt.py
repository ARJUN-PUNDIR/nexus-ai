from langchain_core.prompts import ChatPromptTemplate

planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a research planner.

Break the user's research request into
3 independent web search queries.

Return ONLY the search queries.

One query per line.
- Do not explain anything.

"""
        ),

        (
            "human",
            "{query}"
        )
    ]
)