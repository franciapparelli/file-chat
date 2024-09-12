import sqlite3
from sqlite3 import Error
from pydantic import BaseModel

class Chat(BaseModel):
    chatName: str
    userId: int

class ChatId(BaseModel):
    chatId: int

def create_chats_table(conn):
    try:
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS Chats (
            chatId INTEGER PRIMARY KEY AUTOINCREMENT,
            chatName TEXT NOT NULL,
            userId INTEGER,
            FOREIGN KEY (userId) REFERENCES Users(userId)
        );
        """
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        print("Tabla 'Chats' creada exitosamente.")
    except Error as e:
        print(f"Error al crear la tabla 'Chats': {e}")
