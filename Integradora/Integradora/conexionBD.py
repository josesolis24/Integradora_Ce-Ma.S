import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="inventario_cema",
            autocommit=True  
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
