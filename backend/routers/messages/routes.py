from fastapi import APIRouter, HTTPException
from db.conn_db import create_connection
from .crud import insert_message, get_message, get_messages_by_chat
from .models import Message
from pdf import messagesGemini, insert_mensaje, insert_mensajeAI

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
        response_message = messagesGemini(request.content)
        
        conn = create_connection()
        # Insertar el mensaje del modelo en la base de datos
        insert_mensajeAI(conn, request.chatId, response_message)

        # Devolver la respuesta del modelo
        print(response_message)
        return {"response": response_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento: {e}")
    finally:
        conn.close()

   
   
    return {"response": response_message}