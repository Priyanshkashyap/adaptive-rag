"""
Document grading result.
"""

from pydantic import BaseModel


class GradeResult(BaseModel):
    """
    Retrieval grading output.

    Attributes:
        relevant:
            Whether retrieved chunks are useful.
    """

    relevant: bool
