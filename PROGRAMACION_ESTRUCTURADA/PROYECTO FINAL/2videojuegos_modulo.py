videojuegos = []

def borra_pantalla():
    import os
    os.system("cls" if os.name == "nt" else "clear")

def agregar_videojuego(nombre, precio, plataforma, descripcion, fecha_lanzamiento):
    # Si el usuario solo pone la fecha, agregamos hora por defecto
    if fecha_lanzamiento and len(fecha_lanzamiento) == 10:
        fecha_lanzamiento += " 00:00:00"

    # Si está vacío, lo dejamos como "N/A"
    if not fecha_lanzamiento.strip():
        fecha_lanzamiento = "N/A"

    videojuego = {
        "nombre": nombre,
        "precio": precio,
        "plataforma": plataforma,
        "descripcion": descripcion,
        "fecha_lanzamiento": fecha_lanzamiento,
    }
    videojuegos.append(videojuego)
    print("✅ Videojuego agregado con éxito.\n")

def mostrar_videojuegos():
    if not videojuegos:
        print("No hay videojuegos registrados.\n")
        return
    
    print(f"{'No.':<4}{'Nombre':<25}{'Precio':<10}{'Plataforma':<15}{'Descripción':<30}{'Fecha Lanzamiento':<15}")
    print("-" * 100)
    for i, vj in enumerate(videojuegos, 1):
        nombre = vj['nombre'][:24]
        precio = str(vj['precio'])[:9]
        plataforma = vj['plataforma'][:14]
        descripcion = vj['descripcion'][:29]

        # Mostrar solo YYYY-MM-DD si tiene formato de fecha completa
        fecha = vj['fecha_lanzamiento']
        if fecha != "N/A" and len(fecha) >= 10:
            fecha = fecha[:10]

        print(f"{i:<4}{nombre:<25}{precio:<10}{plataforma:<15}{descripcion:<30}{fecha:<15}")
    print("-" * 100)

def buscar_videojuego(nombre):
    encontrados = [vj for vj in videojuegos if nombre.lower() in vj['nombre'].lower()]
    if encontrados:
        print(f"{'Nombre':<25}{'Precio':<10}{'Plataforma':<15}{'Descripción':<30}{'Fecha Lanzamiento':<15}")
        print("-" * 95)
        for vj in encontrados:
            nombre = vj['nombre'][:24]
            precio = str(vj['precio'])[:9]
            plataforma = vj['plataforma'][:14]
            descripcion = vj['descripcion'][:29]
            fecha = vj['fecha_lanzamiento']
            if fecha != "N/A" and len(fecha) >= 10:
                fecha = fecha[:10]
            print(f"{nombre:<25}{precio:<10}{plataforma:<15}{descripcion:<30}{fecha:<15}")
        print("-" * 95)
        print("\n\t.::✅ ¡LA OPERACIÓN SE REALIZÓ CON ÉXITO! ✅::.\n")
    else:
        print("❌ No se encontró el videojuego.\n")

def modificar_videojuego(index, nombre, precio, plataforma, descripcion, fecha_lanzamiento):
    if fecha_lanzamiento and len(fecha_lanzamiento) == 10:
        fecha_lanzamiento += " 00:00:00"

    if not fecha_lanzamiento.strip():
        fecha_lanzamiento = "N/A"

    if 0 <= index < len(videojuegos):
        videojuegos[index] = {
            "nombre": nombre,
            "precio": precio,
            "plataforma": plataforma,
            "descripcion": descripcion,
            "fecha_lanzamiento": fecha_lanzamiento,
        }
        print("✅ Videojuego modificado con éxito.\n")
    else:
        print("❌ Índice inválido.\n")

def eliminar_videojuego(index):
    if 0 <= index < len(videojuegos):
        eliminado = videojuegos.pop(index)
        print(f"🗑 Videojuego '{eliminado['nombre']}' eliminado.\n")
    else:
        print("❌ Índice inválido.\n")

def vaciar_lista():
    videojuegos.clear()
    print("🧹 Lista de videojuegos vaciada.\n")

