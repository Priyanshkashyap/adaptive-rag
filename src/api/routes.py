"""
API route definitions for Adaptive RAG.
"""

from fastapi import APIRouter, File, Header, HTTPException, UploadFile, status
from src.rag.query_classifier import classify_query
from src.core.logger import logger
from src.models.query import QueryRequest
from src.models.query_response import QueryResponse
from src.models.upload import DocumentUploadResponse
from src.rag.document_upload import process_document, save_uploaded_document
from src.rag.query_service import answer_from_documents
from src.rag.general_service import answer_general_question
from src.rag.search_service import answer_from_search

router = APIRouter()

@router.get("/status")
async def get_status() -> dict[str, str]:
    """
    Check API status.

    Returns:
        Status response.
    """
    return {
        "status": "running",
        "service": "adaptive-rag",
    }

@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    x_description: str | None = Header(default=None, alias="X-Description"),
) -> DocumentUploadResponse:
    """
    Upload a document, save it temporarily, load it, and chunk it.

    Args:
        file:
            Uploaded document.
        x_description:
            Description provided in the header.

    Returns:
        Upload response.
    """
    if not x_description or not x_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Description header is required.",
        )

    temp_path = await save_uploaded_document(file)

    chunks = process_document(
        file_path=str(temp_path),
        filename=file.filename or "unknown",
        description=x_description.strip(),
    )

    logger.info("Upload completed for file=%s", file.filename)

    return DocumentUploadResponse(
        status=True,
        filename=file.filename or "unknown",
        temp_path=str(temp_path),
        description=x_description.strip(),
        chunk_count=len(chunks),
    )


@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest) -> QueryResponse:
    """
    Query uploaded documents using retrieve -> generate flow.

    Args:
        request:
            Query request containing question and session ID.

    Returns:
        Query response with answer and sources.
    """
    route = classify_query(request.query,)
    logger.info("Query route=%s",route.route,)
    if route.route == "INDEX":
        result = answer_from_documents(request.query)
    elif route.route == "GENERAL":
        result = answer_general_question(request.query,)
    elif route.route == "SEARCH":
        result = answer_from_search(request.query,)
    else:
        raise HTTPException(status_code=400,detail="Unknown route.",)
    return QueryResponse(
    status="success",
    confidence=result.confidence,
    session_id=request.session_id,
    question=request.query,
    answer=result.answer,
    source_count=result.source_count,
    sources=result.sources,
)