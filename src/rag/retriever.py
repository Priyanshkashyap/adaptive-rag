"""
Retriever helpers.
"""

from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue,
)

from langchain_core.vectorstores import VectorStoreRetriever

from src.config.settings import settings
from src.core.logger import logger
from src.db.vector_store import get_vector_store


def get_retriever(
    session_id: str,
) -> VectorStoreRetriever:
    """
    Create retriever from Qdrant vector store.

    Args:
        session_id:
            Current chat session.

    Returns:
        Configured retriever.
    """

    logger.info(
        "Creating retriever for session=%s",
        session_id,
    )

    vector_store = get_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": settings.retriever_k,
            "filter": Filter(
                must=[
                    FieldCondition(
                        key="metadata.session_id",
                        match=MatchValue(
                            value=session_id,
                        ),
                    )
                ]
            ),
        }
    )

    return retriever