from pydantic import BaseModel
from backend.db.conn_db import create_connection, insert_mensaje

class Chat(BaseModel):
    mensajes: str
    usuario: str
    chat_id: int

def crear_mensaje(chat: Chat):
    # Utilizar la conexión ya creada
    if conn is not None:
        # Insertar el mensaje en la tabla
        insert_mensaje(conn, chat.usuario, chat.mensajes, chat.chat_id)

        # Cerrar la conexión a la base de datos
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

# Crear una instancia de `Chat`
nuevo_mensaje = Chat(
    usuario="Mauro",
    mensajes="Este es un mensaje",
    chat_id=1
)

# Conectar a la base de datos
conn = create_connection()

# Llamar a la función con la instancia creada
crear_mensaje(nuevo_mensaje)