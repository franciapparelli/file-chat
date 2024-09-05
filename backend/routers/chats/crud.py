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
