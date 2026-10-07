from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding vector for the given text.
    """

    if not text.strip():
        raise ValueError("Text cannot be empty.")

    embedding = model.encode(text)

    return embedding.tolist()