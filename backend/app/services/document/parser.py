from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader


def parse_document(file_path: str) -> str:
    """
    Extract text from PDF, DOCX, or TXT files.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        return _parse_pdf(path)

    if extension == ".docx":
        return _parse_docx(path)

    if extension == ".txt":
        return _parse_txt(path)

    raise ValueError(
        f"Unsupported file type: {extension}. "
        "Supported types: .pdf, .docx, .txt"
    )


def _parse_pdf(path: Path) -> str:
    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages).strip()


def _parse_docx(path: Path) -> str:
    document = DocxDocument(str(path))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n\n".join(paragraphs).strip()


def _parse_txt(path: Path) -> str:
    return path.read_text(
        encoding="utf-8",
        errors="ignore",
    ).strip()