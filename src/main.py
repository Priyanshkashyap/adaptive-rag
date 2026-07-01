"""
FastAPI application entrypoint.
"""

from fastapi import FastAPI

from src.api.routes import router
from src.core.logger import logger

app = FastAPI(
    title="Adaptive RAG API",
    description="Agentic RAG system",
    version="1.0.0"
)

app.include_router(
    router,
    prefix="/api/v1",
    tags=["system"]
)


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Returns:
        Welcome message.
    """
    logger.info("Root endpoint accessed")

    return {
        "message": "Adaptive RAG API"
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Health status.
    """
    logger.info("Health endpoint accessed")

    return {
        "status": "healthy"
    }