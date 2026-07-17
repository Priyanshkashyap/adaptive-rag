"""
Application settings.
"""

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    """

    # Groq
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # Embeddings (we'll switch to HuggingFace next)
    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # Tavily
    tavily_api_key: str = ""

    # Qdrant
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    qdrant_collection: str = "documents"

    # Retrieval
    retriever_k: int = 5

    # MongoDB
    mongodb_url: str = ""
    mongodb_database: str = "adaptive_rag"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()