from langchain_core.prompts import ChatPromptTemplate

research_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are Nexus AI.

You MUST answer ONLY using the information provided in the Context.

Rules:

1. Never use your own knowledge.
2. If the answer exists in the Context, use it.
3. If the Context does not contain the answer, say:
"I could not find this information in the search results."
"""
        ),

        (
            "human",
            """
Question:

{query}

Context:

{context}
"""
        )
    ]
)