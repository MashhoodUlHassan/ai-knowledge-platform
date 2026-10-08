from io import BytesIO

import pytest
from fastapi import UploadFile

from app.core.database import SessionLocal
from app.services.document.service import save_and_process_document


@pytest.mark.asyncio
async def test_save_and_process_document():
    db = SessionLocal()

    try:
        file = UploadFile(
            filename="service_test.txt",
            file=BytesIO(
                b"AI Knowledge Platform is working correctly. "
                b"This document will be saved, parsed, and chunked."
            ),
        )

        result = await save_and_process_document(file, db)

        assert result is not None
        assert result["filename"] == "service_test.txt"
        assert result["status"] is not None

    finally:
        db.close()