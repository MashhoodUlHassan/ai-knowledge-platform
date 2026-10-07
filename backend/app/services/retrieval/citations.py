def format_citations(results: list[dict]) -> list[dict]:
    citations = []

    for index, result in enumerate(results, start=1):
        citations.append(
            {
                "source": f"Source {index}",
                "document_id": result.get("document_id"),
                "chunk_index": result.get("chunk_index"),
                "score": result.get("score"),
                "text": result.get("text"),
            }
        )

    return citations