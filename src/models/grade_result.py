"""
Internal grading result types.
"""
from typing import Literal
from pydantic import BaseModel

class GradeResult(BaseModel):
    """
    Binary relevance result for a retrieved chunk.
    """
    binary_score: Literal["YES", "NO"]