from conexionBD import crear_conexion
from funciones.funciones import limpiar_pantalla, pausa
from tabulate import tabulate  # ✅ Para mostrar tablas

def menu_proveedores():
    while True:
        limpiar_pantalla()
        print("---- Módulo de Proveedores ----")
        print("1. Agregar proveedor")
        print("2. Mostrar proveedores")
        print("3. Eliminar proveedor")
        print("4. Regresar al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_proveedor()
        elif opcion == "2":
            mostrar_proveedores()
        elif opcion == "3":
            eliminar_proveedor()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")
            pausa()

def agregar_proveedor():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    nombre = input("Nombre del proveedor: ")
    telefono = input("Teléfono: ")
    direccion = input("Dirección: ")
    cursor.execute("INSERT INTO proveedores (nombre, telefono, direccion) VALUES (%s, %s, %s)", 
                   (nombre, telefono, direccion))
    conexion.commit()
    conexion.close()
    print("✅ Proveedor agregado correctamente.")
    pausa()

def mostrar_proveedores():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, telefono, direccion FROM proveedores")
    proveedores = cursor.fetchall()

    if not proveedores:
        print("⚠️ No hay proveedores registrados.")
    else:
        print("\n=== LISTA DE PROVEEDORES ===")
        encabezados = ["ID", "Nombre", "Teléfono", "Dirección"]
        print(tabulate(proveedores, headers=encabezados, tablefmt="grid"))

    conexion.close()
    pausa()

def eliminar_proveedor():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    idp = input("ID del proveedor a eliminar: ")
    cursor.execute("DELETE FROM proveedores WHERE id = %s", (idp,))
    conexion.commit()
    conexion.close()
    print("🗑️ Proveedor eliminado correctamente.")
    pausa()
