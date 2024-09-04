import sqlite3
from sqlite3 import Error
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

def create_users_table(conn):
    try:
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS Users (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        """
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        print("Tabla 'Users' creada exitosamente.")
    except Error as e:
        print(f"Error al crear la tabla 'Users': {e}")
