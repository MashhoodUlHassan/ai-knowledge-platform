import json
import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.agents.graph import agent_graph


logger = logging.getLogger(__name__)


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

        logger.info("Chat request completed successfully")

        return {
            "status": "success",
            "message": request.message,
            "answer": result["answer"],
            "sources": result["retrieved_context"],
        }

    except ValueError as exc:
        logger.warning("Chat request validation failed: %s", exc)

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception("Chat request failed")

        raise HTTPException(
            status_code=500,
            detail="Unable to process your request. Please try again later.",
        ) from None


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

            logger.info("Streaming chat request completed successfully")

            data = {
                "status": "success",
                "message": request.message,
                "answer": result["answer"],
                "sources": result["retrieved_context"],
            }

            yield f"data: {json.dumps(data)}\n\n"

        except ValueError as exc:
            logger.warning(
                "Streaming chat validation failed: %s",
                exc,
            )

            error = {
                "status": "error",
                "detail": str(exc),
            }

            yield f"data: {json.dumps(error)}\n\n"

        except Exception:
            logger.exception("Streaming chat request failed")

            error = {
                "status": "error",
                "detail": "Unable to process your request. Please try again later.",
            }

            yield f"data: {json.dumps(error)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )
