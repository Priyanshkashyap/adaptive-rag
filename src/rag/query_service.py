"""
Query answering service.

This module performs the simple flow:
question -> retrieve -> grade -> rewrite -> generate.
"""

from langchain_core.documents import Document
from langchain_core.messages import AIMessage

from src.core.logger import logger
from src.llms.ollama_client import get_llm
from src.models.query_response import SourceChunk
from src.models.query_result import QueryResult
from src.prompts.answer import ANSWER_PROMPT
from src.rag.document_grader import grade_documents
from src.rag.query_rewriter import rewrite_query
from src.rag.retriever import get_retriever


def _build_context(
    documents: list[Document],
) -> str:
    """
    Convert retrieved documents into a single prompt context.
    """

    if not documents:
        return ""

    context_parts: list[str] = []

    for index, document in enumerate(
        documents,
        start=1,
    ):
        filename = document.metadata.get(
            "filename",
            "unknown",
        )

        page = document.metadata.get(
            "page",
            "unknown",
        )

        description = document.metadata.get(
            "description",
            "unknown",
        )

        header = (
            f"[Chunk {index} | "
            f"filename={filename} | "
            f"page={page} | "
            f"description={description}]"
        )

        context_parts.append(
            f"{header}\n{document.page_content}"
        )

    return "\n\n".join(
        context_parts,
    )


def _build_sources(
    documents: list[Document],
) -> list[SourceChunk]:
    """
    Build source metadata.
    """

    sources: list[SourceChunk] = []

    for document in documents:

        sources.append(
            SourceChunk(
                filename=document.metadata.get(
                    "filename",
                    "unknown",
                ),
                page=document.metadata.get(
                    "page",
                ),
                description=document.metadata.get(
                    "description",
                ),
                preview=document.page_content[:250],
            )
        )

    return sources


def _calculate_confidence(
    source_count: int,
) -> float:
    """
    Calculate confidence.
    """

    if source_count >= 5:
        return 0.95

    if source_count == 4:
        return 0.90

    if source_count == 3:
        return 0.85

    if source_count == 2:
        return 0.75

    if source_count == 1:
        return 0.60

    return 0.0


def answer_from_documents(
    question: str,
) -> QueryResult:
    """
    Retrieve, grade, rewrite if needed,
    and generate answer.
    """

    try:

        logger.info(
            "Running document query."
        )

        retriever = get_retriever()

        logger.info(
            "Retrieving document chunks."
        )

        documents = retriever.invoke(
            question,
        )

        logger.info(
            "Retrieved %d chunks.",
            len(documents),
        )

        logger.info(
            "Grading retrieved chunks."
        )

        relevant_documents = grade_documents(
            question,
            documents,
        )

        logger.info(
            "Relevant chunks=%d",
            len(relevant_documents),
        )

        if not relevant_documents:

            logger.info(
                "No relevant chunks found."
            )

            logger.info(
                "Rewriting question."
            )

            rewritten_question = rewrite_query(
                question,
            )

            logger.info(
                "Rewritten question=%s",
                rewritten_question,
            )

            logger.info(
                "Running retrieval again."
            )

            documents = retriever.invoke(
                rewritten_question,
            )

            logger.info(
                "Retrieved %d chunks after rewrite.",
                len(documents),
            )

            relevant_documents = grade_documents(
                rewritten_question,
                documents,
            )

            logger.info(
                "Relevant chunks after retry=%d",
                len(relevant_documents),
            )

            if not relevant_documents:

                logger.warning(
                    "No relevant chunks even after rewrite."
                )

                return QueryResult(
                    answer=(
                        "I could not find relevant "
                        "information in the uploaded "
                        "documents."
                    ),
                    source_count=0,
                    confidence=0.0,
                    sources=[],
                )

            question = rewritten_question

        logger.info(
            "Building prompt context."
        )

        context = _build_context(
            relevant_documents,
        )

        llm = get_llm()

        chain = (
            ANSWER_PROMPT
            | llm
        )

        logger.info(
            "Generating answer."
        )

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
                "Expected AIMessage from LLM."
            )

        if isinstance(
            response.content,
            str,
        ):
            answer_text = response.content

        else:

            parts: list[str] = []

            for part in response.content:

                parts.append(
                    part
                    if isinstance(
                        part,
                        str,
                    )
                    else str(part)
                )

            answer_text = "\n".join(
                parts,
            )

        source_count = len(
            relevant_documents,
        )

        logger.info(
            "Answer generated successfully."
        )

        return QueryResult(
            answer=answer_text,
            source_count=source_count,
            confidence=_calculate_confidence(
                source_count,
            ),
            sources=_build_sources(
                relevant_documents,
            ),
        )

    except Exception:

        logger.exception(
            "Document answering failed."
        )

        raise