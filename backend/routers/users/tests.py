import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "Usuario creado exitosamente"}

    # Intentar crear el mismo usuario otra vez para verificar la duplicación
    duplicate_response = client.post("/users/", json={"username": "testuser", "password": "testpassword"})
    assert duplicate_response.status_code == 400
    assert duplicate_response.json() == {"detail": "El usuario ya existe"}

def test_login():
    # Crear un usuario para probar el login
    client.post("/users/", json={"username": "testuser", "password": "testpassword"})
    
    # Intentar iniciar sesión con credenciales correctas
    response = client.get("/login/", params={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "Inicio de sesión exitoso"}

    # Intentar iniciar sesión con contraseña incorrecta
    wrong_password_response = client.get("/login/", params={"username": "testuser", "password": "wrongpassword"})
    assert wrong_password_response.status_code == 400
    assert wrong_password_response.json() == {"detail": "Usuario o contraseña incorrectos"}

    # Intentar iniciar sesión con un usuario que no existe
    non_existent_user_response = client.get("/login/", params={"username": "nonexistent", "password": "testpassword"})
    assert non_existent_user_response.status_code == 400
    assert non_existent_user_response.json() == {"detail": "Usuario o contraseña incorrectos"}