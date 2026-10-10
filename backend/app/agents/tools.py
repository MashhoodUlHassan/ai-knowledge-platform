from langchain_core.tools import tool
from app.services.retrieval.service import search_similar_chunks
@tool
def retrieve_documents(query: str) -> list[dict]:
    """Retrieve the most relevant document chunks for a user query."""
    return search_similar_chunks(
        query=query,
        top_k=5,
    )
