import funciones
from usuarios import usuario
from notas import nota
import getpass

def main():
    opcion = True
    while opcion:
        funciones.borrarPantalla()
        opcion = funciones.menu_usurios()

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
                    menu_notas(lista_usuario[0], lista_usuario[1], lista_usuario[2])
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

def menu_notas(usuario_id, nombre, apellidos):
    while True:
        funciones.borrarPantalla()
        print(f"\n \t \t \t Bienvenido {nombre} {apellidos}, has iniciado sesión ...")
        opcion = funciones.menu_notas()

        if opcion == "1" or opcion.upper() == "CREAR":
            funciones.borrarPantalla()
            print(f"\n\t .:: Crear Nota ::.")
            titulo = input("\tTitulo: ")
            descripcion = input("\tDescripción: ")
            resultado = nota.crear(usuario_id, titulo, descripcion)
            if resultado:
                print(f"\n\tSe creó satisfactoriamente la nota '{titulo}'.")
            else:
                print("\n\tNo fue posible crear la nota en este momento.")
            funciones.esperarTecla()

        elif opcion == "2" or opcion.upper() == "MOSTRAR":
            funciones.borrarPantalla()
            lista_notas = nota.mostrar(usuario_id)
            if len(lista_notas) > 0:
                print("\n\t.:: Mostrar las Notas ::.\n")
                print(f"{'ID':<10}{'Nombre':<15}{'Descripcion':<15}{'Clasificación':<15}{'Fecha':<15}{'Usuario':<15}")
                print("-" * 80)
                for notas in lista_notas:
                    print(f"{notas[0]:<10}{notas[1]:<15}{notas[2]:<15}{notas[3]:<15}{notas[4]:<15}{notas[5]:<15}")
                print("-" * 80)
            else:
                print("\n\t.:: No hay notas en el sistema ::.")
            funciones.esperarTecla()

        elif opcion == "3" or opcion.upper() == "CAMBIAR":
            funciones.borrarPantalla()
            lista_notas = nota.mostrar(usuario_id)
            if len(lista_notas) > 0:
                print(f"\n\tMostrar las Notas")
                print(f"{'ID':<10}{'Titulo':<15}{'Descripción':<20}{'Fecha':<15}")
                print("-" * 80)
                for fila in lista_notas:
                    print(f"{fila[0]:<10}{fila[2]:<15}{fila[3]:<20}{fila[4]}")
                print("-" * 80)
                resp = input("¿Deseas modificar alguna nota? (Si/No): ").lower().strip()
                if resp == "si":
                    print(f"\n \t .:: {nombre} {apellidos}, vamos a modificar una nota ::. \n")
                    id = input("\t ID de la nota a actualizar: ")
                    titulo = input("\t Nuevo título: ")
                    descripcion = input("\t Nueva descripción: ")
                    respuesta = nota.cambiar(id, titulo, descripcion)
                    if respuesta:
                        print(f"\n\tSe actualizó correctamente la nota '{titulo}'.")
                    else:
                        print("\n\tNo fue posible actualizar la nota. Inténtelo de nuevo.")
                    funciones.esperarTecla()
            else:
                print("\n\tNo existen notas para este usuario.")
                funciones.esperarTecla()

        elif opcion == "4" or opcion.upper() == "ELIMINAR":
            funciones.borrarPantalla()
            print(f"\n \t .:: {nombre} {apellidos}, vamos a borrar una nota ::. \n")
            id = input("\t ID de la nota a eliminar: ")
            respuesta = nota.eliminar(id)
            if respuesta:
                print("\n\tNota eliminada correctamente.")
            else:
                print("\n\tNo fue posible eliminar la nota.")
            funciones.esperarTecla()

        elif opcion == "5" or opcion.upper() == "SALIR":
            break

        else:
            print("\n \t Opción no válida. Intenta de nuevo.")
            funciones.esperarTecla()

if __name__ == "__main__":
    main()
