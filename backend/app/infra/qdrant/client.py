from qdrant_client import QdrantClient
QDRANT_PATH = "backend/app/storage/qdrant"
client = QdrantClient(
    path=QDRANT_PATH,
)
