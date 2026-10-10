from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from app.models import Document
from app.services.document.processor import process_document
UPLOAD_DIR = Path("backend/app/storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
async def save_and_process_document(
    file: UploadFile,
    db: Session,
) -> dict:
    """Save and process a document without Celery or Redis."""
    if not file.filename:
        raise ValueError("Filename is required.")
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            "Supported types: .pdf, .docx, .txt"
        )
    unique_filename = f"{uuid4()}_{Path(file.filename).name}"
    file_path = UPLOAD_DIR / unique_filename
    content = await file.read()
    if not content:
        raise ValueError("The uploaded file is empty.")
    file_path.write_bytes(content)
    document = Document(
        filename=Path(file.filename).name,
        file_path=str(file_path),
        content_type=file.content_type or "application/octet-stream",
        status="pending",
        description="Document uploaded. Processing started.",
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    document_id = document.id
    # Run synchronous processing in a worker thread.
    # The processor creates its own database session.
    await run_in_threadpool(process_document, document_id)
    db.refresh(document)
    return {
        "id": document.id,
        "filename": document.filename,
        "file_path": document.file_path,
        "content_type": document.content_type,
        "status": document.status,
        "message": document.description,
        "created_at": document.created_at.isoformat(),
    }
