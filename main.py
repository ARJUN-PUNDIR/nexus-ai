"""
Lecture 1

Entry point of the Nexus AI project.

Today's objective:
1. Load project configuration.
2. Create an Ollama LLM.
3. Send a prompt.
4. Print the response.
"""

from langchain_ollama import ChatOllama

from app.config.settings import OLLAMA_MODEL
print("Hello Arjun")

def main():
    """
    Application entry point.
    """

    # Create the language model
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0
    )

    # Send a prompt
    response = llm.invoke(
        "Introduce yourself in exactly three lines."
    )

    print("\n========== LLM RESPONSE ==========\n")

    # response is an AIMessage object.
    # The actual text is inside .content
    print(response.content)

    print("\n==================================\n")


if __name__ == "__main__":
    main()