"""
API route definitions for Adaptive RAG.
"""

from fastapi import (
    APIRouter,
    File,
    Header,
    HTTPException,
    UploadFile,
    status,
)

from src.core.logger import logger
from src.memory.chat_history import load_messages
from src.memory.chat_history import save_message
from src.models.query import QueryRequest
from src.models.query_response import QueryResponse
from src.models.upload import DocumentUploadResponse
from src.rag.document_upload import (
    process_document,
    save_uploaded_document,
)
from src.graph.graph_builder import graph
from src.graph.state import AdaptiveRAGState

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


@router.post(
    "/documents/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    x_description: str |None = Header(
        default=None,
        alias="X-Description",
    ),
    x_session_id: str | None = Header(
        default=None,
        alias="X-Session-Id",
    ),
) -> DocumentUploadResponse:
    """
    Upload a document.

    Args:
        file:
            Uploaded document.

        x_description:
            User supplied description.

        x_session_id:
            Session identifier used for document isolation.

    Returns:
        Upload response.
    """

    if not x_description or not x_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Description header is required.",
        )

    if not x_session_id or not x_session_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Session-Id header is required.",
        )

    try:

        temp_path = await save_uploaded_document(file)

        chunks = process_document(
            file_path=str(temp_path),
            filename=file.filename or "unknown",
            description=x_description.strip(),
            session_id=x_session_id.strip(),
        )

        logger.info(
            "Upload completed for file=%s",
            file.filename,
        )

        return DocumentUploadResponse(
            status=True,
            filename=file.filename or "unknown",
            temp_path=str(temp_path),
            description=x_description.strip(),
            chunk_count=len(chunks),
        )

    except HTTPException:
        raise

    except Exception:

        logger.exception(
            "Document upload failed."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document upload failed.",
        )


@router.post(
    "/query",
    response_model=QueryResponse,
)
async def query_document(
    request: QueryRequest,
) -> QueryResponse:
    """
    Execute the LangGraph workflow.
    """

    save_message(
        request.session_id,
        "user",
        request.query,
    )

    initial_state: AdaptiveRAGState = {
        "question": request.query,
        "session_id": request.session_id,
    }

    final_state = graph.invoke(
        initial_state,
    )

    save_message(
        request.session_id,
        "assistant",
        final_state["answer"],
    )

    return QueryResponse(
        status="success",
        confidence=final_state["confidence"],
        session_id=request.session_id,
        question=request.query,
        answer=final_state["answer"],
        source_count=final_state["source_count"],
        sources=final_state["sources"],
    )


@router.get(
    "/history/{session_id}",
)
async def get_history(
    session_id: str,
):
    """
    Return chat history.
    """

    try:

        return {
            "messages": load_messages(
                session_id,
            )
        }

    except Exception:

        logger.exception(
            "Failed to load chat history."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load chat history.",
        )