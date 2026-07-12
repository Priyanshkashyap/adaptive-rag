"""
FastAPI client utilities.
"""
import requests # This is Python's HTTP client library.It lets Python send HTTP requests just like a browser. meanwhile fasapi is for backend
import streamlit as st

BASE_URL = "http://127.0.0.1:8000/rag" # This is the base address of your FastAPI server. localhost gets converted to this only

def upload_document(uploaded_file,description: str,) -> dict:
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
        timeout=60,
    )

    response.raise_for_status()
    return response.json()


def ask_question(question: str,session_id: str,) -> dict:
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
    response.raise_for_status() #say reply wrt the status code received from backend
    return response.json() 

def load_history(
    session_id: str,
) -> dict:

    response = requests.get(
        f"{BASE_URL}/history/{session_id}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()