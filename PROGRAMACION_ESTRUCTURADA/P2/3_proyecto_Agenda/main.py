

import Agenda

def main():
    
    datos = []  

    opcion=True
    while opcion:
     Agenda.borrarPantalla()
     opcion=Agenda.menu_principal()

     match opcion:
        case "1":  
            Agenda.agregar_contacto(datos)
            Agenda.esperarTecla()
        case "2":
            Agenda.mostrar_contactos(datos)
            Agenda.esperarTecla() 
        case "3":
            Agenda.buscar_contacto(datos)
            Agenda.esperarTecla()   
        case "4":
            Agenda.modificar_contacto(datos)
            Agenda.esperarTecla()  
        case "5":
            Agenda.eliminar_contacto(datos)
            Agenda.esperarTecla()
        case "6":
            opcion=False    
            Agenda.borrarPantalla()
            print(" Terminaste la ejecucion del SW")
        case _:
            opcion=True 
            print("Opción invalida vuelva a intentarlo") 
            Agenda.esperarTecla()

if __name__ == "__main__":
    main()

    main()