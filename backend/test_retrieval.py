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


def test_retrieval_top_k_validation():
    response = client.post(
        "/api/v1/retrieval/search",
        json={
            "query": "What is artificial intelligence?",
            "top_k": 0,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "top_k must be between 1 and 20."


def test_retrieval_top_k_max_validation():
    response = client.post(
        "/api/v1/retrieval/search",
        json={
            "query": "What is artificial intelligence?",
            "top_k": 21,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "top_k must be between 1 and 20."
