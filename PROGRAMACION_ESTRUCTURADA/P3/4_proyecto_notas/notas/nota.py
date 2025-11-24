from conexion import *
import datetime

# Asegúrate de crear una conexión a la base de datos aquí
conexion = conectar()  # Suponiendo que tienes una función conectar() en tu módulo conexion.py

def crear(usuario_id, titulo, descripcion):
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO notas(usuario_id, titulo, descripcion, fecha) VALUES (%s, %s, %s, NOW())"
        val = (usuario_id, titulo, descripcion)
        cursor.execute(sql, val)
        conexion.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error al crear nota: {e}")
def mostrar(usuario_id):
    try:
        cursor = conexion.cursor()
        sql = "SELECT * FROM notas WHERE usuario_id = %s"
        cursor.execute(sql, (usuario_id,))
        lista = cursor.fetchall()
        cursor.close()
        return lista
    except Exception as e:
        print(f"Error al mostrar notas: {e}")
def cambiar(id, titulo, descripcion):
    try:
        cursor = conexion.cursor()
        sql = "UPDATE notas SET titulo = %s, descripcion = %s, fecha = NOW() WHERE id = %s"
        val = (titulo, descripcion, id)
        cursor.execute(sql, val)
        conexion.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error al cambiar nota: {e}")
def borrar(id):
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM notas WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error al borrar nota: {e}")
        return False
