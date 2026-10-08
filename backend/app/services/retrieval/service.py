import logging

from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.infra.qdrant.client import client
from app.infra.qdrant.service import COLLECTION_NAME
from app.services.embedding.service import generate_embedding


logger = logging.getLogger(__name__)


def search_similar_chunks(
    query: str,
    document_id: int | None = None,
    top_k: int = 5,
) -> list[dict]:
    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    if top_k < 1 or top_k > 20:
        raise ValueError("top_k must be between 1 and 20.")

    logger.info(
        "Starting vector retrieval: document_id=%s, top_k=%s",
        document_id,
        top_k,
    )

    query_embedding = generate_embedding(query)

    query_filter = None

    if document_id is not None:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id),
                )
            ]
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=query_filter,
        limit=top_k,
        with_payload=True,
    ).points

    logger.info(
        "Vector retrieval completed: results=%s",
        len(results),
    )

    return [
        {
            "id": str(result.id),
            "score": result.score,
            "document_id": result.payload.get("document_id"),
            "chunk_index": result.payload.get("chunk_index"),
            "text": result.payload.get("text"),
        }
        for result in results
    ]
