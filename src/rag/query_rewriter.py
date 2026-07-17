"""
Query rewriting service.
"""

from langchain_core.messages import AIMessage

from src.core.logger import logger
from src.llms.groq_client import get_llm
from src.prompts.rewrite import REWRITE_PROMPT


def rewrite_query(
    question: str,
) -> str:
    """
    Rewrite the question to improve retrieval.

    Args:
        question:
            Original question.

    Returns:
        Rewritten query.
    """

    try:

        logger.info(
            "Rewriting query."
        )

        llm = get_llm()

        chain = (
            REWRITE_PROMPT
            | llm
        )

        response = chain.invoke(
            {
                "question": question,
            }
        )

        if not isinstance(
            response,
            AIMessage,
        ):
            raise TypeError(
                "Expected AIMessage."
            )

        if isinstance(
            response.content,
            str,
        ):
            rewritten_query = response.content.strip()

        else:
            rewritten_query = "\n".join(
                str(part)
                for part in response.content
            ).strip()

        logger.info(
            "Query rewritten successfully."
        )

        return rewritten_query

    except Exception:

        logger.exception(
            "Query rewriting failed."
        )

        raise