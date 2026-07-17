"""
Helpers for validating and saving uploaded documents.

So if your RAG pipeline needs to process the document later,
you need your own copy.
"""

from __future__ import annotations

from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

from fastapi import (
    HTTPException,
    UploadFile,
    status,
)

from src.core.logger import logger
from src.rag.document_loader import (
    load_pdf_document,
    load_txt_document,
)
from src.rag.index_documents import index_documents
from src.rag.text_splitter import split_documents

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
}

UPLOAD_DIR = (
    Path(gettempdir())
    / "adaptive_rag_uploads"
)


def validate_document_filename(
    filename: str,
) -> str:
    """
    Validate uploaded filename.

    Args:
        filename:
            Original filename.

    Returns:
        Lowercase extension.
    """

    if not filename:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required.",
        )

    suffix = Path(
        filename,
    ).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and TXT files are supported.",
        )

    return suffix


async def save_uploaded_document(
    file: UploadFile,
) -> Path:
    """
    Save uploaded document temporarily.
    """

    filename = file.filename or ""

    validate_document_filename(
        filename,
    )

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    suffix = Path(
        filename,
    ).suffix.lower()

    safe_name = (
        f"{uuid4().hex}_"
        f"{Path(filename).stem}"
        f"{suffix}"
    )

    temp_path = (
        UPLOAD_DIR
        / safe_name
    )

    try:

        logger.info(
            "Reading uploaded file."
        )

        contents = await file.read()

        if not contents:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        temp_path.write_bytes(
            contents,
        )

        logger.info(
            "Saved uploaded file %s to %s",
            filename,
            temp_path,
        )

        return temp_path

    except HTTPException:
        raise

    except Exception as exc:

        logger.exception(
            "Failed to save uploaded file."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save uploaded file: {exc}",
        ) from exc

    finally:

        await file.close()


def process_document(
    file_path: str,
    filename: str,
    description: str,
    session_id: str,
):
    """
    Load, split and index document.
    """

    try:

        logger.info(
            "Processing document=%s",
            filename,
        )

        suffix = Path(
            file_path,
        ).suffix.lower()

        logger.info(
            "Loading document."
        )

        if suffix == ".pdf":

            documents = load_pdf_document(
                file_path,
            )

        else:

            documents = load_txt_document(
                file_path,
            )

        logger.info(
            "Splitting document."
        )

        chunks = split_documents(
            documents,
        )

        for chunk in chunks:

            chunk.metadata["filename"] = filename
            chunk.metadata["description"] = description
            chunk.metadata["session_id"] = session_id

            if "page" not in chunk.metadata:

                chunk.metadata["page"] = 0

        logger.info(
            "Created %d chunks.",
            len(chunks),
        )

        logger.info(
            "Indexing chunks."
        )

        index_documents(
            chunks,
        )

        logger.info(
            "Document processing completed."
        )

        return chunks

    except HTTPException:
        raise

    except Exception:

        logger.exception(
            "Document processing failed."
        )

        raise