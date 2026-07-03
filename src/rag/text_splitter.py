"""
Document chunking utilities.
"""
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.logger import logger

def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split documents into chunks.

    Args:
        documents:
            Loaded documents.

    Returns:
        Chunked documents.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=150,)
    chunks = splitter.split_documents(documents)
    logger.info("Created %d chunks",len(chunks),)
    return chunks