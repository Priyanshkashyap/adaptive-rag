"""
Response models for RAG queries.
"""

from pydantic import BaseModel, Field


class SourceChunk(BaseModel):
    """
    Single retrieved source chunk.
    """

    filename: str = Field(
        default="unknown",
        description="Source filename.",
    )

    page: int | None = Field(
        default=None,
        description="Page number if available.",
    )

    description: str | None = Field(
        default=None,
        description="User-provided document description.",
    )

    preview: str = Field(
        default="",
        description="Short preview of chunk text.",
    )


class QueryResponse(BaseModel):
    """
    Response returned by the query endpoint.
    """

    status: str = Field(
        description="Request status.",
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score.",
    )

    session_id: str
    question: str
    answer: str
    source_count: int
    sources: list[SourceChunk]