"""
Qdrant configuration.
"""

from qdrant_client import QdrantClient

from src.config.settings import settings


def get_qdrant_client() -> QdrantClient:
    """
    Create qdrant client.
    """

    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key
    )