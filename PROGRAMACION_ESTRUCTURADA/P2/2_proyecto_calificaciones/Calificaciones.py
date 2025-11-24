import os
import mysql.connector
from mysql.connector import Error

#lista = [
#    ["Ruben", 10.0, 10.0, 10.0]
#    ["Diana", 10.0, 9.8, 8.0]
#    ["José", 5.0, 6.0, 7.0]
#]

def borra_pantalla():
    os.system("cls")

def esperarTecla():
    input("\n\t...Oprima una tecla para continuar...")

def conectar():
    try:
        conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "bd_calificaciones"
        )
        return conexion
    except Error as e:
        print(f"El error que se presento es: {e}")
        return None

def menu_principal():
    print("\t\t📂SISTEMA DE GESTIÓN DE CALIFICACIONES📂:\n\tSelcciona una opcion para empezar:\n\n\t📝 1.- Agregar\n\t📂 2.- Mostrar\n\t📝 3.- Calcular promedio\n\t🔍 4.- Buscar Alumno\n\t🚪 5.- Salir")
    op = input("\n Opcion seleccionada: ").upper().strip()
    return op

def Agregar_Calificaciones(lista):
    borra_pantalla()
    conexionBD = conectar()
    if conexionBD != None:
        print("📝 .::Agregar Calificaciones::. 📝")
        nombre=input("Nombre del Alumno: ").upper().strip()
        calificaciones=[]
        for i in range(1,4):
            continua=True
            while continua:
                try:
                    cal=float(input(f"Calificación {i}: "))
                    if cal>=0 and cal<11:
                        calificaciones.append(cal)
                        continua=False
                    else:
                        print("Ingresa un número valido") 
                except ValueError:
                    print("Ingresa un valor númerico")

        cursor = conexionBD.cursor()

        sql = "INSERT INTO alumno (nombre, calf1, calf2, calf3) VALUES (%s, %s, %s, %s)"
        val = (nombre, calificaciones[0], calificaciones[1], calificaciones[2])
        cursor.execute(sql, val)
        conexionBD.commit()
        print("✅ Acción realizada con exíto ✅")
        cursor.close()

def Mostrar_Calificaciones(lista):
    borra_pantalla()
    conexionBD = conectar()
    if conexionBD != None:
        print("📝 .::Mostrar Calificaciones::. 📝")

        cursor = conexionBD.cursor()
        sql = "SELECT * FROM alumno"
        cursor.execute(sql)
        registros = cursor.fetchall()

        if registros:
            print("\n\t📝 .::Alumnos registrados::. 📝")
            print(f"{'ID':<15} {'Nombre':<10} {'Calf. 1':<10} {'Calf. 2':<10} {'Calf. 3':<10}")
            print(f"{'-' * 60}")
            for fila in registros:
                print(f"{fila[0]:<15} {fila[1]:<10} {fila[2]:<10} {fila[3]:<10} {fila[4]:<10}")
                print(f"{'-' * 60}")  
        else:
            print("⚠️ No hay calificaciones registradas en el sistema ⚠️")
    
        cursor.close()

def Calcular_Promedios(lista):
    borra_pantalla()
    conexionBD = conectar()
    if conexionBD != None:
        print("📝 .:: PROMEDIOS ::. 📝")
        
        cursor = conexionBD.cursor()
        sql = "SELECT  nombre, calf1, calf2, calf3 FROM alumno"
        cursor.execute(sql)
        registros = cursor.fetchall()

        if registros:
            print("\n\t📝 .::Promedios::. 📝")
            print(f"{'Alumno':<15} {'Promedio':<10}")
            print(f"{'-' * 40}")
            promedio_grupal = 0
            for fila in registros:
                promedio = sum(fila[1:]) / 3
                print(f"{fila[0]:<15} {promedio:<10}")
                promedio_grupal += promedio
            print(f"{'-' * 40}")  
            promedio_grupal = promedio_grupal / len(registros)
            print(f"El promedio grupal es: {promedio_grupal} ")
        else:
            print("⚠️ No hay calificaciones registradas en el sistema ⚠️")
        cursor.close()
        
def buscarAlumno(lista):
    borra_pantalla()
    conexionBD = conectar()
    if conexionBD != None:
        print("🔍 .::Mostrar Calificaciones::. 🔍")
        nombre = input("\n\tIngresa el nombre del alumno a buscar: ").upper().strip()

        cursor = conexionBD.cursor()
        sql = "SELECT * FROM alumno WHERE nombre = %s"
        val = (nombre,)
        cursor.execute(sql, val)
        registros = cursor.fetchall()

        if registros:
            print("\n\t📝 .::Alumnos registrados::. 📝")
            print(f"{'ID':<15} {'Nombre':<10} {'Calf. 1':<10} {'Calf. 2':<10} {'Calf. 3':<10}")
            print(f"{'-' * 60}")
            for fila in registros:
                print(f"{fila[0]:<15} {fila[1]:<10} {fila[2]:<10} {fila[3]:<10} {fila[4]:<10}")
                print(f"{'-' * 60}")  
        else:
            print("⚠️ No hay calificaciones registradas en el sistema ⚠️")
    
        cursor.close()

