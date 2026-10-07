from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models import Document
from app.workers.tasks import process_document_task


UPLOAD_DIR = Path("backend/app/storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


async def save_and_process_document(
    file: UploadFile,
    db: Session,
) -> dict:
    """
    Save uploaded document and send document processing
    to a Celery background worker.
    """

    if not file.filename:
        raise ValueError("Filename is required.")

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            "Supported types: .pdf, .docx, .txt"
        )

    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_filename

    content = await file.read()
    file_path.write_bytes(content)

    document = Document(
        filename=file.filename,
        file_path=str(file_path),
        content_type=file.content_type or "application/octet-stream",
        status="pending",
        description="Document uploaded and queued for background processing.",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Send document processing to Celery worker
    process_document_task.delay(document.id)

    return {
        "id": document.id,
        "filename": document.filename,
        "file_path": document.file_path,
        "content_type": document.content_type,
        "status": document.status,
        "message": "Document uploaded and queued for background processing.",
        "created_at": document.created_at.isoformat(),
    }