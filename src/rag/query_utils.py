"""
Shared utilities for document question answering.
"""

from langchain_core.documents import Document

from src.models.query_response import SourceChunk


def build_context(
    documents: list[Document],
) -> str:
    """
    Build prompt context from retrieved documents.

    Args:
        documents:
            Retrieved document chunks.

    Returns:
        Formatted context string.
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


def build_sources(
    documents: list[Document],
) -> list[SourceChunk]:
    """
    Build source metadata for the frontend.

    Args:
        documents:
            Relevant document chunks.

    Returns:
        Source metadata list.
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


def calculate_confidence(
    source_count: int,
) -> float:
    """
    Calculate a simple confidence score.

    Args:
        source_count:
            Number of relevant chunks.

    Returns:
        Confidence score.
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