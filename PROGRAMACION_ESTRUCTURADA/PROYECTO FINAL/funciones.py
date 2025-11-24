import os

def borrarPantalla():
    # Compatible con Windows y Unix
    os.system('cls' if os.name == 'nt' else 'clear')

def esperarTecla():
    input("\n\t\t ... ⚠️ Oprima cualquier tecla para continuar ⚠️ ...")

def menu_usuarios():
    print("\n \t.:: 🎮 Sistema de Gestión de Videojuegos🎮  ::..\n")
    print("\t\t1️⃣ Registro")
    print("\t\t2️⃣ Login")
    print("\t\t3️⃣ Salir")
    opcion = input("\t\t Elige una opción: ").upper().strip()
    return opcion

def menu_Calificaciones_Reseñas_Usuarios ():
    print("\n \t .:: Calificaciones y Reseñas de Usuarios ::.\n")
    print("\t1️⃣ Crear")
    print("\t2️⃣  Mostrar")
    print("\t3️⃣ Cambiar")
    print("\t4️⃣ Eliminar")
    print("\t5️⃣ Salir")
    opcion = input("\t\t Elige una opción: ").upper().strip()
    return opcion

def menu_videojuegos():
    print("\n\t..:::🎮 MENÚ DE GESTIÓN DE VIDEOJUEGOS 🎮:::.." 
          "\n\t1️⃣ Agregar videojuego"
          "\n\t2️⃣ Mostrar videojuegos"
          "\n\t3️⃣ Buscar videojuego por nombre"
          "\n\t4️⃣ Modificar videojuego"
          "\n\t5️⃣ Eliminar videojuego"
          "\n\t6️⃣ Vaciar lista"
          "\n\t7️⃣ Salir")
    opcion = input("\tSelecciona una opción: ").strip()
    return opcion

def menu_Calificaciones_Reseñas_Usuarios_videojuegos():
    while True:
        print("\n\t..::: 📚 MENÚ DE Calificaciones y Reseñas del Usuarios Y VIDEOJUEGOS 📚 :::..")
        print("\t1️⃣ Calificacion y Reseña")
        print("\t2️⃣ Videojuegos")
        print("\t3️⃣ Salir")
        opcion = input("\tSelecciona una opción: ").strip()

        if opcion == "1" or opcion.upper() == "Calificaciones_Reseñas_Usuarios":
            menu_Calificaciones_Reseñas_Usuarios()

        elif opcion == "2" or opcion.upper() == "VIDEOJUEGOS":
            menu_videojuegos()

        elif opcion == "3" or opcion.upper() == "SALIR":
            break
        else:
            print("\n \t Opción no válida. Intenta de nuevo.")
            esperarTecla()