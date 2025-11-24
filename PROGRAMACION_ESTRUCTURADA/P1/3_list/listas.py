import os
#Ejemplo 1 Crear una lista de numeros e imprimir el contenido 
os.system("cls")

numeros=[3,55,201,10,25]

#1er formas
print("Los numeros de la lista son:",numeros)

#2da forma esta forma imprime la lista hacia abajo, trabaja con el valor
for i in numeros:
    print(i)

#3er forma, trabaja con el indice
for i in range(0, len(numeros)):
    print(numeros[i])


#Ejemplo 2 crear una lista de palabras y posteriormente buscar la coincidencia de una palabra 
os.system("cls")

#1er forma
palabras=["hola","casa","mesa","estrella"]
palabras_buscar=input("Dame la palabra a buscar: ")

if palabras_buscar in palabras:
    print ("Se encontro la palabra")
else:
    print("No se encontro la palabra")

#2da forma se recorre toda la lista
#for i in palabras:
    #if i==palabras_buscar:
        #print ("Se encontro la palabra")
    #else:
     #print("No se encontro la palabra") 


#Otra forma para que no aparezca mucho "no se encontro la palabra "
encontro=True
for i in palabras:
    if i==palabras_buscar:
        encontro=True

if encontro:
    print("Se encontro la palabra")
else:
     print("No se encontro la palabra") 

#3er forma
encontro=True
for i in range(0,len(numeros)):
    if palabras[i]==palabras_buscar:
        encontro=True

if encontro:
    print("Se encontro la palabra")
else:
     print("No se encontro la palabra") 


#ejemplo 3 Añadir elementos a una lista 

numeros=[]
opc="si"
while opc=="si":
    numero=float(input("Dame un numero entero o decimal"))
    numeros.append(numeros)
    #numeros.append(float(input("Dame un numero entero o decimal"))) es mas corta para ahorrar linea de codigo
    opc=input("Deseas solicitar otro numero (si/no)").lower()#convierte a minusculas

print(numeros)


#Ejemplo 4 Crear una lista multidimensional (matriz) que almacene el nombre y el telefono de 4 personas 

agenda=[
        ["Carlos","6181234567"],
        ["Alberto","6671234567"],
        ["Martin","6785678923"]
       ]

print(agenda)

for i in agenda:
    print(i)

for r in range(0,3):
    for c in range(0,2):
        print(agenda[r][c])    

cadena=""
for r in range(0,3):
    for c in range(0,2):
      cadena+=f"{agenda[r][c]}, "
    cadena+="\n"     
print(cadena) 























#Ejemplo 2 Crear una lista de palabras y posteriormente buscar la coincidencia de una palabra

os.system("cls")

palabras=["hola","casa","jupiter","sol"]

palabra_buscar=input ("Dame la plabra a buscar: ")

#1era forma
if palabra_buscar in palabras:
    print("Se encontro la palabra")
else:
    print("No encontro la palabra")

#2da forma
encontro=False
for i in palabras:
    if i ==palabra_buscar:
        encontro=True
if encontro:
    print("Se encontro la palabra")
else:
    print("no se encontro la palbara")

#3era forma
encontro=False
for i in palabras(0,len(numeros)):
    if palabras[i]==palabra_buscar:
        encontro=True
if encontro:
    print("Se encontro la palabra")
else:
    print("no se encontro la palbara")







#Ejemplo3 añadir elementos a una lista

numeros=[]
opc="si"

while opc=="si":
    numeros.append(float(input("Dame un numero entero o decimal: ")))
    opc=input("Deseas solicitar otro numero (si/no)").lower()

print(numeros)







#Ejemplo4 Crear una lista multidimensional (matriz) que almacene el nombre y telefono de 4 personas

