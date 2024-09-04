import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_message():
    # Primero, necesitamos un chat para enviar mensajes a él
    create_chat_response = client.post("/chats/", json={"chatName": "Test Chat", "userId": 1})
    assert create_chat_response.status_code == 200

    response = client.post("/messages/", json={"chatId": 1, "userId": 1, "messageText": "Hello, World!"})
    assert response.status_code == 200
    assert response.json() == {"message": "Mensaje creado exitosamente"}

def test_read_message():
    # Crear un chat y un mensaje para obtener después
    client.post("/chats/", json={"chatName": "Test Chat", "userId": 1})
    client.post("/messages/", json={"chatId": 1, "userId": 1, "messageText": "Hello, World!"})
    
    # Suponemos que el mensaje tiene el ID 1
    message_id = 1
    response = client.get(f"/messages/{message_id}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["messageId"] == message_id
    assert data["chatId"] == 1
    assert data["senderId"] == 1
    assert data["messageText"] == "Hello, World!"

def test_read_messages_by_chat():
    # Crear un chat y algunos mensajes
    client.post("/chats/", json={"chatName": "Test Chat", "userId": 1})
    client.post("/messages/", json={"chatId": 1, "userId": 1, "messageText": "Message 1"})
    client.post("/messages/", json={"chatId": 1, "userId": 1, "messageText": "Message 2"})
    
    # Obtener todos los mensajes del chat con ID 1
    response = client.get("/messages/chat/1")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) >= 2  # Verificamos que al menos dos mensajes estén en la respuesta
    assert any(message["messageText"] == "Message 1" for message in data)
    assert any(message["messageText"] == "Message 2" for message in data)
