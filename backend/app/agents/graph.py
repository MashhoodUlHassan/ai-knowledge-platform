import logging

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

from app.agents.guardrails import validate_query
from app.agents.state import AgentState
from app.agents.tools import retrieve_documents
from app.core.settings import settings


logger = logging.getLogger(__name__)


llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    google_api_key=settings.gemini_api_key,
    temperature=0,
)


def retrieve_node(state: AgentState) -> AgentState:
    query = validate_query(state["query"])

    logger.info("Agent retrieval started")

    results = retrieve_documents.invoke(
        {"query": query}
    )

    logger.info(
        "Agent retrieval completed: results=%s",
        len(results),
    )

    return {
        **state,
        "query": query,
        "retrieved_context": results,
    }


def answer_node(state: AgentState) -> AgentState:
    context = "\n\n".join(
        [
            f"[Source {index}] {item['text']}"
            for index, item in enumerate(
                state["retrieved_context"],
                start=1,
            )
        ]
    )

    prompt = f"""
You are an AI Knowledge Platform assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided documents."

Always mention the relevant source numbers.

User question:
{state["query"]}

Context:
{context}
"""

    logger.info(
        "Generating AI answer: context_sources=%s",
        len(state["retrieved_context"]),
    )

    try:
        response = llm.invoke(prompt)

    except Exception:
        logger.exception("LLM answer generation failed")
        raise

    if isinstance(response.content, str):
        answer = response.content

    elif isinstance(response.content, list):
        answer = "".join(
            item.get("text", "")
            if isinstance(item, dict)
            else str(item)
            for item in response.content
        )

    else:
        answer = str(response.content)

    logger.info(
        "AI answer generated successfully: answer_length=%s",
        len(answer),
    )

    return {
        **state,
        "answer": answer,
    }


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", answer_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)

    return graph.compile()


agent_graph = build_agent_graph()
