import mysql.connector
from mysql.connector import Error
import getpass
from datetime import datetime

import funciones
from usuarios import usuario
from Calificaciones_Reseñas_Usuarios import Calificaciones_Reseñas_Usuarios
from conexion import conectar
from funciones import esperarTecla

from videojuegos.videojuegosmodulo import (
    agregar_videojuego,
    mostrar_videojuegos,
    buscar_videojuego,
    modificar_videojuego,
    eliminar_videojuego,
    vaciar_lista,
    cargar_videojuegos_desde_bd  
)


def validar_fecha(fecha_str):
    if fecha_str == "":
        return True  # Permitimos dejar vacío
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def pedir_fecha_lanzamiento():
    while True:
        fecha_lanzamiento = input("Fecha de lanzamiento (AAAA-MM-DD) (deja vacío si no aplica): ").strip()
        if validar_fecha(fecha_lanzamiento):
            return fecha_lanzamiento
        else:
            print("Fecha inválida. El formato debe ser AAAA-MM-DD. Intenta de nuevo.")


def main():
    cargar_videojuegos_desde_bd()

    opcion = True
    while opcion:
        funciones.borrarPantalla()
        opcion = funciones.menu_usuarios()

        if opcion == "1" or opcion.upper() == "REGISTRO":
            funciones.borrarPantalla()
            print("\n \t ..:: Registro en el Sistema ::..")
            nombre = input("\t ¿Cuál es tu nombre?: ").upper().strip()
            apellidos = input("\t ¿Cuáles son tus apellidos?: ").upper().strip()
            email = input("\t Ingresa tu email: ").lower().strip()
            password = getpass.getpass("\t Ingresa tu contraseña: ").strip()

            try:
                lista_usuario = usuario.registrar(nombre, apellidos, email, password)
                if lista_usuario:
                    print(f"\n\t{nombre} {apellidos} se registró correctamente con el email: {email}")
                else:
                    print("\n\tNo fue posible registrar el usuario. Verifica si el correo ya está registrado o inténtalo más tarde.")
            except Exception as e:
                print(f"\n\tOcurrió un error durante el registro: {e}")

            funciones.esperarTecla()

        elif opcion == "2" or opcion.upper() == "LOGIN":
            funciones.borrarPantalla()
            print("\n \t ..:: Inicio de Sesión ::..")
            email = input("\t Ingresa tu E-mail: ").lower().strip()
            password = getpass.getpass("\t Ingresa tu contraseña: ").strip()

            try:
                lista_usuario = usuario.inicio_sesion(email, password)
                if lista_usuario:
                    usuario_id = lista_usuario[0]
                    menu_Calificaciones_Reseñas_Usuarios_videojuegos(usuario_id)
                else:
                    print("\n\tE-mail y/o contraseña incorrectos. Por favor verifica y vuelve a intentar.")
            except Exception as e:
                print(f"\n\tOcurrió un error durante el inicio de sesión: {e}")

            funciones.esperarTecla()

        elif opcion == "3" or opcion.upper() == "SALIR":
            print("Terminó la ejecución del sistema.")
            opcion = False
            funciones.esperarTecla()
        else:
            print("Opción no válida.")
            funciones.esperarTecla()


def menu_Calificaciones_Reseñas_Usuarios_videojuegos(usuario_id):
    while True:
        print("\n\t..::: 📚 MENÚ DE CALIFICACION RESEÑA  Y VIDEOJUEGOS 📚 :::..")
        print("\t1️⃣ Calificaciones y Reseñas de Usuarios")
        print("\t2️⃣ Videojuegos")
        print("\t3️⃣ Salir")
        opcion = input("\tSelecciona una opción: ").strip()

        if opcion == "1" or opcion.upper() == "CALIFICACIONES y RESEÑAS":
            menu_Calificaciones_Reseñas_Usuarios(usuario_id)
        elif opcion == "2" or opcion.upper() == "VIDEOJUEGOS":
            menu_videojuegos()
        elif opcion == "3" or opcion.upper() == "SALIR":
            print("\n👋 Cerrando menú de clasificacion  y Videojuegos...")
            break
        else:
            print("\n\t❌ Opción no válida.")
            funciones.esperarTecla()


