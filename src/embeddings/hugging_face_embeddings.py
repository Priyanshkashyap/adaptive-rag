"""
Embedding model configuration.
"""

from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from src.config.settings import settings


def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Create embedding model.

    Returns:
        HuggingFace embedding model.
    """

    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )