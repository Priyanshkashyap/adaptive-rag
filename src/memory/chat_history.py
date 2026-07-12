"""
MongoDB chat history.
"""
from src.db.mongodb import get_database

def _collection():
    """
    Return chat collection.
    """
    return get_database()["chat_history"] # will return collection [adaptive_rag][chat_history]


def load_messages(session_id: str,) -> list[dict]:
    """
    Load chat history.
    """

    document = _collection().find_one(
        {
            "session_id": session_id,
        }
    )

    if document is None:
        return []

    return document["messages"]


def save_message(session_id: str,role: str,content: str,) -> None:
    """
    Append one chat message.
    """
    _collection().update_one(
        {
            "session_id": session_id,
        },
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content,
                }
            }
        },
        upsert=True,
    )