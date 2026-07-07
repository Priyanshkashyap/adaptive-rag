"""
Prompt for retrieval grading.
"""

from langchain_core.prompts import ChatPromptTemplate


GRADER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You evaluate retrieved documents.

Determine whether the retrieved context is useful.

Return ONLY:

YES

or

NO
""",
        ),
        (
            "human",
            """
Question:

{question}

Retrieved Context:

{context}
""",
        ),
    ]
)