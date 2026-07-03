"""
API route definitions for Adaptive RAG.
"""

from fastapi import APIRouter, File, Header, HTTPException, UploadFile, status
from src.rag.document_upload import process_document
from src.core.logger import logger
from src.models.upload import DocumentUploadResponse
from src.rag.document_upload import save_uploaded_document

router = APIRouter()


@router.get("/status")
async def get_status() -> dict[str, str]:
    """
    Check API status.

    Returns:
        A simple status response.
    """
    return {
        "status": "running",
        "service": "adaptive-rag",
    }


@router.post("/documents/upload", response_model=DocumentUploadResponse) # The response returned by this endpoint will have the structure defined by DocumentUploadResponse
async def upload_document(file: UploadFile = File(...), x_description: str | None = Header(default=None, alias="X-Description"),) -> DocumentUploadResponse: # file(...) means required param.read from header a strng value or none.If the header is missing, set the variable to None.The HTTP header name is X-Description, even though the Python variable is called x_description as "-" is not allowed
    """
    Upload a PDF or TXT document and save it temporarily.

    Args:
        file: Uploaded document.
        x_description: Description passed through the X-Description header.

    Returns:
        Upload response with saved path and metadata.

    Raises:
        HTTPException: If description is missing or file upload fails.
    """
    if not x_description or not x_description.strip(): # strip() removes whitespace from the beginning and end of a string.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Description header is required.",
        )

    temp_path = await save_uploaded_document(file)
    chunks = process_document(str(temp_path))
    logger.info("Generated %d chunks",len(chunks),)

    logger.info("Upload completed for file=%s", file.filename)

    return DocumentUploadResponse(
    status=True,
    filename=file.filename or "unknown",
    temp_path=str(temp_path),
    description=x_description.strip(),
    chunk_count=len(chunks),
)