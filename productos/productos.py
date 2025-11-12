from conexionBD import crear_conexion
from funciones.funciones import limpiar_pantalla, pausa
from tabulate import tabulate  # ✅ Agregado para mostrar tablas de forma bonita


def menu_productos():
    while True:
        limpiar_pantalla()
        print("---- Módulo de Productos ----")
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Eliminar producto")
        print("4. Regresar al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            eliminar_producto()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")
            pausa()


def agregar_producto():
    conexion = crear_conexion()
    if not conexion:
        print("Error al conectar.")
        return

    cursor = conexion.cursor()
    nombre = input("Nombre: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))

    cursor.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
        (nombre, precio, stock)
    )
    conexion.commit()
    conexion.close()
    print("✅ Producto agregado correctamente.")
    pausa()


def mostrar_productos():
    conexion = crear_conexion()
    if not conexion:
        print("Error al conectar.")
        pausa()
        return

    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, precio, stock FROM productos")
    productos = cursor.fetchall()

    if not productos:
        print("⚠️ No hay productos registrados.")
    else:
        encabezados = ["ID", "Nombre", "Precio", "Stock"]
        print("\n=== LISTA DE PRODUCTOS ===")
        print(tabulate(productos, headers=encabezados, tablefmt="grid", floatfmt=".2f"))

    conexion.close()
    pausa()


def eliminar_producto():
    conexion = crear_conexion()
    if not conexion:
        print("Error al conectar.")
        pausa()
        return

    cursor = conexion.cursor()
    idp = input("ID del producto a eliminar: ")

    cursor.execute("DELETE FROM productos WHERE id = %s", (idp,))
    conexion.commit()
    conexion.close()
    print("🗑️ Producto eliminado correctamente.")
    pausa()
