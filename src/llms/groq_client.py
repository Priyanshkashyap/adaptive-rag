"""
Groq client configuration.
"""

from pydantic import SecretStr
from langchain_groq import ChatGroq

from src.config.settings import settings


def get_llm() -> ChatGroq:
    """
    Create Groq LLM instance.

    Returns:
        Groq chat model.
    """

    return ChatGroq(
        model=settings.groq_model,
        api_key=SecretStr(settings.groq_api_key),
        temperature=0,
    )