import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion
from datetime import datetime


class ComprasGUI(tk.Toplevel):
    def __init__(self, menu_principal):
        super().__init__(menu_principal)
        self.menu_principal = menu_principal
        self.title("Gestión de Compras")
        self.geometry("800x650")

        # 🎨 COLORES QUE PEDISTE
        self.color_fondo = "#FADADD"   # Rosa bajito
        self.color_boton = "white"
        self.color_texto = "black"

        self.config(bg=self.color_fondo)

        tk.Label(
            self,
            text="Módulo de Compras",
            font=("Arial", 18, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(pady=15)

        # --- FRAME DE ENTRADAS ---
        frame = tk.Frame(self, bg=self.color_fondo)
        frame.pack(pady=15)

        tk.Label(
            frame,
            text="ID Producto:",
            font=("Arial", 12),
            bg=self.color_fondo,
            fg=self.color_texto
        ).grid(row=0, column=0, padx=10, pady=10)

        self.entry_producto = tk.Entry(frame, width=30)
        self.entry_producto.grid(row=0, column=1)

        tk.Label(
            frame,
            text="Cantidad:",
            font=("Arial", 12),
            bg=self.color_fondo,
            fg=self.color_texto
        ).grid(row=1, column=0, padx=10, pady=10)

        self.entry_cantidad = tk.Entry(frame, width=30)
        self.entry_cantidad.grid(row=1, column=1)

        # --- BOTÓN REGISTRAR ---
        tk.Button(
            self,
            text="Registrar Compra",
            width=30,
            bg=self.color_boton,
            fg=self.color_texto,
            command=self.registrar_compra
        ).pack(pady=15)

        # --- TABLA ---
        self.tabla = ttk.Treeview(
            self,
            columns=("ID", "Producto", "Cantidad", "Fecha"),
            show="headings"
        )

        for col in ("ID", "Producto", "Cantidad", "Fecha"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150)

        self.tabla.pack(pady=10, fill="both", expand=True)

        # --- BOTÓN ELIMINAR ---
        tk.Button(
            self,
            text="Eliminar Compra Seleccionada",
            width=30,
            bg=self.color_boton,
            fg=self.color_texto,
            command=self.eliminar_compra
        ).pack(pady=5)

        # --- VOLVER ---
        tk.Button(
            self,
            text="⬅ Volver al Menú Principal",
            width=30,
            bg=self.color_boton,
            fg=self.color_texto,
            command=self.volver_al_menu
        ).pack(pady=15)

        self.mostrar_compras()

    # ============================
    # FUNCIONES
    # ============================

    def registrar_compra(self):
        id_producto = self.entry_producto.get()
        cantidad = self.entry_cantidad.get()

        if not id_producto or not cantidad:
            messagebox.showwarning("⚠️ Campos vacíos", "Todos los campos son obligatorios.")
            return

        try:
            cantidad = int(cantidad)
        except:
            messagebox.showerror("❌ Error", "La cantidad debe ser numérica.")
            return

        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                "INSERT INTO compras (fecha, id_producto, cantidad) VALUES (%s, %s, %s)",
                (fecha_hoy, id_producto, cantidad)
            )

            conexion.commit()
            conexion.close()

            messagebox.showinfo("✔️ Éxito", "Compra registrada.")
            self.mostrar_compras()

            self.entry_producto.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al registrar compra:\n{e}")

    def mostrar_compras(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        conexion = crear_conexion()
        cursor = conexion.cursor()

        # CORREGIDO: id → id_compra
        cursor.execute("""
            SELECT id_compra, id_producto, cantidad,
                   DATE_FORMAT(fecha, '%d-%m-%Y')
            FROM compras
        """)

        compras = cursor.fetchall()
        conexion.close()

        for compra in compras:
            self.tabla.insert("", tk.END, values=compra)

    def eliminar_compra(self):
        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning("⚠️ Selección requerida", "Seleccione una compra para eliminar.")
            return

        id_compra = self.tabla.item(seleccionado)["values"][0]

        conexion = crear_conexion()
        cursor = conexion.cursor()

        # CORREGIDO: id → id_compra
        cursor.execute("DELETE FROM compras WHERE id_compra = %s", (id_compra,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("🗑️ Eliminado", "Compra eliminada correctamente.")
        self.mostrar_compras()

    def volver_al_menu(self):
        self.destroy()
        self.menu_principal.deiconify()
