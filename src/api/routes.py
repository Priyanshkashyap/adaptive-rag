"""
API route definitions.
"""

from fastapi import APIRouter
from src.models.query import QueryRequest

router = APIRouter()


@router.get("/status")
async def get_status() -> dict[str, str]:
    """
    Check API status.

    Returns:
        API status response.
    """
    return {
        "status": "running",
        "service": "adaptive-rag"
    }

@router.post("/query")
async def query(
    request: QueryRequest
) -> dict:
    """
    Process user query.
    """

    return {
        "query": request.query,
        "session_id": request.session_id,
        "answer": "This is a placeholder answer."
    }