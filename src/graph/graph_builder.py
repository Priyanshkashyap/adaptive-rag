"""
Build the Adaptive RAG LangGraph.
"""

from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from src.graph.document_nodes import (
    generate_node,
    grade_node,
    no_document_node,
    retrieve_node,
    rewrite_node,
)
from src.graph.nodes import (
    classify_node,
    general_node,
    search_node,
)
from src.graph.state import AdaptiveRAGState


def route_after_classifier(
    state: AdaptiveRAGState,
) -> str:
    """
    Decide which pipeline to execute.
    """

    route = state.get("route")

    if route == "INDEX":
        return "retrieve"

    if route == "GENERAL":
        return "general"

    if route == "SEARCH":
        return "search"

    raise ValueError(
        f"Unknown route: {route}"
    )


def route_after_grading(
    state: AdaptiveRAGState,
) -> str:
    """
    Decide whether rewriting is needed.
    """

    rewritten = state.get(
        "rewritten_question"
    )

    relevant = state.get(
        "relevant_documents",
        [],
    )

    if relevant:
        return "generate"

    if rewritten is None:
        return "rewrite"

    return "no_documents"


builder = StateGraph(
    AdaptiveRAGState,
)

builder.add_node(
    "classifier",
    classify_node,
)

builder.add_node(
    "retrieve",
    retrieve_node,
)

builder.add_node(
    "grade",
    grade_node,
)

builder.add_node(
    "rewrite",
    rewrite_node,
)

builder.add_node(
    "generate",
    generate_node,
)

builder.add_node(
    "no_documents",
    no_document_node,
)

builder.add_node(
    "general",
    general_node,
)

builder.add_node(
    "search",
    search_node,
)

builder.add_edge(
    START,
    "classifier",
)

builder.add_conditional_edges(
    "classifier",
    route_after_classifier,
)

builder.add_edge(
    "retrieve",
    "grade",
)

builder.add_conditional_edges(
    "grade",
    route_after_grading,
)

builder.add_edge(
    "rewrite",
    "retrieve",
)

builder.add_edge(
    "generate",
    END,
)

builder.add_edge(
    "general",
    END,
)

builder.add_edge(
    "search",
    END,
)

builder.add_edge(
    "no_documents",
    END,
)

graph = builder.compile()