"""
Qdrant vector store helpers.
"""
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams
from langchain_qdrant import QdrantVectorStore
from src.config.settings import settings
from src.db.qdrant import get_qdrant_client
from src.embeddings.hugging_face_embeddings import get_embeddings
from qdrant_client.models import PayloadSchemaType


def get_vector_store() -> QdrantVectorStore:
    """
    Create Qdrant vector store.

    Returns:
        Configured vector store.
    """

    client = get_qdrant_client()
    collections = client.get_collections()



    names = [ # eg. ["users", "books", "notes"]
        collection.name
        for collection in collections.collections
    ]

    if settings.qdrant_collection not in names: # if not in env

        client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE,
    ),
)

   
    client.create_payload_index( # cuz vo khudse indexing ni kr paara tha sessions_id ka toh manually bolna para krne
    collection_name=settings.qdrant_collection,
    field_name="metadata.session_id",
    field_schema=PayloadSchemaType.KEYWORD,
)

    return QdrantVectorStore(
        client=client,
        collection_name=settings.qdrant_collection,
        embedding=get_embeddings(),
    )