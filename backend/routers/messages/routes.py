from fastapi import APIRouter, HTTPException
from db.conn_db import create_connection
from .crud import insert_message, get_message, get_messages_by_chat, delete_message
from .models import Message, MessageId
from pdf import messagesGemini

router = APIRouter()

@router.post("/")
async def create_message(message: Message):
    conn = create_connection()
    if conn:
        try:
            response = await messagesGemini(message.content)
            insert_message(conn, message.chatId, message.userId, message.content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al crear mensaje: {e}")
        finally:
            conn.close()
    return {"message": "Mensaje creado exitosamente", "response": response}

@router.get("/{messageId}")
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

@router.get("/chat/{chatId}")
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

@router.post("/gemini")
async def create_message(message: Message):
    conn = create_connection()
    if conn:
        try:
            response = messagesGemini(message.content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al crear mensaje: {e}")
        finally:
            conn.close()
    return {"response": response}

@router.post("/delete")
async def delete_messages(messageId: MessageId):
    conn = create_connection()
    if conn:
        try:
            chats = delete_message(messageId.messageId, conn)
            print(messageId.messageId)
            return {"response": chats}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al obtener chats: {e}")
        finally:
            conn.close()