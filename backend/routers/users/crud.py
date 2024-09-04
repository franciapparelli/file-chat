import sqlite3
from sqlite3 import Error

def insert_user(conn, username, password):
    try:
        sql_insert = """
        INSERT INTO Users (username, password)
        VALUES (?, ?);
        """
        cursor = conn.cursor()
        cursor.execute(sql_insert, (username, password))
        conn.commit()
        print("Usuario insertado exitosamente.")
    except sqlite3.Error as e:  # Cambia sqlite3.Error por el módulo adecuado si no es sqlite
        print(f"Error al insertar el usuario: {e}")
    finally:
        cursor.close()  # Cerrar el cursor después de su uso


def get_user(conn, username):
    try:
        sql_select = """
        SELECT * FROM Users WHERE username = ?;
        """
        cursor = conn.cursor()
        cursor.execute(sql_select, (username,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error al obtener el usuario: {e}")
        return None


def get_all_users(conn):
    try:
        sql_select = """
        SELECT * FROM Users;
        """
        print(conn.cursor)
        cursor = conn.cursor()
        cursor.execute(sql_select)
        rows = cursor.fetchall()  # Obtener todas las filas
        print(rows)
        return rows  # Retornar todas las filas como una lista de tuplas
    except Error as e:
        print(f"Error al obtener el usuario: {e}")
        return None