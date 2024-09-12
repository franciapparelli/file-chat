import sqlite3
from sqlite3 import Error

def insert_message(conn, chatId, userId, content):
    try:
        sql_insert = """
        INSERT INTO Messages (chatId, userId, content)
        VALUES (?, ?, ?);
        """
        cursor = conn.cursor()
        cursor.execute(sql_insert, (chatId, userId, content))
        conn.commit()
        print("Mensaje insertado exitosamente.")
    except Error as e:
        print(f"Error al insertar el mensaje: {e}")

def get_message(conn, messageId):
    try:
        sql_select = """
        SELECT * FROM Messages WHERE messageId = ?;
        """
        cursor = conn.cursor()
        cursor.execute(sql_select, (messageId,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error al obtener el mensaje: {e}")
        return None

def get_messages_by_chat(conn, chatId):
    try:
        sql_select = """
        SELECT * FROM Messages WHERE chatId = ? ORDER BY timestamp;
        """
        cursor = conn.cursor()
        cursor.execute(sql_select, (chatId,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener los mensajes: {e}")
        return None

def delete_message(messageId, conn):
    try:
        sql_delete_message = """
        DELETE
            FROM Messages
            WHERE messageId = ?;
        """
        cursor = conn.cursor()
        cursor.execute(sql_delete_message, (messageId,))
        conn.commit()
        return "Se ha borrado el mensaje correctamente"
    except Error as e:
        print(f"Error al borrar el chat: {e}")
        return None
