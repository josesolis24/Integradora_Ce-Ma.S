import mysql.connector
from mysql.connector import Error

def borrarPantalla():
  import os  
  os.system("cls")

def esperarTecla():
    input("Oprima cualquier tecla para continuar")


def menu_principal():
   print(".:: Sistema de Agenda ::.. "
         "\n1️⃣ Agregar contacto  "
         "\n2️⃣ Mostrar todos los contactos"
         "\n3️⃣ Buscar contactos por nombre "
         "\n4️⃣ Modificar Contacto "
         "\n5️⃣ Eliminar contacto "
         "\n6️⃣ SALIR ")
   opcion=input("Elige una opción (1️⃣➖6️⃣): ") 
   return opcion

def conectar():
    try:
        conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "bd_agenda"
        )
        return conexion
    except Error as e:
        print(f"El error que se presento es: {e}")
        return None

def agregar_contacto(agenda):
    borrarPantalla()
    conexionBD = conectar()
    if conexionBD != None:
        print("\t\t📝.:: Agregar Contacto ::.📝")
        nombre = input("\nNombre: ").upper().strip()
        if nombre in agenda:
            print("\n⚠ Contacto ya existente ⚠")
        else:
            telefono = input("Teléfono: ").strip()
            email = input("Email: ").lower().strip()
            agenda[nombre] = [telefono, email]

            cursor = conexionBD.cursor()
            sql = "INSERT INTO contacto (nombre, telefono, email) VALUES (%s, %s, %s)"
            val = (nombre, agenda[nombre][0], agenda[nombre][1])
            cursor.execute(sql, val)
            conexionBD.commit()

            print("\n✅ :: Acción realizada con éxito :: ✅")

            cursor.close()

        
def mostrar_contactos(agenda):
    conexionBD = conectar()
    if conexionBD != None:
        borrarPantalla()
        print("\t\t👤.:: Mostrar Contactos ::.👤")
        cursor = conexionBD.cursor()
        sql = "SELECT * FROM contacto"
        cursor.execute(sql)
        contactos = cursor.fetchall()

        if contactos:
            print("\n\t ::Contactos::")
            print(f"\n{'ID':<15} {'Nombre':<15} {'Teléfono':<15} {'Email':<15}")
            print(f"-" * 60)
            for fila in contactos:
                print(f"{fila[0]:<15} {fila[1]:<15} {fila[2]:<15} {fila[3]:<15}")
            print(f"-" * 60)
        else:
            print("❌ No hay contactos en el sistema ❌")
        
        cursor.close()

def buscar_contacto(agenda):
    conexionBD = conectar()
    if conexionBD != None:
        borrarPantalla()
        print("\t\t🔍.:: Buscar Contacto ::.🔍")
        nombre = input("\n\tIngresa el nombre del contacto a buscar: ").upper().strip()

        cursor = conexionBD.cursor()
        sql = "SELECT * FROM contacto WHERE nombre = %s"
        val = (nombre,)
        cursor.execute(sql, val)
        contactos = cursor.fetchall()

        if contactos:
            print("\n\t ::Contactos::")
            print(f"\n{'ID':<15} {'Nombre':<15} {'Teléfono':<15} {'Email':<15}")
            print(f"-" * 60)
            for fila in contactos:
                print(f"{fila[0]:<15} {fila[1]:<15} {fila[2]:<15} {fila[3]:<15}")
            print(f"-" * 60)
        else:
            print("\n\t❌ No existe ese contacto en el sistema ❌")
        
        cursor.close()

def modificar_contacto(agenda):
    conexionBD = conectar()
    if conexionBD != None:
        borrarPantalla()
        print("\t\t🔄.:: Modificar Contacto ::.🔄")
        busqueda = input("\n\tIngresa el nombre del contacto a modificar: ").upper().strip()

        cursor = conexionBD.cursor()
        sql = "SELECT * FROM contacto WHERE nombre = %s"
        val = (busqueda,)
        cursor.execute(sql, val)
        contactos = cursor.fetchall()

        if contactos:
            print("\n\t ::Contactos::")
            print(f"\n{'ID':<15} {'Nombre':<15} {'Teléfono':<15} {'Email':<15}")
            print(f"-" * 60)
            for fila in contactos:
                print(f"{fila[0]:<15} {fila[1]:<15} {fila[2]:<15} {fila[3]:<15}")
            print(f"-" * 60)
            id = input("Selecciona el ID del contacto a modificar: ").strip()
            if id in contactos:
                resp = input(f"¿Desea modificar el contacto {busqueda} con el ID: {id}? (Si/No): ").upper().strip()
                if resp == "SI":
                    nombre = input("\nNombre: ").upper().strip()
                    telefono = input("Teléfono: ").strip()
                    email = input("Email: ").lower().strip()

                    sql = "UPDATE contacto SET nombre = %s, telefono = %s, email = %s WHERE nombre = %s AND id = %s"
                    val = (nombre, telefono, email, busqueda, id)
                    cursor.execute(sql, val)
                    conexionBD.commit()
                    print("\n✅ :: Acción realizada con éxito :: ✅")
            else:
                print("\n\t⚠ ::ID no valido, ingrese un ID correcto y vuelva a intentarlo:: ⚠")
        else:
            print("❌ No hay existe ese contacto en el sistema ❌")
        
        cursor.close()

def eliminar_contacto(agenda):
    conexionBD = conectar()
    if conexionBD != None:
        borrarPantalla()
        print("\t\t📛.:: Eliminar Contacto ::.📛")
        nombre = input("\n\tIngresa el nombre del contacto a eliminar: ").upper().strip()

        cursor = conexionBD.cursor()
        sql = "SELECT * FROM contacto WHERE nombre = %s"
        val = (nombre,)
        cursor.execute(sql, val)
        contactos = cursor.fetchall()

        if contactos:
            print("\n\t ::Contactos::")
            print(f"\n{'ID':<15} {'Nombre':<15} {'Teléfono':<15} {'Email':<15}")
            print(f"-" * 60)
            for fila in contactos:
                print(f"{fila[0]:<15} {fila[1]:<15} {fila[2]:<15} {fila[3]:<15}")
            print(f"-" * 60)
            id = input("Selecciona el ID del contacto a eliminar: ").strip()
            if id in contactos:             
                resp = input(f"¿Desea eliminar el contacto {nombre} con el ID: {id}? (Si/No): ").upper().strip()
                if resp == "SI":
                    sql = "DELETE FROM contacto WHERE nombre = %s AND id = %s"
                    val = (nombre, id)
                    cursor.execute(sql, val)
                    conexionBD.commit()
                    print("\n✅ :: Acción realizada con éxito :: ✅")
            else:
                print("\n\t⚠ ::ID no valido, ingrese un ID correcto y vuelva a intentarlo:: ⚠")
        else:
            print("❌ No hay existe ese contacto en el sistema ❌")
        
        cursor.close()
