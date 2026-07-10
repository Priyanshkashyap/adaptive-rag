"""
Query answering service.

This module performs the simple flow:
question -> retrieve -> generate.
"""
from langchain_core.documents import Document # contains page content and metadata
from langchain_core.messages import AIMessage # The LLM doesn't return a string directly.has content inside 
from src.core.logger import logger
from src.llms.ollama_client import get_llm
from src.models.query_response import SourceChunk
from src.models.query_result import QueryResult
from src.prompts.answer import ANSWER_PROMPT
from src.rag.retriever import get_retriever

def _build_context(documents: list[Document],) -> str: # This converts retrieved chunks into one long string.
    """
    Convert retrieved documents into a single prompt context.

    Args:
        documents:
            Retrieved chunks from the vector store.

    Returns:
        Formatted context string.
    """
    if not documents:
        return ""

    context_parts: list[str] = []

    for index, document in enumerate(documents,start=1,):

        filename = document.metadata.get("filename","unknown",)
        page = document.metadata.get("page","unknown",)
        description = document.metadata.get("description","unknown",)
        header = f"[Chunk {index} | filename={filename} | page={page} | description={description}]"
        context_parts.append(f"{header}\n{document.page_content}")
    return "\n\n".join(context_parts)

def _build_sources(documents: list[Document],) -> list[SourceChunk]: # give to frontend only parts of chunk thats required
    """
    Build source metadata.

    Args:
        documents:
            Retrieved chunks.

    Returns:
        List of source chunks.
    """
    sources: list[SourceChunk] = []

    for document in documents:

        sources.append(
            SourceChunk( # creating object of this class
                filename=document.metadata.get(
                    "filename",
                    "unknown",
                ),
                page=document.metadata.get(
                    "page",
                ),
                description=document.metadata.get(
                    "description",
                ),
                preview=document.page_content[:250],
            )
        )

    return sources

def _calculate_confidence(source_count: int,) -> float:
    """
    Calculate a simple confidence score.

    Args:
        source_count:
            Number of retrieved chunks.

    Returns:
        Confidence score.
    """
    if source_count >= 5:
        return 0.95
    if source_count == 4:
        return 0.90
    if source_count == 3:
        return 0.85
    if source_count == 2:
        return 0.75
    if source_count == 1:
        return 0.60

    return 0.0

def answer_from_documents(question: str,) -> QueryResult:
    """
    Retrieve relevant chunks and generate an answer.

    Args:
        question:
            User query.

    Returns:
        Generated answer with sources.
    """

    logger.info("Running document query for question=%s",question,)
    retriever = get_retriever()

    documents = retriever.invoke(question,)
    context = _build_context(documents,)
    llm = get_llm()
    chain = ANSWER_PROMPT | llm # The | operator means "pipe the output of the left into the input of the right."

    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )
    if not isinstance(response, AIMessage): # if they not of this exact type
        raise TypeError("Expected AIMessage from LLM.")

    if isinstance(response.content, str):
        answer_text = response.content
    else: # llm will reply in either string or list form
        parts = []
        for part in response.content:
            if isinstance(part, str):
                 parts.append(part)
            else:
                parts.append(str(part))
        answer_text = "\n".join(parts)

    source_count = len(documents)

    return QueryResult(answer=answer_text,source_count=source_count,confidence=_calculate_confidence(source_count,),
    sources=_build_sources(documents),
)