import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bd_videojuegos"
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"\n❌ Error al conectar con la base de datos: {e}")
    return None
