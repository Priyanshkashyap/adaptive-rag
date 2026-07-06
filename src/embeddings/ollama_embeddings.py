"""
Embedding model configuration.
"""

from langchain_ollama import OllamaEmbeddings
from src.config.settings import settings

def get_embeddings() -> OllamaEmbeddings:
    """
    Create embedding model.

    Returns:
        Ollama embedding model.
    """

    return OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )