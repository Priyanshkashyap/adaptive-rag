"""
LangGraph routing nodes.
"""

from src.core.logger import logger
from src.graph.state import AdaptiveRAGState

from src.rag.general_service import answer_general_question
from src.rag.query_classifier import classify_query
from src.rag.search_service import answer_from_search


def classify_node(
    state: AdaptiveRAGState,
) -> AdaptiveRAGState:
    """
    Classify the incoming question.
    """

    logger.info(
        "Running classifier node.",
    )

    route = classify_query(
        state["question"],
    )

    state["route"] = route.route

    return state


def general_node(
    state: AdaptiveRAGState,
) -> AdaptiveRAGState:
    """
    Answer a general knowledge question.
    """

    logger.info(
        "Running general node.",
    )

    result = answer_general_question(
        state["question"],
    )

    state["answer"] = result.answer
    state["confidence"] = result.confidence
    state["source_count"] = result.source_count
    state["sources"] = result.sources

    return state


def search_node(
    state: AdaptiveRAGState,
) -> AdaptiveRAGState:
    """
    Answer using Tavily search.
    """

    logger.info(
        "Running search node.",
    )

    result = answer_from_search(
        state["question"],
    )

    state["answer"] = result.answer
    state["confidence"] = result.confidence
    state["source_count"] = result.source_count
    state["sources"] = result.sources

    return state