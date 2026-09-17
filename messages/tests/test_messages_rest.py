from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_messages():
    response = client.get("/api/messages")
    assert response.status_code == 200

def test_create_message():
    test_message = {"text": "test text"}
    response = client.post("/api/messages", json=test_message)
    assert response.status_code == 201
    assert response.json()["text"] == test_message["text"]
    assert response.json()["id"] != None