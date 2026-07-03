"""
Document loading utilities.
"""
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader # langchain_community contains integrations with external libraries, services, and data sources.
from langchain_core.documents import Document # langchain_core contains the fundamental abstractions and interfaces that almost every LangChain application uses.
from src.core.logger import logger

def load_pdf_document(file_path: str,) -> list[Document]:
    """
    Load PDF document.

    Args:
        file_path:
            Path to PDF file.

    Returns:
        Loaded document pages.
    """
    logger.info("Loading PDF document from %s",file_path,)
    loader = PyPDFLoader(file_path) # It only creates a loader object and tells it:"When I ask you later, use this PDF file."
    documents = loader.load() # read contents and store in the form of langchain documents
    logger.info("Loaded %d pages from PDF",len(documents),)
    return documents

def load_txt_document(file_path: str,) -> list[Document]:
    """
    Load text document.

    Args:
        file_path:
            Path to TXT file.

    Returns:
        Loaded text document.
    """
    logger.info("Loading TXT document from %s",file_path,)
    text = Path(file_path).read_text(encoding="utf-8",) #Create a Path object
    document = Document(page_content=text,metadata={"source": file_path,},)

    return [document]