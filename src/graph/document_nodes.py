"""
Document-processing nodes for the LangGraph workflow.
"""

from langchain_core.documents import Document
from langchain_core.messages import AIMessage

from src.core.logger import logger
from src.graph.state import AdaptiveRAGState
from src.llms.ollama_client import get_llm
from src.models.query_response import SourceChunk
from src.prompts.answer import ANSWER_PROMPT
from src.rag.query_utils import (
    build_context,
    build_sources,
    calculate_confidence,
)
from src.rag.document_grader import grade_documents
from src.rag.query_rewriter import rewrite_query
from src.rag.retriever import get_retriever


def retrieve_node(
    state: AdaptiveRAGState,
) -> AdaptiveRAGState:
    """
    Retrieve document chunks.
    """
    logger.info("Retrieve node.")

    question = state.get("rewritten_question")

    if question is None:
        question = state["question"]

    retriever = get_retriever()

    state["documents"] = retriever.invoke(
        question,
    )

    return state


def grade_node(
    state: AdaptiveRAGState,
) -> AdaptiveRAGState:
    """
    Grade retrieved chunks.
    """
    logger.info("Grade node.")

    documents = state.get("documents")

    if documents is None:
        raise ValueError(
            "Documents missing from graph state."
        )

    question = state.get("rewritten_question")

    if question is None:
        question = state["question"]

    state["relevant_documents"] = grade_documents(
        question,
        documents,
    )

    return state


def rewrite_node(
    state: AdaptiveRAGState,
) -> AdaptiveRAGState:
    """
    Rewrite the query.
    """
    logger.info("Rewrite node.")

    state["rewritten_question"] = rewrite_query(
        state["question"],
    )

    return state


def generate_node(
    state: AdaptiveRAGState,
) -> AdaptiveRAGState:
    """
    Generate the final answer.
    """
    logger.info("Generate node.")

    documents = state.get("relevant_documents")

    if documents is None:
        raise ValueError(
            "Relevant documents missing."
        )

    question = state.get("rewritten_question")

    if question is None:
        question = state["question"]

    context = build_context(
        documents,
    )

    llm = get_llm()
    chain = ANSWER_PROMPT | llm

    response = chain.invoke(
        {
            "question": question,
            "context": context,
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
        answer = response.content
    else:
        answer = "\n".join(
            str(part)
            for part in response.content
        )

    state["answer"] = answer
    state["confidence"] = calculate_confidence(
        len(documents),
    )
    state["source_count"] = len(
        documents,
    )
    state["sources"] = build_sources(
        documents,
    )

    return state


def no_document_node(
    state: AdaptiveRAGState,
) -> AdaptiveRAGState:
    """
    No relevant documents found.
    """
    logger.info("No relevant documents node.")

    state["answer"] = (
        "I could not find relevant information "
        "in the uploaded documents."
    )
    state["confidence"] = 0.0
    state["source_count"] = 0
    state["sources"] = []

    return state