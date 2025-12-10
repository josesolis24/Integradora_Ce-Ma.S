from conexionBD import crear_conexion
from funciones.funciones import limpiar_pantalla, pausa
from tabulate import tabulate  # Para mostrar tabla



# ==========================
#  USUARIO ACTUAL DEL SISTEMA
# ==========================
# 👉 Cámbialo si tu proyecto ya tiene login
usuario_actual = "admin"


def menu_categorias():
    while True:
        limpiar_pantalla()
        print("---- Módulo de Categorías ----")
        print("1. Agregar categoría")
        print("2. Mostrar categorías")
        print("3. Eliminar categoría")
        print("4. Regresar al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_categoria()
        elif opcion == "2":
            mostrar_categorias()
        elif opcion == "3":
            eliminar_categoria()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")
            pausa()


# ==========================
#   AGREGAR CATEGORÍA
# ==========================
def agregar_categoria():
    print(">>> SOY categoriasGUI.py — SI ME VES, ESTE ES EL ARCHIVO CORRECTO") 
    print(">>> DEBUG: usuario_actual =", usuario_actual)
    print(">>> DEBUG: ESTOY A PUNTO DE INSERTAR")

    conexion = crear_conexion()
    if not conexion:
        print("Error al conectar.")
        return

    cursor = conexion.cursor()

    nombre = input("Nombre de la categoría: ")

    # Guardar quién creó y actualizó
    creado_por = usuario_actual
    actualizado_por = usuario_actual

    sql = """
        INSERT INTO categorias (nombre, creado_por, actualizado_por)
        VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (nombre, creado_por, actualizado_por))
    conexion.commit()
    conexion.close()

    print("Categoría agregada correctamente.")
    pausa()


# ==========================
#   MOSTRAR CATEGORÍAS
# ==========================
def mostrar_categorias():
    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_categoria, nombre, creado_por, actualizado_por FROM categorias")
    categorias = cursor.fetchall()

    if categorias:
        encabezados = ["ID", "Nombre", "Creado por", "Actualizado por"]
        print(tabulate(categorias, headers=encabezados, tablefmt="grid"))
    else:
        print("No hay categorías registradas.")

    conexion.close()
    pausa()


# ==========================
#   ELIMINAR CATEGORÍA
# ==========================
def eliminar_categoria():
    conexion = crear_conexion()
    cursor = conexion.cursor()

    id_cat = input("ID de la categoría a eliminar: ")

    cursor.execute("DELETE FROM categorias WHERE id_categoria = %s", (id_cat,))
    conexion.commit()
    conexion.close()

    print("Categoría eliminada.")
    pausa()

