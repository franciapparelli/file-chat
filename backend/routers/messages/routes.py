from fastapi import APIRouter, HTTPException
from db.conn_db import create_connection
from .crud import insert_message, get_message, get_messages_by_chat

router = APIRouter()

@router.post("/messages/")
async def create_message(chatId: int, userId: int, messageText: str):
    conn = create_connection()
    if conn:
        try:
            insert_message(conn, chatId, userId, messageText)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al crear mensaje: {e}")
        finally:
            conn.close()
    return {"message": "Mensaje creado exitosamente"}

@router.get("/messages/{messageId}")
async def read_message(messageId: int):
    conn = create_connection()
    if conn:
        try:
            message = get_message(conn, messageId)
            if message is None:
                raise HTTPException(status_code=404, detail="Mensaje no encontrado")
            return {
                "messageId": message[0],
                "chatId": message[1],
                "senderId": message[2],
                "messageText": message[3],
                "timestamp": message[4]
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al obtener mensaje: {e}")
        finally:
            conn.close()

@router.get("/messages/chat/{chatId}")
async def read_messages_by_chat(chatId: int):
    conn = create_connection()
    if conn:
        try:
            messages = get_messages_by_chat(conn, chatId)
            return [
                {
                    "messageId": message[0],
                    "chatId": message[1],
                    "senderId": message[2],
                    "messageText": message[3],
                    "timestamp": message[4]
                }
                for message in messages
            ]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al obtener mensajes: {e}")
        finally:
            conn.close()
