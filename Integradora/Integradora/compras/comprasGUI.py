import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion
from datetime import datetime


class ComprasGUI(tk.Toplevel):
    def __init__(self, menu_principal):
        super().__init__(menu_principal)
        self.menu_principal = menu_principal
        self.title("Gestión de Compras")
        self.geometry("850x700")

        # 🎨 COLORES
        self.color_fondo = "#FADADD"
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

        # ID PRODUCTO
        tk.Label(frame, text="ID Producto:", font=("Arial", 12),
                 bg=self.color_fondo, fg=self.color_texto).grid(row=0, column=0, padx=10, pady=10)

        self.entry_producto = tk.Entry(frame, width=30)
        self.entry_producto.grid(row=0, column=1)

        # CANTIDAD
        tk.Label(frame, text="Cantidad:", font=("Arial", 12),
                 bg=self.color_fondo, fg=self.color_texto).grid(row=1, column=0, padx=10, pady=10)

        self.entry_cantidad = tk.Entry(frame, width=30)
        self.entry_cantidad.grid(row=1, column=1)

        # ID PROVEEDOR
        tk.Label(frame, text="ID Proveedor:", font=("Arial", 12),
                 bg=self.color_fondo, fg=self.color_texto).grid(row=2, column=0, padx=10, pady=10)

        self.entry_proveedor = tk.Entry(frame, width=30)
        self.entry_proveedor.grid(row=2, column=1)

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
            columns=("ID", "Producto", "Cantidad", "Proveedor", "Total", "Fecha"),
            show="headings"
        )

        for col in ("ID", "Producto", "Cantidad", "Proveedor", "Total", "Fecha"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=130)

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
    # REGISTRAR COMPRA
    # ============================

    def registrar_compra(self):
        id_producto = self.entry_producto.get()
        cantidad = self.entry_cantidad.get()
        id_proveedor = self.entry_proveedor.get()

        if not id_producto or not cantidad:
            messagebox.showwarning("⚠️ Campos vacíos", "ID Producto y Cantidad son obligatorios.")
            return

        try:
            cantidad = float(cantidad)
        except:
            messagebox.showerror("❌ Error", "La cantidad debe ser numérica.")
            return

        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            # Obtener precio del producto
            cursor.execute("SELECT precio FROM productos WHERE id_producto = %s", (id_producto,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("❌ Error", "El ID de producto no existe.")
                conexion.close()
                return

            precio = float(result[0])
            total = cantidad * precio

            fecha_hoy = datetime.now().strftime("%Y-%m-%d")

            # Insertar con proveedor y total
            cursor.execute(
                "INSERT INTO compras (fecha, id_proveedor, id_producto, cantidad, total) VALUES (%s, %s, %s, %s, %s)",
                (fecha_hoy, id_proveedor if id_proveedor != "" else None, id_producto, cantidad, total)
            )

            conexion.commit()
            conexion.close()

            messagebox.showinfo("✔️ Éxito", "Compra registrada con éxito.")
            self.mostrar_compras()

            self.entry_producto.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
            self.entry_proveedor.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al registrar compra:\n{e}")

    # ============================
    # MOSTRAR COMPRAS
    # ============================

    def mostrar_compras(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id_compra, id_producto, cantidad, 
                   IFNULL(id_proveedor, 'N/A'),
                   IFNULL(total, 0),
                   DATE_FORMAT(fecha, '%d-%m-%Y')
            FROM compras
        """)

        compras = cursor.fetchall()
        conexion.close()

        for compra in compras:
            self.tabla.insert("", tk.END, values=compra)

    # ============================
    # ELIMINAR COMPRA
    # ============================

    def eliminar_compra(self):
        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning("⚠️ Selección requerida", "Seleccione una compra para eliminar.")
            return

        id_compra = self.tabla.item(seleccionado)["values"][0]

        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM compras WHERE id_compra = %s", (id_compra,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("🗑️ Eliminado", "Compra eliminada correctamente.")
        self.mostrar_compras()

    # ============================
    # VOLVER
    # ============================

    def volver_al_menu(self):
        self.destroy()
        self.menu_principal.deiconify()

