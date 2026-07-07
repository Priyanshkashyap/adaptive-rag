"""
Prompt for query rewriting.
"""

from langchain_core.prompts import ChatPromptTemplate


REWRITE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Rewrite the question to improve retrieval.

Do not answer.

Return ONLY the rewritten query.
""",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)