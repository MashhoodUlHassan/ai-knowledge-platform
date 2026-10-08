from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_retrieval_validation():
    response = client.post(
        "/api/v1/retrieval/search",
        json={
            "query": "",
            "top_k": 5,
        },
    )

    assert response.status_code == 400
    assert "detail" in response.json()