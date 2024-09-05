from fastapi import APIRouter, HTTPException
from db.conn_db import create_connection
from .crud import insert_chat, get_chat, get_all_chats
from .models import Chat

router = APIRouter()

@router.post("/")
async def create_chat(chat: Chat):
    conn = create_connection()
    if conn:
        try:
            insert_chat(conn, chat.chatName, chat.userId)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al crear chat: {e}")
        finally:
            conn.close()
    return {"message": "Chat creado exitosamente"}

@router.get("/{userId}")
async def read_chat(userId: int):
    conn = create_connection()
    if conn:
        try:
            chats = get_chat(conn, userId)
            if chats is None:
                raise HTTPException(status_code=404, detail="Chat no encontrado")
            return [{"chatId": chat[0], "chatName": chat[1], "userId": chat[2]} for chat in chats]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al obtener chat: {e}")
        finally:
            conn.close()

@router.get("/")
async def read_chats():
    conn = create_connection()
    if conn:
        try:
            chats = get_all_chats(conn)
            return [{"chatId": chat[0], "chatName": chat[1], "userId": chat[2]} for chat in chats]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al obtener chats: {e}")
        finally:
            conn.close()
