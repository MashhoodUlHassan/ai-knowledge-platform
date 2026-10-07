from qdrant_client import QdrantClient


QDRANT_URL = "http://localhost:6333"

client = QdrantClient(
    url=QDRANT_URL,
)