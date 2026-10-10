from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.graph import agent_graph
from app.services.retrieval.citations import format_citations
router = APIRouter(prefix="/agent", tags=["Agent"])
class AgentRequest(BaseModel):
    query: str
@router.post("/ask")
def ask_agent(request: AgentRequest):
    try:
        result = agent_graph.invoke(
            {
                "query": request.query,
                "retrieved_context": [],
                "answer": "",
            }
        )
        return {
            "status": "success",
            "query": request.query,
            "answer": result["answer"],
            "sources": format_citations(result["retrieved_context"]),
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process your request. Please try again later.",
        ) from None
