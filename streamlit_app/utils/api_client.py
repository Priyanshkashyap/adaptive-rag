"""
FastAPI client utilities.
"""

import requests


BASE_URL = "http://127.0.0.1:8000/rag"


def _handle_response(
    response: requests.Response,
) -> dict:
    """
    Validate API response.

    Args:
        response:
            HTTP response from FastAPI.

    Returns:
        Parsed JSON response.

    Raises:
        RuntimeError:
            If the API returns an error.
    """

    if response.ok:
        return response.json()

    try:
        detail = response.json().get(
            "detail",
            "Unknown server error.",
        )
    except Exception:
        detail = "Unknown server error."

    raise RuntimeError(detail)


def upload_document(
    uploaded_file,
    description: str,
) -> dict:
    """
    Upload document to FastAPI.

    Args:
        uploaded_file:
            Streamlit uploaded file.

        description:
            Document description.

    Returns:
        Upload response.
    """

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type,
        )
    }

    headers = {
        "X-Description": description,
    }

    response = requests.post(
        f"{BASE_URL}/documents/upload",
        files=files,
        headers=headers,
        timeout=300,
    )

    return _handle_response(
        response,
    )


def ask_question(
    question: str,
    session_id: str,
) -> dict:
    """
    Query FastAPI.

    Args:
        question:
            User question.

        session_id:
            Chat session.

    Returns:
        Query response.
    """

    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "query": question,
            "session_id": session_id,
        },
        timeout=120,
    )

    return _handle_response(
        response,
    )


def load_history(
    session_id: str,
) -> dict:
    """
    Load chat history from FastAPI.

    Args:
        session_id:
            Chat session identifier.

    Returns:
        Chat history.
    """

    response = requests.get(
        f"{BASE_URL}/history/{session_id}",
        timeout=30,
    )

    return _handle_response(
        response,
    )