"""
Web search answering service.
"""
from langchain_core.messages import AIMessage
from src.core.logger import logger
from src.llms.ollama_client import get_llm
from src.models.query_result import QueryResult
from src.prompts.search import SEARCH_PROMPT
from src.tools.search import get_tavily_client

def answer_from_search(question: str,) -> QueryResult:
    """
    Search the web using Tavily
    and summarize using Ollama.
    """
    logger.info("Running Tavily search.")
    tavily = get_tavily_client()
    results = tavily.search(query=question,max_results=5,)
    context_parts: list[str] = []

    for result in results["results"]: # similar to for result in results.get("results"): but [] Assumes the key must exist , if not Python raises a KeyError.

        title = result.get("title","",)
        content = result.get("content","", )
        url = result.get("url","",)
        context_parts.append(f"""Title:{title}Content:{content}URL:{url}""")

    context = "\n\n".join(context_parts,)
    llm = get_llm()

    chain = SEARCH_PROMPT | llm

    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    if not isinstance(
        response,
        AIMessage,
    ):
        raise TypeError(
            "Expected AIMessage."
        )

    if isinstance(response.content,str,):
        answer = response.content
    else:
        answer = "\n".join(str(part)
            for part in response.content
        )

    return QueryResult(
        answer=answer,
        source_count=len(
            results["results"]
        ),
        confidence=0.90,
        sources=[],
    )