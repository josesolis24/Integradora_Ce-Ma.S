import mysql.connector
from mysql.connector import Error
from conexion import conectar  # Tu función para conectar a la BD

videojuegos = []  # Lista local en Python


# Cargar videojuegos desde la base de datos
def cargar_videojuegos_desde_bd():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, precio, plataforma, descripcion, fecha_lanzamiento FROM videojuegos")
        registros = cursor.fetchall()

        videojuegos.clear()
        for fila in registros:
            videojuegos.append({
                "id": fila["id"],
                "nombre": fila["nombre"],
                "precio": fila["precio"],
                "plataforma": fila["plataforma"],
                "descripcion": fila["descripcion"],
                "fecha_lanzamiento": fila["fecha_lanzamiento"],  # Puede ser None
            })
        print("📂 Videojuegos cargados desde la base de datos.")
    except Error as e:
        print(f"❌ Error al cargar videojuegos: {e}")
    finally:
        try:
            if conn.is_connected():
                cursor.close()
                conn.close()
        except Exception:
            pass


# Guardar un videojuego en la BD
def guardar_videojuego_en_bd(nombre, precio, plataforma, descripcion, fecha_lanzamiento):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
            INSERT INTO videojuegos (nombre, precio, plataforma, descripcion, fecha_lanzamiento)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, precio, plataforma, descripcion, fecha_lanzamiento)
        cursor.execute(query, valores)
        conn.commit()
        print("💾 Videojuego guardado en la base de datos.")
    except Error as e:
        print(f"❌ Error al guardar en la base de datos: {e}")
    finally:
        try:
            if conn.is_connected():
                cursor.close()
                conn.close()
        except Exception:
            pass


# Vaciar tabla de la BD
def vaciar_bd_videojuegos():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM videojuegos")
        conn.commit()
        print("🧹 Tabla videojuegos vaciada en la base de datos.")
    except Error as e:
        print(f"❌ Error al vaciar la tabla en la BD: {e}")
    finally:
        try:
            cursor.close()
            if conn.is_connected():
                conn.close()
        except Exception:
            pass


# Función corregida para vaciar lista y tabla con confirmación
def vaciar_lista():
    confirmar = input("¿Estás seguro de vaciar toda la lista de videojuegos y borrar la tabla en la base de datos? (s/n): ")
    if confirmar.lower() == 's':
        vaciar_bd_videojuegos()
        videojuegos.clear()
        print("🧹 Lista local de videojuegos vaciada.\n")
    else:
        print("Operación cancelada. No se vació la lista.")


# Agregar videojuego con parámetros
def agregar_videojuego(nombre, precio, plataforma, descripcion, fecha_lanzamiento):
    try:
        precio_float = float(precio)
    except ValueError:
        print("❌ Error: el precio debe ser un número.")
        return
    guardar_videojuego_en_bd(nombre, precio_float, plataforma, descripcion, fecha_lanzamiento)
    cargar_videojuegos_desde_bd()


# Mostrar videojuegos con formato tabla y precio con separadores de miles
def mostrar_videojuegos():
    if not videojuegos:
        print("📭 No hay videojuegos cargados.")
    else:
        print("\n=== Lista de Videojuegos ===")
        print(f"{'ID':<5} {'Nombre':<25} {'Precio':<12} {'Plataforma':<15} {'Descripción':<30} {'Fecha Lanzamiento':<15}")
        print("-" * 107)
        for v in videojuegos:
            descripcion_corta = (v['descripcion'][:27] + '...') if v['descripcion'] and len(v['descripcion']) > 30 else (v['descripcion'] or "")
            try:
                precio = float(v['precio'])
            except (ValueError, TypeError):
                precio = 0.0
            fecha = v['fecha_lanzamiento']
            fecha_str = "N/A" if fecha is None else str(fecha)
            print(f"{v['id']:<5} {v['nombre']:<25} {f'${precio:,.2f}':<12} {v['plataforma']:<15} {descripcion_corta:<30} {fecha_str:<15}")


# Buscar videojuego por nombre con tabla formateada y precio con separadores de miles
def buscar_videojuego(nombre_buscar=None):
    if nombre_buscar is None:
        nombre_buscar = input("Ingrese el nombre del videojuego a buscar: ").lower()
    else:
        nombre_buscar = nombre_buscar.lower()
    encontrados = [v for v in videojuegos if nombre_buscar in v['nombre'].lower()]
    if encontrados:
        print("\n=== Resultados de búsqueda ===")
        print(f"{'ID':<5} {'Nombre':<25} {'Precio':<12} {'Plataforma':<15} {'Descripción':<30} {'Fecha Lanzamiento':<15}")
        print("-" * 107)
        for v in encontrados:
            descripcion_corta = (v['descripcion'][:27] + '...') if v['descripcion'] and len(v['descripcion']) > 30 else (v['descripcion'] or "")
            try:
                precio = float(v['precio'])
            except (ValueError, TypeError):
                precio = 0.0
            fecha = v['fecha_lanzamiento']
            fecha_str = "N/A" if fecha is None else str(fecha)
            print(f"{v['id']:<5} {v['nombre']:<25} {f'${precio:,.2f}':<12} {v['plataforma']:<15} {descripcion_corta:<30} {fecha_str:<15}")
    else:
        print("❌ No se encontraron videojuegos con ese nombre.")


# Modificar videojuego usando índice (de la lista)
def modificar_videojuego(indice, nombre, precio, plataforma, descripcion, fecha_lanzamiento):
    if indice < 0 or indice >= len(videojuegos):
        print("❌ Índice inválido.")
        return
    try:
        precio_float = float(precio)
    except ValueError:
        print("❌ Error: el precio debe ser un número.")
        return
    videojuego = videojuegos[indice]
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
            UPDATE videojuegos
            SET nombre=%s, precio=%s, plataforma=%s, descripcion=%s, fecha_lanzamiento=%s
            WHERE id=%s
        """
        valores = (nombre, precio_float, plataforma, descripcion, fecha_lanzamiento, videojuego['id'])
        cursor.execute(query, valores)
        conn.commit()
        print("✏️ Videojuego modificado correctamente.")
        cargar_videojuegos_desde_bd()
    except Error as e:
        print(f"❌ Error al modificar videojuego: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# Eliminar videojuego usando índice (de la lista)
def eliminar_videojuego(indice):
    if indice < 0 or indice >= len(videojuegos):
        print("❌ Índice inválido.")
        return
    videojuego = videojuegos[indice]
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM videojuegos WHERE id = %s", (videojuego['id'],))
        conn.commit()
        print("🗑️ Videojuego eliminado correctamente.")
        cargar_videojuegos_desde_bd()
    except Error as e:
        print(f"❌ Error al eliminar videojuego: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()