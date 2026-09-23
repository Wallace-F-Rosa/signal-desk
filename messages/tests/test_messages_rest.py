from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
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
    assert response.json()["id"] is not None

def test_create_message_exception():
    with patch("messages.service.MessageService.create_message") as mock_create:
        mock_create.side_effect = SQLAlchemyError("DB Error")
        test_message = {"text": "test text"}
        response = client.post("/api/messages", json=test_message)
        assert response.status_code == 500
        assert response.json()["detail"] == "Unable to save message"

def test_get_messages_exception():
    with patch("messages.service.MessageService.get_messages") as mock_get:
        mock_get.side_effect = SQLAlchemyError("DB Error")
        response = client.get("/api/messages")
        assert response.status_code == 500
        assert response.json()["detail"] == "Unable to load messages"

def test_create_message_invalid_payload():
    # Testing Pydantic validation (exception path for request logic)
    invalid_message = {"wrong_field": "test text"}
    response = client.post("/api/messages", json=invalid_message)
    assert response.status_code == 422
