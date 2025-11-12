import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Cambia si tu MySQL tiene contraseña
            database="inventario_cema"
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
