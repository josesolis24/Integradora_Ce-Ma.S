from conexionBD import crear_conexion
from funciones.funciones import limpiar_pantalla, pausa
from tabulate import tabulate  # 🔹 Import para mostrar los datos en tabla


def menu_compras():
    while True:
        limpiar_pantalla()
        print("---- Módulo de Compras ----")
        print("1. Registrar compra")
        print("2. Mostrar compras")
        print("3. Eliminar compra")
        print("4. Regresar al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_compra()
        elif opcion == "2":
            mostrar_compras()
        elif opcion == "3":
            eliminar_compra()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")
            pausa()


def registrar_compra():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    id_producto = input("ID del producto comprado: ")
    cantidad = int(input("Cantidad comprada: "))
    fecha = input("Fecha (DD-MM-YYYY): ")
    cursor.execute("INSERT INTO compras (id_producto, cantidad, fecha) VALUES (%s, %s, %s)", 
                   (id_producto, cantidad, fecha))
    conexion.commit()
    conexion.close()
    print("Compra registrada con éxito.")
    pausa()


def mostrar_compras():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM compras")
    compras = cursor.fetchall()

    if compras:
        # 🔹 Mostrar resultados en formato tabla
        encabezados = ["ID", "ID Producto", "Cantidad", "Fecha"]
        print(tabulate(compras, headers=encabezados, tablefmt="grid"))
    else:
        print("No hay compras registradas.")

    conexion.close()
    pausa()


def eliminar_compra():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    idc = input("ID de la compra a eliminar: ")
    cursor.execute("DELETE FROM compras WHERE id = %s", (idc,))
    conexion.commit()
    conexion.close()
    print("Compra eliminada.")
    pausa()