def menu_Calificaciones_Reseñas_Usuarios(usuario_id):
    while True:
        funciones.borrarPantalla()
        opcion = funciones.menu_Calificaciones_Reseñas_Usuarios()

        if opcion == "1" or opcion.upper() == "CREAR":
            funciones.borrarPantalla()
            print(f"\n\t .:: Crear Calificaciones y Reseñas del Usuarios ::.")
            titulo = input("\tTitulo: ")
            descripcion = input("\tDescripción: ")
            Calificacion = input("\tClasificación (1-5): ")
            Reseña = input("\tReseña: ")
            resultado = Calificaciones_Reseñas_Usuarios.crear(usuario_id, titulo, descripcion, Calificacion, Reseña)
            if resultado:
                print(f"\n\tSe creó satisfactoriamente la Calificacion y Reseña '{titulo}'.")
            else:
                print("\n\tNo fue posible crear la Calificacion y Reseña en este momento.")
            funciones.esperarTecla()

        elif opcion == "2" or opcion.upper() == "MOSTRAR":
            funciones.borrarPantalla()
            lista_Calificaciones_Reseñas_Usuarios = Calificaciones_Reseñas_Usuarios.mostrar(usuario_id)
            if len(lista_Calificaciones_Reseñas_Usuarios) > 0:
                print("\n\t.:: Mostrar las Calificaciones  y Reseñas del Usuarios ::.\n")
                print(f"{'ID':<10}{'Nombre':<15}{'Descripcion':<15}{'Clasificación':<15}{'Reseña':<15}{'Usuario':<15}")
                print("-" * 80)
                for Calificaciones_Reseñas_Usuarios_ in lista_Calificaciones_Reseñas_Usuarios:
                    print(f"{Calificaciones_Reseñas_Usuarios_[0]:<10}{Calificaciones_Reseñas_Usuarios_[1]:<15}{Calificaciones_Reseñas_Usuarios_[2]:<15}{Calificaciones_Reseñas_Usuarios_[3]:<15}{Calificaciones_Reseñas_Usuarios_[4]:<15}{Calificaciones_Reseñas_Usuarios_[5]:<15}")
                print("-" * 80)
            else:
                print("\n\t.:: No hay Calificacion y Reseña en el sistema ::.")
            funciones.esperarTecla()

        elif opcion == "3" or opcion.upper() == "CAMBIAR":
            funciones.borrarPantalla()
            lista_Calificaciones_Reseñas_Usuarios = Calificaciones_Reseñas_Usuarios.mostrar(usuario_id)
            if len(lista_Calificaciones_Reseñas_Usuarios) > 0:
                print(f"\n\tMostrar las Calificacion y Reseña")
                print(f"{'ID':<10}{'Titulo':<15}{'Descripción':<20}{'Fecha':<15}")
                print("-" * 80)
                for fila in lista_Calificaciones_Reseñas_Usuarios:
                    print(f"{fila[0]:<10}{fila[2]:<15}{fila[3]:<20}{fila[4]}")
                print("-" * 80)
                resp = input("¿Deseas modificar alguna Calificaciones o Reseñas? (Si/No): ").lower().strip()
                if resp == "si":
                    id = input("\t ID del juego  a actualizar: ")
                    titulo = input("\t Nuevo título: ")
                    descripcion = input("\t Nueva descripción: ")
                    Calificacion = input("\t Nueva clasificación (1-5): ")
                    Reseña = input("\t Nueva reseña: ")
                    respuesta = Calificaciones_Reseñas_Usuarios.cambiar(id, titulo, descripcion, Calificacion, Reseña)
                    if respuesta:
                        print(f"\n\tSe actualizó correctamente la Calificacion y Reseña '{titulo}'.")
                    else:
                        print("\n\tNo fue posible actualizar la Calificacion y Reseña. Inténtelo de nuevo.")
                    funciones.esperarTecla()
            else:
                print("\n\tNo existen Calificacion y Reseña para este usuario.")
                funciones.esperarTecla()

        elif opcion == "4" or opcion.upper() == "ELIMINAR":
            funciones.borrarPantalla()
            id = input("\t ID de la Calificacion y Reseña a eliminar: ")
            respuesta = Calificaciones_Reseñas_Usuarios.eliminar(id)
            if respuesta:
                print("\n\tNota eliminada correctamente.")
            else:
                print("\n\tNo fue posible eliminar la  Calificacion y Reseña.")
            funciones.esperarTecla()

        elif opcion == "5" or opcion.upper() == "SALIR":
            break
        else:
            print("\n \t Opción no válida. Intenta de nuevo.")
            funciones.esperarTecla()


def menu_videojuegos():
    while True:
        print("\n\t..::: 🎮SISTEMA DE GESTIÓN DE VIDEOJUEGOS ONLINE🎮:::... " \
              "\n 1️⃣ Agregar videojuego \n 2️⃣ Mostrar videojuegos " \
              "\n 3️⃣ Buscar videojuego por nombre  " \
              "\n 4️⃣ Modificar videojuego " \
              "\n 5️⃣ Eliminar videojuego \n 6️⃣ Vaciar lista de videojuegos " \
              "\n 7️⃣ Salir del sistema")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre: ").strip()
            precio = input("Precio: ").strip()
            plataforma = input("Plataforma: ").strip()
            descripcion = input("Descripción: ").strip()
            fecha_lanzamiento = pedir_fecha_lanzamiento()
            agregar_videojuego(nombre, precio, plataforma, descripcion, fecha_lanzamiento)
            funciones.esperarTecla()

        elif opcion == "2":
            mostrar_videojuegos()
            funciones.esperarTecla()

        elif opcion == "3":
            nombre_buscar = input("Nombre a buscar: ").strip()
            buscar_videojuego(nombre_buscar)
            funciones.esperarTecla()

        elif opcion == "4":
            try:
                indice = int(input("Índice del videojuego a modificar (empezando en 0): "))
            except ValueError:
                print("Índice inválido.")
                funciones.esperarTecla()
                continue
            nombre = input("Nuevo nombre: ").strip()
            precio = input("Nuevo precio: ").strip()
            plataforma = input("Nueva plataforma: ").strip()
            descripcion = input("Nueva descripción: ").strip()
            fecha_lanzamiento = pedir_fecha_lanzamiento()
            modificar_videojuego(indice, nombre, precio, plataforma, descripcion, fecha_lanzamiento)
            funciones.esperarTecla()

        elif opcion == "5":
            try:
                indice = int(input("Índice del videojuego a eliminar (empezando en 0): "))
            except ValueError:
                print("Índice inválido.")
                funciones.esperarTecla()
                continue
            eliminar_videojuego(indice)
            funciones.esperarTecla()

        elif opcion == "6":
            vaciar_lista()
            funciones.esperarTecla()

        elif opcion == "7":
            print("👋 Saliendo del sistema. ¡Hasta luego!")
            break

        else:
            print("❌ Opción inválida.\n")
            funciones.esperarTecla()


if __name__ == "__main__":
    main()
