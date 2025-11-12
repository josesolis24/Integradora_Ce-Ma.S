from funciones import limpiar_pantalla, pausa
from usuarios.usuarios import menu_usuarios
from productos.productos import menu_productos
from categorias.categorias import menu_categorias
from proveedores.proveedores import menu_proveedores
from ventas.ventas import menu_ventas
from compras.compras import menu_compras
from reportes.reportes import menu_reportes
from pedidos.pedidos import menu_pedidos
from login.login import login

def menu_principal():
    while True:
        limpiar_pantalla()
        print("====== SISTEMA DE INVENTARIO Ce&Ma ======")
        print("1. Gestión de Usuarios")
        print("2. Gestión de Productos")
        print("3. Gestión de Categorías")
        print("4. Gestión de Proveedores")
        print("5. Ventas")
        print("6. Compras")
        print("7. Reportes")
        print("8. Pedidos")
        print("9. Salir")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            menu_usuarios()
        elif opcion == "2":
            menu_productos()
        elif opcion == "3":
            menu_categorias()
        elif opcion == "4":
            menu_proveedores()
        elif opcion == "5":
            menu_ventas()
        elif opcion == "6":
            menu_compras()
        elif opcion == "7":
            menu_reportes()
        elif opcion == "8":
            menu_pedidos()
        elif opcion == "9":
            print("Saliendo del sistema... ¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")
            pausa()

if __name__ == "__main__":
    # Primero se ejecuta el login
    if login():
        menu_principal()
    else:
        print("\n🔒 Acceso denegado. Cerrando el sistema...")
