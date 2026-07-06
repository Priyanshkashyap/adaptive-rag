"""
Helpers for validating and saving uploaded documents.
So if your RAG pipeline needs to process the document later, you need your own copy.
"""

from __future__ import annotations # This enables postponed evaluation of type hints.

from pathlib import Path # class for path with prefined functions
from tempfile import gettempdir #Returns the OS temporary directory different for different OS
from uuid import uuid4 #Generates random unique identifiers.
from src.rag.document_loader import (load_pdf_document,load_txt_document,)
from src.rag.text_splitter import (split_documents,)
from fastapi import HTTPException, UploadFile, status #UploadFile Represents a class of uploaded file from multipart form data with prefined functions
from src.core.logger import logger
from src.rag.index_documents import index_documents
ALLOWED_EXTENSIONS = {".pdf", ".txt"}
UPLOAD_DIR = Path(gettempdir()) / "adaptive_rag_uploads" # documents are Saved temporarily in /tmp/adaptive_rag_uploads


def validate_document_filename(filename: str) -> str: # returns what kind of file the file is
    """
    Validate the uploaded filename.

    Args:
        filename: Original filename from the upload.

    Returns:
        The file extension in lowercase.

    Raises:
        HTTPException: If the filename is missing or extension is invalid.
    """
    if not filename: # if it doesnt exist
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required.",
        )

    suffix = Path(filename).suffix.lower() # eg. return .pdf from RAG.PDF

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and TXT files are supported.",
        )

    return suffix


async def save_uploaded_document(file: UploadFile) -> Path:   # input in the post method gets converted to this type hint
    """
    Save the uploaded file into a temporary folder.

    Args:
        file: Uploaded file from FastAPI.

    Returns:
        The saved temporary file path.

    Raises:
        HTTPException: If saving fails or file is empty.
    """
    filename = file.filename or "" 
    validate_document_filename(filename)

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True) # Don't throw an error if the folder already exists.Create parent directories if they don't exist.creates the folder: adaptive_rag_uploads inside upload_dir

    suffix = Path(filename).suffix.lower()
    safe_name = f"{uuid4().hex}_{Path(filename).stem}{suffix}" # f" means string with destructured values
    temp_path = UPLOAD_DIR / safe_name # file name inside folders

    try:
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        temp_path.write_bytes(contents) # creates that file and save the og fne contents in it

        logger.info("Saved uploaded file %s to %s", filename, temp_path)
        return temp_path

    except HTTPException: # In Python, except is the equivalent of Java's catch.
        raise # throw the above exception
    except Exception as exc: # This catches everything else.
        logger.exception("Failed to save uploaded file")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save uploaded file: {exc}",
        ) from exc # Without from exc, Python loses the original stack trace chain.
    finally:
        await file.close()

def process_document(file_path: str,filename: str,description: str,):
    """
    Load and split document.

    Args:
        file_path:
            Saved file path.

    Returns:
        Chunked documents.
    """
    suffix = Path(file_path,).suffix.lower()
    if suffix == ".pdf":
        documents = load_pdf_document(file_path,)
    else:
        documents = load_txt_document(file_path,)

    chunks = split_documents(documents)
    for chunk in chunks:
        chunk.metadata["filename"] = filename
        chunk.metadata["description"] = description
        if "page" not in chunk.metadata: # This code checks whether the metadata dictionary contains a default "page" key, and if it doesn't, it adds one with value 0.
            chunk.metadata["page"] = 0
    index_documents(chunks)
    return chunks