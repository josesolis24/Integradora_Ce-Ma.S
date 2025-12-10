from conexionBD import crear_conexion
from funciones.funciones import limpiar_pantalla, pausa
from tabulate import tabulate  # ✅ Tablas

def menu_reportes():
    while True:
        limpiar_pantalla()
        print("---- Módulo de Reportes ----")
        print("1. Productos con bajo stock")
        print("2. Ventas por fecha")
        print("3. Compras por fecha")
        print("4. Regresar al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            reporte_bajo_stock()
        elif opcion == "2":
            reporte_ventas_fecha()
        elif opcion == "3":
            reporte_compras_fecha()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")
            pausa()

def reporte_bajo_stock():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, stock FROM productos WHERE stock < 5")
    productos = cursor.fetchall()

    if not productos:
        print("✅ No hay productos con stock bajo.")
    else:
        print("\n=== PRODUCTOS CON STOCK BAJO ===")
        print(tabulate(productos, headers=["Nombre", "Stock"], tablefmt="grid"))

    conexion.close()
    pausa()

def reporte_ventas_fecha():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    fecha = input("Fecha (DD-MM-YYYY): ")
    cursor.execute("SELECT id, id_producto, cantidad, fecha FROM ventas WHERE fecha = %s", (fecha,))
    ventas = cursor.fetchall()

    if not ventas:
        print("⚠️ No hay ventas registradas en esa fecha.")
    else:
        print(f"\n=== VENTAS DEL DÍA {fecha} ===")
        print(tabulate(ventas, headers=["ID", "Producto ID", "Cantidad", "Fecha"], tablefmt="grid"))

    conexion.close()
    pausa()

def reporte_compras_fecha():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    fecha = input("Fecha (DD-MM-YYYY): ")
    cursor.execute("SELECT id, id_producto, cantidad, fecha FROM compras WHERE fecha = %s", (fecha,))
    compras = cursor.fetchall()

    if not compras:
        print("⚠️ No hay compras registradas en esa fecha.")
    else:
        print(f"\n=== COMPRAS DEL DÍA {fecha} ===")
        print(tabulate(compras, headers=["ID", "Producto ID", "Cantidad", "Fecha"], tablefmt="grid"))

    conexion.close()
    pausa()
