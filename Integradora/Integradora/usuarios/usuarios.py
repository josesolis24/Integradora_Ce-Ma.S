from conexionBD import crear_conexion
from funciones.funciones import pausa, limpiar_pantalla
from tabulate import tabulate  # ✅ Tablas

def menu_usuarios():
    while True:
        limpiar_pantalla()
        print("---- Módulo de Usuarios ----")
        print("1. Registrar usuario")
        print("2. Mostrar usuarios")
        print("3. Eliminar usuario")
        print("4. Regresar al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            mostrar_usuarios()
        elif opcion == "3":
            eliminar_usuario()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")
            pausa()

def registrar_usuario():
    conexion = crear_conexion()
    if not conexion:
        print("Error de conexión.")
        return
    cursor = conexion.cursor()
    nombre = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (nombre, contraseña))
    conexion.commit()
    conexion.close()
    print("✅ Usuario registrado con éxito.")
    pausa()

def mostrar_usuarios():
    conexion = crear_conexion()
    if not conexion:
        print("Error de conexión.")
        return
    cursor = conexion.cursor()
    cursor.execute("SELECT id, username FROM usuarios")
    usuarios = cursor.fetchall()

    if not usuarios:
        print("⚠️ No hay usuarios registrados.")
    else:
        print("\n=== LISTA DE USUARIOS ===")
        print(tabulate(usuarios, headers=["ID", "Nombre de Usuario"], tablefmt="grid"))

    conexion.close()
    pausa()

def eliminar_usuario():
    conexion = crear_conexion()
    if not conexion:
        print("Error de conexión.")
        return
    cursor = conexion.cursor()
    id_usuario = input("ID del usuario a eliminar: ")
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
    conexion.commit()
    conexion.close()
    print("🗑️ Usuario eliminado correctamente.")
    pausa()
