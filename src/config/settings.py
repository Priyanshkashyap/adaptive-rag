"""
Application settings.
"""

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    """

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:8b"
    embedding_model: str = "nomic-embed-text"
    tavily_api_key: str = ""
    embedding_model: str = "nomic-embed-text"
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    qdrant_collection: str = "documents"
    retriever_k: int = 5
    mongodb_url: str = ""
    mongodb_database: str = "adaptive_rag"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()