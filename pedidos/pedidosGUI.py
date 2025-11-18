import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from conexionBD import crear_conexion


class PedidosGUI:
    def __init__(self, master=None, regresar_callback=None):
        self.master = tk.Toplevel(master)
        self.master.title("Gestión de Pedidos")
        self.master.geometry("800x600")

        self.regresar_callback = regresar_callback

        tk.Label(self.master, text="Módulo de Pedidos", font=("Arial", 18, "bold")).pack(pady=10)

        frame = tk.Frame(self.master)
        frame.pack(pady=10)

        campos = [
            ("Cliente:", "cliente"),
            ("Producto:", "producto"),
            ("Cantidad:", "cantidad"),
            ("Precio (unidad):", "precio"),
            ("Anticipo:", "anticipo"),
            ("Fecha entrega (DD-MM-YYYY):", "fecha"),
            ("Estado:", "estado")
        ]

        self.entries = {}

        for i, (texto, key) in enumerate(campos):
            tk.Label(frame, text=texto).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            self.entries[key] = tk.Entry(frame)
            self.entries[key].grid(row=i, column=1, padx=5, pady=5)

        self.entries["estado"].insert(0, "Pendiente")

        tk.Button(self.master, text="Registrar Pedido", width=30,
                  command=self.registrar_pedido).pack(pady=10)

        tk.Button(self.master, text="Regresar al Menú Principal", width=30,
                  command=self.regresar_menu).pack(pady=5)

        columnas = ("ID", "Cliente", "Producto", "Cantidad", "Precio", "Anticipo", "Fecha Entrega", "Estado")
        self.tabla = ttk.Treeview(self.master, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)

        self.tabla.pack(pady=10)

        tk.Button(self.master, text="Eliminar Pedido Seleccionado", width=30,
                  command=self.eliminar_pedido).pack(pady=10)

        self.mostrar_pedidos()


    def registrar_pedido(self):
        datos = {key: entry.get() for key, entry in self.entries.items()}

        if any(not x for x in datos.values()):
            messagebox.showwarning("⚠️ Campos vacíos", "Todos los campos son obligatorios.")
            return

        try:
            fecha_guardar = datetime.strptime(datos["fecha"], "%d-%m-%Y").strftime("%Y-%m-%d")

            conexion = crear_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO pedidos (cliente, producto, cantidad, precio, anticipo, fecha_entrega, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (datos["cliente"], datos["producto"], datos["cantidad"], datos["precio"],
                  datos["anticipo"], fecha_guardar, datos["estado"]))

            conexion.commit()
            conexion.close()

            messagebox.showinfo("✔️ Registrado", "Pedido registrado correctamente.")
            self.mostrar_pedidos()

            for entry in self.entries.values():
                entry.delete(0, tk.END)

            self.entries["estado"].insert(0, "Pendiente")

        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al registrar pedido:\n{e}")


    def mostrar_pedidos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, cliente, producto, cantidad, precio, anticipo,
            DATE_FORMAT(fecha_entrega, '%d-%m-%Y'), estado FROM pedidos
        """)
        pedidos = cursor.fetchall()
        conexion.close()

        for pedido in pedidos:
            self.tabla.insert("", tk.END, values=pedido)


    def eliminar_pedido(self):
        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning("⚠️ Selección requerida", "Seleccione un pedido para eliminar.")
            return

        id_pedido = self.tabla.item(seleccionado)["values"][0]

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id = %s", (id_pedido,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("🗑️ Eliminado", "Pedido eliminado correctamente.")
        self.mostrar_pedidos()


    def regresar_menu(self):
        self.master.destroy()
        if self.regresar_callback:
            self.regresar_callback()
