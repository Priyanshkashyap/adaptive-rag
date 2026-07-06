"""
Document indexing utilities.
"""

from langchain_core.documents import Document

from src.core.logger import logger
from src.db.vector_store import get_vector_store


def index_documents(
    chunks: list[Document],
) -> None:
    """
    Store chunks inside Qdrant.

    Args:
        chunks:
            Chunked documents.
    """

    logger.info(
        "Indexing %d chunks",
        len(chunks),
    )

    vector_store = get_vector_store()

    vector_store.add_documents(
        chunks,
    )

    logger.info(
        "Document indexing completed.",
    )