'''List (Array)
son colleciones o conjuntos de datos / valores bajo un mismo nombre, para acceder a los valores se hace con un indice numerico

Nota: sus valores si son modificables

La lista es una coleccion ordena y modificable.
Permite miembros duplicados.

'''
import os
os.system ("cls")

#Funciones mas comunes en las listas

paises=["Mexico", "España", "Canada", "Brasil"]

numeros=[23,12,100,34]

varios=["Hola", True, 33, 3.12]

#Ordenar las listas
print(numeros)
print(paises)
print(varios)

#Con la funcion sort() ordena los numeros, de menor a mayor
#al igual ordena los paises alfaveticamente
numeros.sort()
print(numeros)
paises.sort()
print(paises)

#Agregar o insertar o añadir un elemento de la lista 
#1er forma paises=["Mexico", "España", "Canada", "Brasil"]
print(paises)
paises.append("Honduras")
print(paises)

#2da forma 
paises.insert(0,"Honduras")
print(paises)

#1ra forma para borrar
#eliminar o borrar o suprimir un elemento de la lista 
#1er forma paises=["Mexico", "España", "Canada", "Brasil"]
paises.sort()#es para ordenar los paises 
print(paises)
paises.pop(4)
print(paises)

#2da forma para borrar
paises.remove("Honduras")
print(paises)

#Buscar un elemento dentro de una lista

print("Brasil" in paises)

#Contar el numero de veces que un elemento esta dentro de una lista 
#numeros=[23,12,100,34]
print(numeros)
print(numeros.count(12))
numeros.insert(1,12)
print(numeros)
print(numeros.count(101))

#Dar la vuelta a los elementos de una lista 
print(paises)
paises.reverse()
print(paises)

print(numeros)
numeros.reverse()
print(numeros)

#Conocer el indice o la posicion de un valor de la lista
posicion=paises.index("España")

paises[posicion]="ESPAÑA" #Cambia todas las letras a mayusculas 

#Unir el contenido de una o mas listas 
#numeros=[100,34,23,12,12]
numeros2=[300,500,100]

print(numeros)
print(numeros2)

numeros.extend(numeros2) # Une las dos liastas
print(numeros)

paises.extend(numeros2) #Une dos listas con tipo de datos diferente 
print(paises)
