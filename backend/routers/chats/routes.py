from fastapi import APIRouter, HTTPException
from db.conn_db import create_connection
from .crud import insert_chat, get_chat, get_all_chats

router = APIRouter()

@router.post("/chats/")
async def create_chat(chatName: str, userId: int):
    conn = create_connection()
    if conn:
        try:
            insert_chat(conn, chatName, userId)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al crear chat: {e}")
        finally:
            conn.close()
    return {"message": "Chat creado exitosamente"}

@router.get("/chats/{chatId}")
async def read_chat(chatId: int):
    conn = create_connection()
    if conn:
        try:
            chat = get_chat(conn, chatId)
            if chat is None:
                raise HTTPException(status_code=404, detail="Chat no encontrado")
            return {"chatId": chat[0], "chatName": chat[1], "userId": chat[2]}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al obtener chat: {e}")
        finally:
            conn.close()

@router.get("/chats/")
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
