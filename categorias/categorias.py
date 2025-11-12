from conexionBD import crear_conexion
from funciones.funciones import limpiar_pantalla, pausa
from tabulate import tabulate  # 🔹 Import para mostrar como tabla


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


def agregar_categoria():
    conexion = crear_conexion()
    if not conexion:
        print("Error al conectar.")
        return
    cursor = conexion.cursor()
    nombre = input("Nombre de la categoría: ")
    cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
    conexion.commit()
    conexion.close()
    print("Categoría agregada correctamente.")
    pausa()


def mostrar_categorias():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    if categorias:
        # 🔹 Mostrar los resultados como tabla
        encabezados = ["ID", "Nombre"]
        print(tabulate(categorias, headers=encabezados, tablefmt="grid"))
    else:
        print("No hay categorías registradas.")

    conexion.close()
    pausa()


def eliminar_categoria():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    id_cat = input("ID de la categoría a eliminar: ")
    cursor.execute("DELETE FROM categorias WHERE id = %s", (id_cat,))
    conexion.commit()
    conexion.close()
    print("Categoría eliminada.")
    pausa()
