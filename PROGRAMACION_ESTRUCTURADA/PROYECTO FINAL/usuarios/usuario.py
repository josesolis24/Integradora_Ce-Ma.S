import mysql.connector
from mysql.connector import Error
import datetime
import hashlib

def hash_password(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def registrar(nombre, apellidos, email, contrasena):
    from conexion import conectar  # ✅ Import local para evitar ciclo
    try:
        conexion = conectar()
        if conexion is None:
            print("No se pudo conectar a la base de datos.")
            return False

        cursor = conexion.cursor()
        fecha = datetime.datetime.now()
        contrasena = hash_password(contrasena)

        sql = "INSERT INTO usuarios(nombre, apellidos, email, password, fecha) VALUES (%s, %s, %s, %s, %s)"
        val = (nombre, apellidos, email, contrasena, fecha)

        cursor.execute(sql, val)
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error en registrar: {e}")
        return False
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def inicio_sesion(email, contrasena):
    from conexion import conectar  # ✅ Import local para evitar ciclo
    try:
        conexion = conectar()
        if conexion is None:
            print("No se pudo conectar a la base de datos.")
            return None

        cursor = conexion.cursor()
        contrasena = hash_password(contrasena)
        
        sql = "SELECT * FROM usuarios WHERE email=%s AND password=%s"
        val = (email, contrasena)
        cursor.execute(sql, val)
        registro = cursor.fetchone()
        return registro
    except Exception as e:
        print(f"Error en inicio de sesión: {e}")
        return None
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
