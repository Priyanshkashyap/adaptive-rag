"""
Tavily search service.
"""

from tavily import TavilyClient

from src.config.settings import settings


def get_tavily_client() -> TavilyClient:
    """
    Create Tavily client.
    """

    return TavilyClient(
        api_key=settings.tavily_api_key
    )