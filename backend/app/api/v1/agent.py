from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.graph import agent_graph

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
            "sources": result["retrieved_context"],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Agent failed: {str(exc)}",
        ) from exc