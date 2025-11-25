from conexionBD import crear_conexion
from funciones.funciones import limpiar_pantalla, pausa
from tabulate import tabulate

def menu_pedidos():
    while True:
        limpiar_pantalla()
        print("=== MÓDULO DE PEDIDOS ===")
        print("1. Registrar nuevo pedido")
        print("2. Ver pedidos registrados")
        print("3. Actualizar estado de pedido")
        print("4. Eliminar pedido")
        print("5. Volver al menú principal")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            registrar_pedido()
        elif opcion == "2":
            ver_pedidos()
        elif opcion == "3":
            actualizar_estado_pedido()
        elif opcion == "4":
            eliminar_pedido()
        elif opcion == "5":
            break
        else:
            print("⚠️ Opción no válida.")
            pausa()


def registrar_pedido():
    conexion = crear_conexion()
    if not conexion:
        print("❌ No se pudo conectar a la base de datos.")
        pausa()
        return

    cliente = input("Nombre del cliente: ")
    producto = input("Producto pedido: ")
    try:
        cantidad = int(input("Cantidad: "))
    except ValueError:
        print("⚠️ Cantidad inválida.")
        pausa()
        return

    try:
        precio = float(input("Precio total del pedido (en MXN): "))
        if precio <= 0:
            print("⚠️ El precio debe ser mayor que 0.")
            pausa()
            return
    except ValueError:
        print("⚠️ Valor inválido para el precio.")
        pausa()
        return

    fecha_entrega = input("Fecha de entrega (DD-MM-YYYY): ")

    da_anticipo = input("¿El cliente dará anticipo? (s/n): ").strip().lower()
    anticipo = 0.0
    if da_anticipo == "s":
        try:
            anticipo = float(input("Monto del anticipo (0 - 50000): "))
            if anticipo < 0 or anticipo > 50000:
                print("⚠️ El anticipo debe estar entre 0 y 50000.")
                pausa()
                return
        except ValueError:
            print("⚠️ Valor inválido. Se registrará anticipo 0.")
            anticipo = 0.0

    subtotal = precio - anticipo
    if subtotal < 0:
        print("⚠️ El anticipo no puede ser mayor que el precio total.")
        pausa()
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO pedidos (cliente, producto, cantidad, total, anticipo, fecha_entrega, estado)
            VALUES (%s, %s, %s, %s, %s, %s, 'Pendiente')
        """, (cliente, producto, cantidad, precio, anticipo, fecha_entrega))
        conexion.commit()

        print("\n✅ Pedido registrado con éxito.")
        print(f"💵 Precio total: ${precio:,.2f}")
        print(f"💰 Anticipo: ${anticipo:,.2f}")
        print(f"🧾 Subtotal a pagar: ${subtotal:,.2f}")
    except Exception as e:
        print(f"⚠️ Error al registrar pedido: {e}")
    finally:
        conexion.close()
        pausa()


def ver_pedidos():
    conexion = crear_conexion()
    if not conexion:
        print("❌ No se pudo conectar a la base de datos.")
        pausa()
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, cliente, producto, cantidad, total, anticipo, fecha_entrega, estado FROM pedidos")
        pedidos = cursor.fetchall()

        if not pedidos:
            print("\n⚠️ No hay pedidos registrados.")
        else:
            headers = ["ID", "Cliente", "Producto", "Cantidad", "Total", "Anticipo", "Fecha entrega", "Estado"]
            print("\n=== LISTA DE PEDIDOS ===")
            print(tabulate(pedidos, headers, tablefmt="grid"))
    except Exception as e:
        print(f"⚠️ Error al consultar pedidos: {e}")
    finally:
        conexion.close()
        pausa()


def actualizar_estado_pedido():
    conexion = crear_conexion()
    if not conexion:
        print("❌ No se pudo conectar a la base de datos.")
        pausa()
        return

    pedido_id = input("ID del pedido a actualizar: ")

    print("\nSelecciona el nuevo estado:")
    print("1. Pendiente")
    print("2. En proceso")
    print("3. Entregado")
    print("4. Cancelado")
    op = input("Opción: ")

    estados = {
        "1": "Pendiente",
        "2": "En proceso",
        "3": "Entregado",
        "4": "Cancelado"
    }

    nuevo_estado = estados.get(op)
    if not nuevo_estado:
        print("⚠️ Opción inválida. No se realizó ningún cambio.")
        pausa()
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (nuevo_estado, pedido_id))
        conexion.commit()
        print(f"✅ Estado del pedido actualizado a '{nuevo_estado}'.")
    except Exception as e:
        print(f"⚠️ Error al actualizar estado: {e}")
    finally:
        conexion.close()
        pausa()


def eliminar_pedido():
    conexion = crear_conexion()
    if not conexion:
        print("❌ No se pudo conectar a la base de datos.")
        pausa()
        return

    pedido_id = input("ID del pedido a eliminar: ")

    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id = %s", (pedido_id,))
        conexion.commit()
        print("🗑️ Pedido eliminado correctamente.")
    except Exception as e:
        print(f"⚠️ Error al eliminar pedido: {e}")
    finally:
        conexion.close()
        pausa()
