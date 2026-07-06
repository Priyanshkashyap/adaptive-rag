"""
Qdrant configuration.
"""
from qdrant_client import QdrantClient
from src.config.settings import settings
from src.core.logger import logger

def get_qdrant_client() -> QdrantClient:
    """
    Create Qdrant client.

    Returns:
        Connected Qdrant client.

    Raises:
        ValueError:
            If environment variables are missing.
    """

    if not settings.qdrant_url:
        raise ValueError(
            "QDRANT_URL missing in .env"
        )

    if not settings.qdrant_api_key:
        raise ValueError(
            "QDRANT_API_KEY missing in .env"
        )

    logger.info(
        "Creating Qdrant client"
    )

    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )