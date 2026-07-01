"""
Query request model.
"""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """
    User query request.
    """

    query: str = Field(
        min_length=1,
        description="User question"
    )

    session_id: str = Field(
        min_length=1,
        description="Chat session identifier"
    )