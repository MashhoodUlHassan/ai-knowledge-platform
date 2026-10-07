from uuid import uuid4

from qdrant_client.models import PointStruct

from app.infra.qdrant.client import client
from app.infra.qdrant.service import COLLECTION_NAME


def store_embedding(
    text: str,
    embedding: list[float],
    document_id: int,
    chunk_index: int,
) -> str:
    """
    Store a document chunk and its embedding in Qdrant.
    """

    point_id = str(uuid4())

    point = PointStruct(
        id=point_id,
        vector=embedding,
        payload={
            "document_id": document_id,
            "chunk_index": chunk_index,
            "text": text,
        },
    )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point],
    )

    return point_id