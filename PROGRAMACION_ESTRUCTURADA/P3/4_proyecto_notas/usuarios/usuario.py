import mysql.connector
from mysql.connector import Error
import datetime
import hashlib
from conexion import *

def hash_password(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def registrar(nombre, apellidos, email, contrasena):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        fecha = datetime.datetime.now()
        contrasena = hash_password(contrasena)

        sql = "INSERT INTO usuarios(nombre, apellidos, email, password, fecha) VALUES (%s, %s, %s, %s, %s)"
        val = (nombre, apellidos, email, contrasena, fecha)

        cursor.execute(sql, val)
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error en registrar: {e}")  # ⬅️ esto debe aparecer
        return False


import hashlib
from conexion import *

def inicio_sesion(email, contrasena):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        # Encriptar la contraseña como al registrar
        contrasena = hashlib.sha256(contrasena.encode()).hexdigest()
        
        sql = "SELECT * FROM usuarios WHERE email=%s AND password=%s"
        val = (email, contrasena)
        cursor.execute(sql, val)
        registro = cursor.fetchone()  # Esto devuelve una tupla o None

        return registro  # Puede ser una tupla (usuario encontrado) o None
    except Exception as e:
        print(f"Error en inicio de sesión: {e}")
        return None

