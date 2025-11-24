#Notas: 1.- utilizar funciones y mandar llamar desde otro archivo. 
# 2.- Utilizar una lizta para almacenar los nombres de las peliculas
# 3. Utilizar e implimentar una BD relacional en MySQL 
import os
os.system("cls")

import peliculas

opcion=True
while opcion:
    peliculas.borrarPantalla()
    print("\n\t\t...::: CINEPOLIS CLON :::... \n\t\t..::: Sistema de Gestión de Peliculas :::..." \
    "\n\t\t\t 1.- Crear  \n\t\t\t 2.- Borrar \n\t\t\t 3.- Mostar \n\t\t\t 4.- Buscar " \
    "\n\t\t\t 5.- Modificar \n\t\t\t 6.-SALIR")
    opcion=input("\t\t Elige una opción: ").upper()

    match opcion:
        case "1":
            peliculas.crearPeliculas()
            peliculas.esperarTecla ()
        case "2":
            peliculas.borrarPeliculas()
            peliculas.esperarTecla () 
        case "3":
            peliculas.mostrarPeliculas() 
            peliculas.esperarTecla()     
        case "4":
            peliculas.buscarPeliculas() 
            peliculas.esperarTecla()
        case "5": 
            peliculas.modificarPeliculas()
            peliculas.esperarTecla()
        
        case "6":
            opcion=False    
            print("\n\tTerminaste la ejecucion del SW")
        case _: 
            input("\n\tOpción invalida vuelva a intentarlo ... por favor")