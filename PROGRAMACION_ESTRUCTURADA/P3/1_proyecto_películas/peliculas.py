
import mysql.connector
from mysql.connector import Error

#Disct u objeto para almacenar los atributos (nombre,categoria,clasificacion,genero,idioma)  y sus valores 

# pelicula={
#            "nombre":"",
#            "categoria":"",
#            "clasificacion":"",
#            "genero":"",
#            "idioma":""
#          }

pelicula={}

def borrarPantalla():
  import os  
  os.system("cls")

def esperarTecla():
  input("\n\t\t... Oprima cualquier tecla para continuar ...")  

def conectar():
  try:
    conexion=mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="bd_peliculas"  
      )
    return conexion
  except Error as e:
    print(f"El error que se presento es: {e}")
    return None

def crearPeliculas():
  borrarPantalla()
  conexionBD=conectar()
  if conexionBD!=None:
    print("\n\t.:: Crear Películas ::. \n")
    pelicula["nombre"]=input("Ingresa el nombre: ").upper().strip()
    #pelicula.update({"nombre":input("Ingresa el nombre: ").upper().strip()})
    pelicula.update({"categoria":input("Ingresa la categoría: ").upper().strip()})
    pelicula.update({"clasificacion":input("Ingresa la clasificación: ").upper().strip()})
    pelicula.update({"genero":input("Ingresa el genero: ").upper().strip()})
    pelicula.update({"idioma":input("Ingresa el idioma: ").upper().strip()})
    
    ####### BD
    cursor=conexionBD.cursor()
    sql="insert into peliculas (nombre,categoria,clasificacion,genero,idioma) value (%s,%s,%s,%s,%s)"
    val=(pelicula["nombre"],pelicula["categoria"],pelicula["clasificacion"],pelicula["genero"],pelicula["idioma"])
    cursor.execute(sql,val)
    conexionBD.commit()
    print("\n\t\t::: ¡LA OPERACIÓN SE REALIZÓ CON EXÍTO! :::")

def mostrarPeliculas():
  borrarPantalla()
  conexionBD=conectar()
  if conexionBD!=None:
    print("\n\t.:: Mostrar las Películas ::. \n")
    cursor=conexionBD.cursor()
    sql="select * from peliculas"
    cursor.execute(sql)
    registros=cursor.fetchall()
    if registros:
      print("Mostrar las Peliculas")
      print(f"{'ID':<10}{'Nombre':<15}{'Categoria':<15}{'Clasificacion':<15}{'Genero':<15}{'Idioma':<15}")
      print(f"-"*80)
      for pelis in registros:
        print(f"{pelis[0]:<10}{pelis[1]:<15}{pelis[2]:<15}{pelis[3]:<15}{pelis[4]:<15}{pelis[5]:<15}")
      print(f"-"*80)  
    else:
      print("\t .:: No hay peliculas en el sistema ::..")  

def buscarPeliculas():
  borrarPantalla()
  conexionBD=conectar()
  if conexionBD!=None:
    print("\n\t.:: Buscar Películas ::. \n")
    nombre=input("Ingresa el nombre de la pelicula a buscar: ").upper().strip()
    cursor=conexionBD.cursor()
    sql="select * from peliculas where nombre=%s"
    val=(nombre,)
    cursor.execute(sql,val)
    registros=cursor.fetchall()
    if registros:
      print("Mostrar las Peliculas")
      print(f"{'ID':<10}{'Nombre':<15}{'Categoria':<15}{'Clasificacion':<15}{'Genero':<15}{'Idioma':<15}")
      print(f"-"*80)
      for pelis in registros:
        print(f"{pelis[0]:<10}{pelis[1]:<15}{pelis[2]:<15}{pelis[3]:<15}{pelis[4]:<15}{pelis[5]:<15}")
      print(f"-"*80)  
    else:
      print("\t .:: peliculas no encontradas en el sistema ::..")


def borrarPeliculas():
  borrarPantalla()
  conexionBD=conectar()
  if conexionBD!=None:
    print("\n\t.:: Borrar Películas ::. \n")
    nombre=input("Ingresa el nombre de la pelicula a borrar: ").upper().strip()
    cursor=conexionBD.cursor()
    sql="select * from peliculas where nombre=%s"
    val=(nombre,)
    cursor.execute(sql,val)
    registros=cursor.fetchall()
    if registros:
      print("Mostrar las Peliculas")
      print(f"{'ID':<10}{'Nombre':<15}{'Categoria':<15}{'Clasificacion':<15}{'Genero':<15}{'Idioma':<15}")
      print(f"-"*80)
      for pelis in registros:
        print(f"{pelis[0]:<10}{pelis[1]:<15}{pelis[2]:<15}{pelis[3]:<15}{pelis[4]:<15}{pelis[5]:<15}")
      print(f"-"*80) 
      resp=input(f"¿Deseas borrar la pelicula {nombre}? (Si/No): ").lower().strip()
      if resp=="si":
        sql="delete from peliculas where nombre = %s"
        val=(nombre,)
        cursor.execute(sql,val)
        conexionBD.commit()
        print("\n\t\t::: ¡LA OPERACIÓN SE REALIZÓ CON EXÍTO! :::")
    else:
      print("\t .:: peliculas no encontradas en el sistema ::..")



      
       