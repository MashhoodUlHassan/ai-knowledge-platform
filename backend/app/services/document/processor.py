from app.core.database import SessionLocal
from app.models import Document
from app.services.embedding.service import generate_embedding
from app.services.document.chunker import chunk_text
from app.services.document.parser import parse_document
from app.infra.qdrant.repository import store_embedding
def process_document(document_id: int) -> dict:
    """Process a saved document without Celery or Redis."""
    db = SessionLocal()
    try:
        document = db.get(Document, document_id)
        if document is None:
            raise ValueError(
                f"Document with ID {document_id} not found."
            )
        document.status = "processing"
        db.commit()
        extracted_text = parse_document(document.file_path)
        chunks = chunk_text(extracted_text)
        if not chunks:
            raise ValueError(
                "No text could be extracted from the document."
            )
        for chunk_index, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)
            store_embedding(
                text=chunk,
                embedding=embedding,
                document_id=document.id,
                chunk_index=chunk_index,
            )
        document.status = "processed"
        document.description = (
            f"Processed {len(chunks)} text chunks."
        )
        db.commit()
        return {
            "id": document.id,
            "status": document.status,
            "description": document.description,
        }
    except Exception as exc:
        db.rollback()
        document = db.get(Document, document_id)
        if document is not None:
            document.status = "failed"
            document.description = (
                f"Processing failed: {str(exc)[:400]}"
            )
            db.commit()
        raise
    finally:
        db.close()
