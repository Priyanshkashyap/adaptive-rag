"""
Document relevance grading service.
"""

from typing import cast

from langchain_core.documents import Document

from src.core.logger import logger
from src.llms.groq_client import get_llm
from src.models.grade_result import GradeResult
from src.prompts.grader import GRADER_PROMPT


def _build_grading_context(
    document: Document,
) -> str:
    """
    Convert one retrieved document into a grading context string.

    Args:
        document:
            Retrieved document chunk.

    Returns:
        Formatted grading context.
    """

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

    return (
        f"[filename={filename} | "
        f"page={page} | "
        f"description={description}]\n"
        f"{document.page_content}"
    )


def grade_documents(
    question: str,
    documents: list[Document],
) -> list[Document]:
    """
    Keep only retrieved chunks that are relevant.

    Args:
        question:
            User query.

        documents:
            Retrieved chunks.

    Returns:
        Relevant document chunks.
    """

    try:

        if not documents:

            logger.info(
                "No retrieved documents available for grading."
            )

            return []

        logger.info(
            "Grading %d retrieved chunks.",
            len(documents),
        )

        llm = get_llm()

        structured_llm = llm.with_structured_output(
            GradeResult,
        )

        chain = (
            GRADER_PROMPT
            | structured_llm
        )

        relevant_documents: list[Document] = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            result = cast(
                GradeResult,
                chain.invoke(
                    {
                        "question": question,
                        "context": _build_grading_context(
                            document,
                        ),
                    }
                ),
            )

            logger.info(
                "Chunk %d grade=%s",
                index,
                result.binary_score,
            )

            if result.binary_score == "YES":

                relevant_documents.append(
                    document,
                )

        logger.info(
            "%d/%d chunks marked relevant.",
            len(relevant_documents),
            len(documents),
        )

        return relevant_documents

    except Exception:

        logger.exception(
            "Document grading failed."
        )

        raise # "I caught the exception, logged it, and now I want the exact same exception to continue propagating upward."