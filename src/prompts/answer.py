"""
Prompt for answer generation.
"""
from langchain_core.prompts import ChatPromptTemplate #Its job is to build prompts that look like a conversation.

ANSWER_PROMPT = ChatPromptTemplate.from_messages( # This creates a prompt template from multiple chat messages so make llm understand better
    [
        (
            "system",
            """
You are an expert AI assistant.
Answer ONLY using the provided context.
If the answer cannot be found in the context,
reply:
"I could not find the answer in the provided documents."
Keep answers concise.
Always cite relevant information from the supplied context.
""",
        ),
        (
            "human",
            """
Context:
{context}
Question:
{question}
""",
        ),
    ]
)