"""
Ollama client configuration.
"""

from langchain_ollama import ChatOllama # creates a chat model that talks to your local Ollama server.
from src.config.settings import settings

def get_llm() -> ChatOllama:
    """
    Create Ollama LLM instance.

    Returns:
        Ollama LLM.
    """

    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0
    )