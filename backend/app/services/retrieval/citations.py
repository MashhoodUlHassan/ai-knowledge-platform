def format_citations(results: list[dict]) -> list[dict]:
    """Group retrieved chunks by document while preserving their references."""
    citations = []
    document_sources = {}
    for index, result in enumerate(results, start=1):
        document_id = result.get("document_id")
        key = document_id if document_id is not None else f"unknown-{index}"
        if key not in document_sources:
            source = {
                "source": f"Source {len(document_sources) + 1}",
                "document_id": document_id,
                "score": result.get("score"),
                "text": result.get("text"),
                "chunks": [],
            }
            document_sources[key] = source
            citations.append(source)
        source = document_sources[key]
        source["chunks"].append({
            "chunk_index": result.get("chunk_index"),
            "score": result.get("score"),
            "text": result.get("text"),
        })
        if result.get("score") is not None:
            current_score = source.get("score")
            if current_score is None or result["score"] > current_score:
                source["score"] = result["score"]
    return citations
