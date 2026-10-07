import asyncio
from io import BytesIO

from fastapi import UploadFile

from app.services.document.service import save_and_process_document


async def main():
    file = UploadFile(
        filename="service_test.txt",
        file=BytesIO(
            b"AI Knowledge Platform is working correctly. "
            b"This document will be saved, parsed, and chunked."
        ),
    )

    result = await save_and_process_document(file)

    print(result)


asyncio.run(main())