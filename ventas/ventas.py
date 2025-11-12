from conexionBD import crear_conexion
from funciones.funciones import limpiar_pantalla, pausa
from tabulate import tabulate  # ✅ Agregado

def menu_ventas():
    while True:
        limpiar_pantalla()
        print("---- Módulo de Ventas ----")
        print("1. Registrar venta")
        print("2. Mostrar ventas")
        print("3. Eliminar venta")
        print("4. Regresar al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_venta()
        elif opcion == "2":
            mostrar_ventas()
        elif opcion == "3":
            eliminar_venta()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")
            pausa()

def registrar_venta():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    id_producto = input("ID del producto vendido: ")
    cantidad = int(input("Cantidad vendida: "))
    fecha = input("Fecha (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO ventas (id_producto, cantidad, fecha) VALUES (%s, %s, %s)", 
                   (id_producto, cantidad, fecha))
    conexion.commit()
    conexion.close()
    print("✅ Venta registrada con éxito.")
    pausa()

def mostrar_ventas():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, id_producto, cantidad, fecha FROM ventas")
    ventas = cursor.fetchall()

    if not ventas:
        print("⚠️ No hay ventas registradas.")
    else:
        print("\n=== LISTA DE VENTAS ===")
        print(tabulate(ventas, headers=["ID", "Producto ID", "Cantidad", "Fecha"], tablefmt="grid"))

    conexion.close()
    pausa()

def eliminar_venta():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    idv = input("ID de la venta a eliminar: ")
    cursor.execute("DELETE FROM ventas WHERE id = %s", (idv,))
    conexion.commit()
    conexion.close()
    print("🗑️ Venta eliminada correctamente.")
    pausa()
