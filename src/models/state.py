"""
LangGraph shared state object.
"""

from typing import TypedDict


class GraphState(TypedDict):
    """
    Shared graph state.

    Attributes:
        query:
            User question.

        route:
            Selected route.

        documents:
            Retrieved chunks.

        answer:
            Final generated answer.
    """

    query: str
    route: str
    documents: list
    answer: str
