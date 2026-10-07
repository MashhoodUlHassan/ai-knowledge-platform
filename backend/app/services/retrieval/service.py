from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.infra.qdrant.client import client
from app.infra.qdrant.service import COLLECTION_NAME
from app.services.embedding.service import generate_embedding


def search_similar_chunks(
    query: str,
    document_id: int | None = None,
    top_k: int = 5,
) -> list[dict]:
    if not query.strip():
        raise ValueError("Query cannot be empty.")

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