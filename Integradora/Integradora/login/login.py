from conexionBD import crear_conexion
from funciones.funciones import limpiar_pantalla, pausa

def login():
    """
    Inicia sesión verificando usuario y contraseña en la base de datos.
    Solo permite el acceso si las credenciales son correctas.
    """
    while True:
        limpiar_pantalla()
        print("===== INICIO DE SESIÓN =====")
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")

        conexion = crear_conexion()
        if not conexion:
            print("❌ No se pudo conectar a la base de datos.")
            pausa()
            return False

        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (usuario, contrasena))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                print(f"\n✅ Bienvenido, {usuario}!")
                pausa()
                return True
            else:
                print("\n⚠️ Usuario o contraseña incorrectos.")
                opcion = input("¿Deseas intentar de nuevo? (s/n): ").lower()
                if opcion != "s":
                    return False
        except Exception as e:
            print(f"⚠️ Error durante el inicio de sesión: {e}")
            pausa()
            return False
from conexionBD import crear_conexion
from funciones.funciones import limpiar_pantalla, pausa

def login():
    """
    Inicia sesión verificando usuario y contraseña en la base de datos.
    Solo permite el acceso si las credenciales son correctas.
    """
    while True:
        limpiar_pantalla()
        print("===== INICIO DE SESIÓN =====")
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")

        conexion = crear_conexion()
        if not conexion:
            print("❌ No se pudo conectar a la base de datos.")
            pausa()
            return False

        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (usuario, contrasena))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                print(f"\n✅ Bienvenido, {usuario}!")
                pausa()
                return True
            else:
                print("\n⚠️ Usuario o contraseña incorrectos.")
                opcion = input("¿Deseas intentar de nuevo? (s/n): ").lower()
                if opcion != "s":
                    return False
        except Exception as e:
            print(f"⚠️ Error durante el inicio de sesión: {e}")
            pausa()
            return False
