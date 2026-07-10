"""
Prompt for general LLM questions.
"""
from langchain_core.prompts import ChatPromptTemplate

GENERAL_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Answer the user's question accurately.

Do not mention documents or uploaded files.

If you are unsure, clearly say so.
""",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)