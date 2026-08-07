"""
Token-Efficient Conversation Memory Summarizer for Nexus AI
"""

from typing import Any
from langchain_core.messages import SystemMessage
from app.graph.state import AgentState
from app.config import get_llm


llm = get_llm()

SYSTEM_PROMPT = """You are Nexus AI, an autonomous multi-agent research assistant.
You have stateful conversational memory. Always remember user details, facts, and context from previous turns in the conversation thread."""


def prepare_summarized_messages(state: AgentState) -> tuple[list[Any], str]:
    """
    Helper function for Token-Efficient Memory:
    1. If message history > 6 messages, condenses older turns into a 2-3 sentence running summary.
    2. Keeps only the 4 most recent raw messages.
    3. Combines System Prompt + Running Summary + Recent Messages to keep token usage low.
    """
    messages = list(state.get("messages", []))
    existing_summary = state.get("summary", "")

    if len(messages) > 6:
        print("\n🧠 [MEMORY] Summarizing older conversation turns to save tokens...")
        older_messages = messages[:-4]
        older_text = "\n".join(f"{getattr(m, 'type', 'user')}: {getattr(m, 'content', '')}" for m in older_messages)

        summarize_prompt = f"""Summarize key user details, names, and research topics from this conversation into a concise 2-3 sentence summary.

Previous Summary: {existing_summary}
Conversation History:
{older_text}

Output ONLY the updated 2-3 sentence summary:"""

        try:
            new_summary = llm.invoke(summarize_prompt).content.strip()
            print(f"   └─ ✅ Compact Summary: '{new_summary}'")
        except Exception:
            new_summary = existing_summary
    else:
        new_summary = existing_summary

    system_text = SYSTEM_PROMPT
    if new_summary:
        system_text += f"\n\n--- Running Summary of Previous Conversation ---\n{new_summary}"

    recent_messages = messages[-4:] if len(messages) > 4 else messages
    prompt_sequence = [SystemMessage(content=system_text)] + recent_messages

    return prompt_sequence, new_summary
