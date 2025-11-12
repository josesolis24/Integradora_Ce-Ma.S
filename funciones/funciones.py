def limpiar_pantalla():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    input("\nPresiona ENTER para continuar...")
