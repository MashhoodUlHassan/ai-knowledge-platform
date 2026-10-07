from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

from app.agents.graph import agent_graph


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    message: str


@router.post("")
def chat(request: ChatRequest):
    try:
        result = agent_graph.invoke(
            {
                "query": request.message,
                "retrieved_context": [],
                "answer": "",
            }
        )

        return {
            "status": "success",
            "message": request.message,
            "answer": result["answer"],
            "sources": result["retrieved_context"],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/stream")
def chat_stream(request: ChatRequest):
    def generate():
        try:
            result = agent_graph.invoke(
                {
                    "query": request.message,
                    "retrieved_context": [],
                    "answer": "",
                }
            )

            data = {
                "status": "success",
                "message": request.message,
                "answer": result["answer"],
                "sources": result["retrieved_context"],
            }

            yield f"data: {json.dumps(data)}\n\n"

        except Exception as exc:
            error = {
                "status": "error",
                "detail": str(exc),
            }

            yield f"data: {json.dumps(error)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )