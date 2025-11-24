from conexion import conectar
import datetime

# 🔹 Crear reseña
def crear(usuario_id, titulo, descripcion, clasificacion, reseña):
    try:
        conn = conectar()
        if conn is None:
            print("❌ No se pudo conectar a la base de datos.")
            return False
        cursor = conn.cursor()
        sql = """
            INSERT INTO calificaciones_reseñas
            (usuario_id, titulo, descripcion, clasificacion, reseña, fecha)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        val = (usuario_id, titulo, descripcion, clasificacion, reseña)
        cursor.execute(sql, val)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al crear reseña: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# 🔹 Mostrar reseñas desde la base de datos
def mostrar(usuario_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
            SELECT id, titulo, descripcion, clasificacion, reseña, usuario_id
            FROM calificaciones_reseñas
            WHERE usuario_id = %s
        """
        cursor.execute(sql, (usuario_id,))
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print("Error al mostrar calificaciones y reseñas:", e)
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# 🔹 Cambiar reseña
def cambiar(id, titulo, descripcion, clasificacion, reseña):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
            UPDATE calificaciones_reseñas
            SET titulo = %s, descripcion = %s, clasificacion = %s, reseña = %s, fecha = NOW()
            WHERE id = %s
        """
        val = (titulo, descripcion, clasificacion, reseña, id)
        cursor.execute(sql, val)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al cambiar reseña: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# 🔹 Eliminar reseña
def eliminar(id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM calificaciones_reseñas WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar reseña: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
