peliculas = []

def borra_pantalla():
    import os
    os.system("cls")

def esperarTecla():
    input("\n\t\Oprime  una tecla para continuar...")
    

def agregar_pelicula():
    borra_pantalla()
    print("\n\t.:: ➕Agregar Película🎬 ::\n")
    nombre = input("Ingrese el nombre: ").upper ().strip ()
    peliculas.append(nombre)
    print("\n\t\t::: ✅¡LA OPERACIÓN SE REALIZÓ CON ÉXITO!✅ :::\n" ) 
    #print("`\u2705`")
    

def consultarPeliculas():
    borra_pantalla()
    print("\n\t.:: 📖Consultar o Mostrar  Películas🎬 ::\n")
    if len(peliculas) > 0:
        for i in range(0, len(peliculas)):
            print(f"{i+1}. {peliculas[i]}")
    else:
        print("\n\t.::📭No hay películas registradas.📭")

def vaciarPeliculas():
    borra_pantalla()
    print("\n\t.:: 🗑️Vaciar o quitar TODAS las   Películas::.🗑️\n ")
    resp = input("¿Deseas quitar TODOS las peliculas del sistema? (si/no): ").lower().strip()
    if resp == "si":
        peliculas.clear()
        print("\n\t\t::: ✅¡LA OPERACIÓN SE REALIZÓ CON ÉXITO!✅ :::\n")

def buscar_Peliculas():
    borra_pantalla()
    print("\n\t.:: 🔍Buscar Películas🔍 ::\n")
    pelicula_buscar = input("Ingrese el nombre de la película a buscar: ").upper().strip()
    encontro=0
    if not  (pelicula_buscar in peliculas):
        print("\n\t.:: ❌¡No se encuentra la película!❌.\n")
    else:
        for i in range(0, len(peliculas)):
            if pelicula_buscar  == peliculas[i]:
               print(f"\nLa película '{pelicula_buscar}' si tenemos y esta en la casilla {i+1} ")
            encontro+=1
        print(f"\n\t.::✅¡Se encontraron {encontro} con este titulo!✅.\n")
        print("\n\t\t::: ✅¡LA OPERACIÓN SE REALIZÓ CON ÉXITO!✅ :::\n")       


def eliminar_pelicula(): 
    borra_pantalla()
    print("\n\t.:: 🗑️Borrar  Película🗑️ ::\n")
    pelicula_buscar=input("Ingrese el nombre de la pelicula a borrar: ").upper().strip()
    encontro=0
    if not (pelicula_buscar in peliculas):
        print("\n\t\t.::❌¡No se encuentra la película!❌.")
    else:
        resp="si"
        while pelicula_buscar in peliculas:
            posicion = peliculas.index(pelicula_buscar)
            resp = input(f"¿Deseas eliminar la pelicula del sistema? (si/no) ")
            if resp == "si":
                print(f"\nLa película '{pelicula_buscar}' y estaba en la casilla {posicion+1}.")
                peliculas.pop(posicion)
            else:
                break