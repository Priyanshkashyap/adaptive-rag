"""
Shared LangGraph state.
"""

from typing import NotRequired, TypedDict

from langchain_core.documents import Document

from src.models.query_response import SourceChunk


class AdaptiveRAGState(TypedDict):
    """
    Shared state passed between LangGraph nodes.
    """

    # Present at graph start
    question: str
    session_id: str

    # Filled by classifier
    route: NotRequired[str]

    # Filled by retriever
    documents: NotRequired[list[Document]]

    # Filled by grader
    relevant_documents: NotRequired[list[Document]]

    # Filled by rewriter
    rewritten_question: NotRequired[str]

    # Filled by generator
    answer: NotRequired[str]
    confidence: NotRequired[float]
    source_count: NotRequired[int]
    sources: NotRequired[list[SourceChunk]]

    # Filled on failure
    error: NotRequired[str]