import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_chat():
    response = client.post("/chats/", json={"chatName": "Test Chat", "userId": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Chat creado exitosamente"}

def test_read_chat():
    # Primero, creamos un chat para obtenerlo después
    create_response = client.post("/chats/", json={"chatName": "Test Chat", "userId": 1})
    assert create_response.status_code == 200
    
    # Suponemos que el chat tiene el ID 1
    chat_id = 1
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["chatId"] == chat_id
    assert data["chatName"] == "Test Chat"
    assert data["userId"] == 1


def test_read_chats():
    # Crear algunos chats
    client.post("/chats/", json={"chatName": "Chat 1", "userId": 1})
    client.post("/chats/", json={"chatName": "Chat 2", "userId": 2})
    
    # Obtener todos los chats
    response = client.get("/chats/")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) >= 2  # Verificamos que al menos dos chats estén en la respuesta
    assert any(chat["chatName"] == "Chat 1" for chat in data)
    assert any(chat["chatName"] == "Chat 2" for chat in data)
