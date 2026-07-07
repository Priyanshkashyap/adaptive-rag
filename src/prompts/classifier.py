"""
Prompt for query classification.
"""
from langchain_core.prompts import ChatPromptTemplate

CLASSIFIER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Classify the user query.

Return ONLY one word.

Choices:

INDEX
GENERAL
SEARCH

INDEX:
Questions about uploaded documents.

GENERAL:
General knowledge.

SEARCH:
Current events or information requiring the internet.
""",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)