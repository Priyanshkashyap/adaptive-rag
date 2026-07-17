"""
Web search answering service.
"""

from langchain_core.messages import AIMessage

from src.core.logger import logger
from src.llms.groq_client import get_llm
from src.models.query_result import QueryResult
from src.prompts.search import SEARCH_PROMPT
from src.tools.search import get_tavily_client


def answer_from_search(
    question: str,
) -> QueryResult:
    """
    Search the web using Tavily and summarize using Ollama.

    Args:
        question:
            User question.

    Returns:
        Generated answer.
    """

    try:

        logger.info(
            "Running Tavily search."
        )

        tavily = get_tavily_client()

        results = tavily.search(
            query=question,
            max_results=5,
        )

        logger.info(
            "Retrieved %d web results.",
            len(results["results"]),
        )

        context_parts: list[str] = []

        for result in results["results"]:

            title = result.get(
                "title",
                "",
            )

            content = result.get(
                "content",
                "",
            )

            url = result.get(
                "url",
                "",
            )

            context_parts.append(
                f"""
Title:
{title}

Content:
{content}

URL:
{url}
"""
            )

        context = "\n\n".join(
            context_parts,
        )

        llm = get_llm()

        chain = SEARCH_PROMPT | llm

        logger.info(
            "Generating answer from web search."
        )

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

        if isinstance(
            response.content,
            str,
        ):
            answer = response.content

        else:
            answer = "\n".join(
                str(part)
                for part in response.content
            )

        logger.info(
            "Web search answer generated successfully."
        )

        return QueryResult(
            answer=answer,
            source_count=len(
                results["results"]
            ),
            confidence=0.90,
            sources=[],
        )

    except Exception:

        logger.exception(
            "Search answering failed."
        )

        raise