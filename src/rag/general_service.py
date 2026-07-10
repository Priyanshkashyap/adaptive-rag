"""
General knowledge answering service.
"""
from langchain_core.messages import AIMessage
from src.core.logger import logger
from src.llms.ollama_client import get_llm
from src.models.query_result import QueryResult
from src.prompts.general import GENERAL_PROMPT

def answer_general_question(question: str,) -> QueryResult:
    """
    Answer a general knowledge question using the LLM.

    Args:
        question:
            User question.

    Returns:
        Generated answer.
    """
    logger.info("Running general LLM query.",)
    llm = get_llm()
    chain = GENERAL_PROMPT | llm
    response = chain.invoke(
        {
            "question": question,
        }
    )

    if not isinstance(response, AIMessage):
        raise TypeError("Expected AIMessage from LLM.")

    if isinstance(response.content, str):
        answer = response.content
    else:
        answer = "\n".join(
            str(part)
            for part in response.content #either list or string replied by llm
        )

    return QueryResult(
        answer=answer,
        source_count=0,
        confidence=1.0,
        sources=[],
    )