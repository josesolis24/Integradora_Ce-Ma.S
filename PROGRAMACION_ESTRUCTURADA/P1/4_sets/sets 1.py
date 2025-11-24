"""

 
 Sets.- 
  Es un tipo de datos para tener una coleccion de valores pero no tiene ni indice ni orden

  Set es una colección desordenada, inmutable* y no indexada. No hay miembros duplicados.
"""
import os
os.system("cls")

paises={"Mexico","Brasil","España","Canada"}
print(paises)

#Funciones u operaciones 
for i in paises:
    print(i)

paises.add("México")
print(paises)

paises.pop()
print(paises)

paises.remove("México")
print(paises)


#ejemplo. Crear un programa que solicite los email de los alumnos de la UTD
#almacenar en una lista y posterior mente mostrar los emails sin duplicados

import os
os.system("cls")

emails= []
resp="si"

while resp=="si":
  
  emails.append(input("Ingrese el email de la UTD: "))
  resp=input("¿Desea ingresar otro email? (si/no): ").lower()
    
emails_set = set(emails)
emails_list = list(emails_set)
print("Los emails: ")






  



