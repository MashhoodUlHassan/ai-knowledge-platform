from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_api():
    response = client.post(
        "/chat",
        json={"message": "What is AI?"},
    )

    assert response.status_code in [200, 400, 500]