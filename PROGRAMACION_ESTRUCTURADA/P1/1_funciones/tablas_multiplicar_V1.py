import os

'''Crear un programa que calcule y imprima la tabla de multiplicar del 2
   Restriciones :
   1.- Sin estructuras de control
   2.- Sin funciones

'''

#vercion 1
num=int(input("Ingresa un numero de la tabla de multiplicar:"))
multi=num*1
print (f"´{num} x 1 = {multi}")
multi=2*2
print (f"{num} x 2 = {multi}")
multi=2*3
print (f"{num} x 3 = {multi}")
multi=2*4
print (f"{num}  x 4 = {multi}")
multi=2*5
print (f"{num} x 5 = {multi}")
multi=2*6
print (f"{num} x 6 = {multi}")
multi=2*7
print (f"{num}  x 7 = {multi}")
multi=2*8
print (f"{num}  x 8 = {multi}")
multi=2*9
print (f"{num} x 9 = {multi}")
multi=2*10
print (f"{num}  x 10 = {multi}")

#vercion 2
'''Crear un programa que calcule y imprima la tabla de multiplicar del 2
   Restriciones :
   1.- Con estructuras de control
   2.- Sin funciones

'''

num=int(input("Ingresa un numero de la tabla de multiplicar:"))
for i in range(1,11):
    multi=num*i
    print(f"{num} x {i} = {multi}")


#vercion 3
'''Crear un programa que calcule y imprima la tabla de multiplicar del 2
   Restriciones :
   1.- Con estructuras de control
   2.- con funciones

'''

num=int(input("Ingresa un numero de la tabla de multiplicar:"))
for i in range(1,11):
    multi=num*i
    print(f"{num} x {i} = {multi}")

