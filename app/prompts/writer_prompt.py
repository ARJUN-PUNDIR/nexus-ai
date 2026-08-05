"""
Writer Prompt
"""

from langchain_core.prompts import ChatPromptTemplate


writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional research writer.

Use ONLY the provided research context.

If information is unavailable,
say that it was not found.

Generate a report using Markdown.

Structure:

# Introduction

# Key Findings

# Detailed Explanation

# Conclusion
            """,
        ),
        (
            "human",
            """
User Query:

{query}


Research Context:

{context}
            """,
        ),
    ]
)