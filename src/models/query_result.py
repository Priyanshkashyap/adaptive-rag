"""
Internal query result types.
"""

from typing import NamedTuple

from src.models.query_response import SourceChunk


class QueryResult(NamedTuple):
    """
    Internal query result.
    """

    answer: str
    source_count: int
    confidence: float
    sources: list[SourceChunk]