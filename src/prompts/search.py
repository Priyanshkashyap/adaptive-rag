"""
Prompt for web search answers.
"""

from langchain_core.prompts import ChatPromptTemplate

SEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI assistant.

Answer ONLY using the supplied web search results.

If the answer cannot be found in the search results,
say so.

Keep the answer concise.

Do not invent facts.
""",
        ),
        (
            "human",
            """
Search Results:

{context}

Question:

{question}
""",
        ),
    ]
)