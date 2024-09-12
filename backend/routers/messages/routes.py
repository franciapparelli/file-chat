from fastapi import APIRouter, HTTPException
from db.conn_db import create_connection
from .crud import insert_message, get_message, get_messages_by_chat, delete_message
from .models import Message, MessageId
from pdf import messagesGemini, insert_mensaje, insert_mensajeAI

router = APIRouter()

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
                    "userId": message[2],
                    "content": message[3],
                    "timestamp": message[4]
                }
                for message in messages
            ]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al obtener mensajes: {e}")
        finally:
            conn.close()

@router.post("/gemini")
async def chat_msg(request: Message):
    """json
    {
        chat_id: num_id
        userId: userId,
        content: content
    }
    """
    conn = create_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error al conectar con la base de datos.")
    
    try:
        # Insertar el mensaje del usuario
        insert_mensaje(conn, request.chatId, request.userId, request.content)
        
        # Obtener respuesta del modelo
        conn = create_connection()
        response_message = messagesGemini(conn, request.content, request.chatId)
        
        conn = create_connection()
        # Insertar el mensaje del modelo en la base de datos
        insert_mensajeAI(conn, request.chatId, response_message)

        return {"response": response_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento: {e}")

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