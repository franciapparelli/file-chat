import sqlite3
from sqlite3 import Error

def create_connection():
    database = "db/chat_db.db"

    db_file = database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conexión a SQLite establecida: {db_file}")
    except Error as e:
        print(f"Error al conectar a SQLite: {e}")
    
    return conn

def makeQuery(query):
    conn = create_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
    except Error as e:
        print(f"{e}")

# def insert_mensaje(conn, usuario, mensajes, chat_id):
#     try:
#         sql_insert = """
#         INSERT INTO tabla_chat (usuario, mensaje, chat_id)
#         VALUES (?, ?, ?);
#         """
#         cursor = conn.cursor()
#         cursor.execute(sql_insert, (usuario, mensajes, chat_id))
#         conn.commit()
#         print("Mensaje insertado exitosamente.")
#     except Error as e:
#         print(f"Error al insertar el mensaje: {e}")

# Conectar y crear la tabla
conn = create_connection()

# if conn:
#     makeQuery(""" 

# """)
#     conn.close()