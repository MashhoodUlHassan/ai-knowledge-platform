from qdrant_client.models import Distance, VectorParams

from app.infra.qdrant.client import client


COLLECTION_NAME = "document_chunks"
VECTOR_SIZE = 384


def create_collection() -> None:
    """
    Create the document chunks collection if it doesn't exist.
    """

    collections = client.get_collections().collections

    collection_names = {
        collection.name
        for collection in collections
    }

    if COLLECTION_NAME not in collection_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )