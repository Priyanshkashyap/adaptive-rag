"""
Qdrant vector store helpers.
"""

from langchain_qdrant import QdrantVectorStore

from src.config.settings import settings
from src.db.qdrant import get_qdrant_client
from src.embeddings.ollama_embeddings import get_embeddings


def get_vector_store() -> QdrantVectorStore: # its like jpa uses entity and entity manager to talk to postgres sql
    """
    Create Qdrant vector store.

    Returns:
        Configured vector store.
    """

    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=settings.qdrant_collection,
        embedding=get_embeddings(),
    )