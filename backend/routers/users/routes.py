from fastapi import APIRouter, HTTPException, Depends
from db.conn_db import create_connection
from .crud import insert_user, get_user

router = APIRouter()

@router.post("/users/")
async def create_user(username: str, password: str):
    conn = create_connection()
    if conn:
        try:
            # Verificar si el usuario ya existe
            if get_user(conn, username):
                raise HTTPException(status_code=400, detail="El usuario ya existe")
            insert_user(conn, username, password)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al crear usuario: {e}")
        finally:
            conn.close()
    return {"message": "Usuario creado exitosamente"}

@router.get("/login/")
async def login(username: str, password: str):
    conn = create_connection()
    if conn:
        try:
            user = get_user(conn, username)
            if user is None or user[2] != password:
                raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al iniciar sesión: {e}")
        finally:
            conn.close()
    return {"message": "Inicio de sesión exitoso"}
