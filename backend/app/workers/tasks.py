from app.workers.celery_app import celery_app


@celery_app.task
def test_task(name: str) -> str:
    return f"Hello {name}, Celery worker is working!"


@celery_app.task
def process_document_task(document_id: int) -> str:
    from app.core.database import SessionLocal
    from app.models import Document
    from app.services.embedding.service import generate_embedding
    from app.services.document.chunker import chunk_text
    from app.services.document.parser import parse_document
    from app.infra.qdrant.repository import store_embedding

    db = SessionLocal()

    try:
        document = db.get(Document, document_id)

        if not document:
            raise ValueError(
                f"Document with ID {document_id} not found."
            )

        document.status = "processing"
        db.commit()

        extracted_text = parse_document(document.file_path)
        chunks = chunk_text(extracted_text)

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

        return (
            f"Document {document.id} processed successfully "
            f"with {len(chunks)} chunks."
        )

    except Exception:
        db.rollback()

        document = db.get(Document, document_id)

        if document:
            document.status = "failed"
            db.commit()

        raise

    finally:
        db.close()