#Proyecto 3
#Crear un proyecto  que permita  gestionar (administrar ); colocar  un menu  de opciones para agregar, borrar,  modificar, y calcular procedimiento  calificaciones de los alumnos
#  
#Notas: 
#1.-utiliza  funciones y mandar a llamar desde otro archivo 
#2.- Utilizar listasa  para almacenar  los siguentes atrivutos (nombre, del alunmo y 3 calificaciones)


import Calificaciones

def main():

    opcion=True
    datos = []
    while opcion:
        Calificaciones.borra_pantalla()
        opcion=Calificaciones.menu_pricpal()

    match opcion:
        case "1":
            Calificaciones.Agregar_Calificaciones(datos)
            Calificaciones.esperarTecla()
        case "2":
            Calificaciones.Mostrar_Calificaciones(datos)
            Calificaciones.esperarTecla() 
        case "3":
           Calificaciones.Calcular_Promedios(datos)   
           Calificaciones.esperarTecla()
        case "4":
           opcion=False
           Calificaciones.borra_pantalla() 
           print("✅Terminaste la ejecucion del SW✅")
        
        case _:
            opcion=True 
            input("Opción invalida vuelva a intentarlo ... por favor")

main()

if __name__ == "__main__":
    main()

