import sqlite3
from sqlite3 import Error

def insert_chat(conn, chatName, userId):
    try:
        sql_insert = """
        INSERT INTO Chats (chatName, userId)
        VALUES (?, ?);
        """
        cursor = conn.cursor()
        cursor.execute(sql_insert, (chatName, userId))
        conn.commit()
        print("Chat insertado exitosamente.")
    except Error as e:
        print(f"Error al insertar el chat: {e}")

def get_chat(conn, userId):
    try:
        sql_select = """
        SELECT * FROM Chats WHERE userId = ?;
        """
        cursor = conn.cursor()
        cursor.execute(sql_select, (userId,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener el chat: {e}")
        return None

def get_all_chats(conn):
    try:
        sql_select_all = """
        SELECT * FROM Chats;
        """
        cursor = conn.cursor()
        cursor.execute(sql_select_all)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener los chats: {e}")
        return None

def delete_chat(chatId, conn):
    try:
        sql_delete_chat = """
        DELETE
            FROM Chats
            WHERE chatId = ?;
        """
        cursor = conn.cursor()
        cursor.execute(sql_delete_chat, (chatId,))
        conn.commit()
        return "Se ha borrado el chat correctamente"
    except Error as e:
        print(f"Error al borrar el chat: {e}")
        return None
    

# @app.delete("/delete")
# async def delete_chat(chat_id: int = Query(..., description="ID del chat que se desea eliminar")):
#     print(chat_id)
#     conn = create_connection()
#     if conn is None:
#         return {"error": "No se pudo conectar a la base de datos."}
   
#     response = delete_msg(conn, chat_id)
#     return response

# def delete_msg(conn, chat_id):
#     try:
#         sql_delete = """
#         DELETE
#             FROM tabla_chat
#             WHERE chat_id = ?;
#         """
#         cursor = conn.cursor()
#         cursor.execute(sql_delete, (chat_id,))
#         conn.commit()
#         print(f"Chat con chat_id {chat_id} eliminado exitosamente.")
#     except Error as e:
#         print(f"Error al eliminar el chat con chat_id {chat_id}: {e}")
#     finally:
#         if conn:
#             conn.close()  # Cierra la conexión