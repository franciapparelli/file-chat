import sqlite3
from sqlite3 import Error

def create_messages_table(conn):
    try:
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS Messages (
            messageId INTEGER PRIMARY KEY AUTOINCREMENT,
            chatId INTEGER,
            senderId INTEGER,
            messageText TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chatId) REFERENCES Chats(chatId),
            FOREIGN KEY (senderId) REFERENCES Users(userId)
        );
        """
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        print("Tabla 'Messages' creada exitosamente.")
    except Error as e:
        print(f"Error al crear la tabla 'Messages': {e}")
