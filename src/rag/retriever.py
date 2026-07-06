"""
Retriever helpers.
"""

from langchain_core.vectorstores import VectorStoreRetriever

from src.core.logger import logger
from src.db.vector_store import get_vector_store
from src.config.settings import settings

def get_retriever() -> VectorStoreRetriever:
    """
    Create retriever from Qdrant vector store.

    Returns:
        Configured retriever.
    """

    logger.info(
        "Creating retriever."
    )

    vector_store = get_vector_store()

    retriever = vector_store.as_retriever( # This converts your vector_store into a retriever object with top k chunks.
        search_kwargs={
            "k": settings.retriever_k,
        }
    )

    return retriever