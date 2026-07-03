"""
FastAPI application entrypoint.
"""

from fastapi import FastAPI

from src.api.routes import router
from src.core.logger import logger

app = FastAPI( # This creates the main FastAPI application object.
    title="Adaptive RAG API",
    version="1.0.0",
    description="Agentic RAG system",
)

app.include_router(router, prefix="/rag", tags=["rag"]) # Take all endpoints inside router and add them to the application.


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Returns:
        Welcome message.
    """
    logger.info("Root endpoint accessed")
    return {"message": "Adaptive RAG API"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Health status.
    """
    logger.info("Health endpoint accessed")
    return {"status": "healthy"}