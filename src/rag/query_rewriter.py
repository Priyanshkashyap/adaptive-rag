"""
Query rewriting service.
"""
from langchain_core.messages import AIMessage
from src.core.logger import logger
from src.llms.ollama_client import get_llm
from src.prompts.rewrite import REWRITE_PROMPT

def rewrite_query(question: str,) -> str:
    """
    Rewrite the question to improve retrieval.

    Args:
        question:
            Original question.

    Returns:
        Rewritten query.
    """
    logger.info("Rewriting query.")
    llm = get_llm()
    chain = REWRITE_PROMPT | llm

    response = chain.invoke(
        {
            "question": question,
        }
    )
    if not isinstance(response,AIMessage,):
        raise TypeError(
            "Expected AIMessage."
        )

    if isinstance(response.content,str,):
        return response.content.strip()

    return "\n".join(
        str(part)
        for part in response.content
    ).strip()