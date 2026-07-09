"""
Query classification service.
"""
from src.core.logger import logger
from src.llms.ollama_client import get_llm
from src.models.route_identifier import RouteIdentifier
from src.prompts.classifier import CLASSIFIER_PROMPT
from typing import cast

def classify_query(question: str,) -> RouteIdentifier:
    """
    Classify the query.

    Args:
        question:
            User question.

    Returns:
        Predicted route.
    """
    logger.info("Classifying query.")
    llm = get_llm()

    structured_llm = llm.with_structured_output(RouteIdentifier,)
    chain = (CLASSIFIER_PROMPT | structured_llm)

    result = cast(RouteIdentifier,chain.invoke( # type casting
        {
            "question": question,
        }
    ),
)
    logger.info("Predicted route=%s",result.route,) # results in route identifier result of a classification
    return result

   