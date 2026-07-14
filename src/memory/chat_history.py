"""
MongoDB chat history.
"""

from src.core.logger import logger
from src.db.mongodb import get_database


def _collection():
    """
    Return chat collection.
    """

    return get_database()[
        "chat_history"
    ]


def load_messages(
    session_id: str,
) -> list[dict]:
    """
    Load chat history.
    """

    try:

        logger.info(
            "Loading chat history for session=%s",
            session_id,
        )

        document = _collection().find_one(
            {
                "session_id": session_id,
            }
        )

        if document is None:

            logger.info(
                "No chat history found."
            )

            return []

        logger.info(
            "Loaded %d messages.",
            len(document["messages"]),
        )

        return document["messages"]

    except Exception:

        logger.exception(
            "Failed to load chat history."
        )

        raise


def save_message(
    session_id: str,
    role: str,
    content: str,
) -> None:
    """
    Append one chat message.
    """

    try:

        logger.info(
            "Saving %s message.",
            role,
        )

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

    except Exception:

        logger.exception(
            "Failed to save chat history."
        )

        raise