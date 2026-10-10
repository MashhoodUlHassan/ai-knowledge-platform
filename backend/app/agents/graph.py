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
    results = retrieve_documents.invoke({"query": query})
    logger.info("Agent retrieval completed: results=%s", len(results))
    return {
        **state,
        "query": query,
        "retrieved_context": results,
    }
def build_document_context(results: list[dict]) -> str:
    """Group retrieved chunks by document for consistent source numbering."""
    documents = {}
    unknown_counter = 0
    for result in results:
        document_id = result.get("document_id")
        if document_id is None:
            unknown_counter += 1
            key = f"unknown-{unknown_counter}"
        else:
            key = document_id
        if key not in documents:
            documents[key] = {
                "document_id": document_id,
                "chunks": [],
            }
        text = result.get("text")
        if text:
            documents[key]["chunks"].append(text)
    context_parts = []
    for index, document in enumerate(documents.values(), start=1):
        document_id = document["document_id"]
        label = (
            f"Document {document_id}"
            if document_id is not None
            else "Document ID unknown"
        )
        chunk_text = "\n\n".join(document["chunks"])
        context_parts.append(
            f"[Source {index}] {label}\n{chunk_text}"
        )
    return "\n\n".join(context_parts)
def answer_node(state: AgentState) -> AgentState:
    results = state["retrieved_context"]
    context = build_document_context(results)
    prompt = f"""
You are an AI Knowledge Platform assistant.
Answer the user's question using ONLY the provided context.
If the answer cannot be found in the context, say:
"I don't have enough information in the provided documents."
Citation rules:
- Cite supporting sources using their exact labels, such as [Source 1].
- Place citations at the end of the relevant sentence or paragraph.
- Avoid repeating the same citation unnecessarily.
- Cite only sources that support the claim.
- Never invent source numbers or unsupported facts.
- If the context does not contain the answer, clearly say so.
User question:
{state["query"]}
Context:
{context}
"""
    logger.info(
        "Generating AI answer: document_sources=%s, retrieved_chunks=%s",
        len({item.get("document_id") for item in results}),
        len(results),
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
            item.get("text", "") if isinstance(item, dict) else str(item)
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
