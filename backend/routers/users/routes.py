from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from db.conn_db import create_connection
from .crud import insert_user, get_user, get_all_users
from .models import User

router = APIRouter()

@router.post("/")
async def create_user(user: User):
    conn = create_connection()
    if conn:
        try:
            # Verificar si el usuario ya existe
            if get_user(conn, user.username):
                raise HTTPException(status_code=400, detail="El usuario ya existe")
            insert_user(conn, user.username, user.password)
        except Exception as e:
            print("error: ", e)
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
                raise HTTPException(status_code=400, detail="Usuario o contraseña incorrecta")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al iniciar sesión: {e}")
        finally:
            conn.close()
    return {"message": "Inicio de sesión exitoso"}

@router.get("/")
def get_users():
    conn = create_connection()
    if conn:
        try:
            users = get_all_users(conn)
            if users:
                return JSONResponse(content={"users": users})
            else:
                raise HTTPException(status_code=404, detail="No se encontraron usuarios.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al obtener usuarios: {e}")
        finally:
            conn.close()
    else:
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos.")
