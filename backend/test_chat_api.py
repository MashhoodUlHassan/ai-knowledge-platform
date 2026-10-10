from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_chat_api_success():
    mock_result = {
        "answer": "Artificial intelligence is the field of building intelligent systems.",
        "retrieved_context": [
            {
                "id": "1",
                "score": 0.95,
                "document_id": 1,
                "chunk_index": 0,
                "text": "Artificial intelligence involves building systems that perform tasks requiring human intelligence.",
            }
        ],
    }
    with patch(
        "app.api.v1.chat.agent_graph.invoke",
        return_value=mock_result,
    ):
        response = client.post(
            "/chat",
            json={"message": "What is artificial intelligence?"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "What is artificial intelligence?"
    assert data["answer"] == mock_result["answer"]
    assert len(data["sources"]) == 1
    source = data["sources"][0]
    assert source["source"] == "Source 1"
    assert source["document_id"] == 1
    assert source["score"] == 0.95
    assert source["text"] == mock_result["retrieved_context"][0]["text"]
    assert len(source["chunks"]) == 1
    assert source["chunks"][0]["chunk_index"] == 0
def test_chat_api_empty_message():
    response = client.post(
        "/chat",
        json={"message": ""},
    )
    assert response.status_code == 400
