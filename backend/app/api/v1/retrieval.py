from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.retrieval.citations import format_citations
from app.services.retrieval.service import search_similar_chunks

router = APIRouter(prefix="/retrieval", tags=["Retrieval"])


class RetrievalRequest(BaseModel):
    query: str
    document_id: int | None = None
    top_k: int = 5


@router.post("/search")
def retrieve_chunks(request: RetrievalRequest):
    try:
        results = search_similar_chunks(
            query=request.query,
            document_id=request.document_id,
            top_k=request.top_k,
        )

        citations = format_citations(results)

        return {
            "status": "success",
            "query": request.query,
            "results": results,
            "citations": citations,
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Retrieval failed: {str(exc)}",
        ) from exc