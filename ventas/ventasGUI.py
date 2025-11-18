import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion
from datetime import datetime


class VentasGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Ventas")
        self.geometry("750x500")

        tk.Label(self, text="Módulo de Ventas", font=("Arial", 16, "bold")).pack(pady=10)

        # --- FORMULARIO ---
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="ID Producto:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_producto = tk.Entry(frame, width=25)
        self.entry_producto.grid(row=0, column=1)

        tk.Label(frame, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_cantidad = tk.Entry(frame, width=25)
        self.entry_cantidad.grid(row=1, column=1)

        # --- BOTONES ---
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Registrar Venta", width=18,
                  command=self.registrar_venta).grid(row=0, column=0, padx=5)

        tk.Button(frame_btn, text="Eliminar Seleccionada", width=18,
                  command=self.eliminar_venta).grid(row=0, column=1, padx=5)

        tk.Button(frame_btn, text="Regresar al Menú", width=18,
                  command=self.destroy).grid(row=0, column=2, padx=5)

        # --- TABLA ---
        self.tabla = ttk.Treeview(self, columns=("ID", "Producto", "Cantidad", "Fecha", "Total"), show="headings")
        
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Producto", text="Producto ID")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Total", text="Total $")

        self.tabla.column("ID", width=50)
        self.tabla.column("Producto", width=100)
        self.tabla.column("Cantidad", width=80)
        self.tabla.column("Fecha", width=120)
        self.tabla.column("Total", width=120)

        self.tabla.pack(pady=10, fill="both", expand=True)

        self.mostrar_ventas()


    def registrar_venta(self):
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

        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT precio FROM productos WHERE id = %s", (id_producto,))
        resultado = cursor.fetchone()

        if not resultado:
            messagebox.showerror("❌ Error", "El producto NO existe.")
            conexion.close()
            return

        precio = resultado[0]
        total = precio * cantidad
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            "INSERT INTO ventas (fecha, id_producto, cantidad, total) VALUES (%s, %s, %s, %s)",
            (fecha_hoy, id_producto, cantidad, total)
        )

        conexion.commit()
        conexion.close()

        messagebox.showinfo("✔️ Éxito", f"Venta registrada (Total: ${total:.2f})")
        self.entry_producto.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)

        self.mostrar_ventas()


    def mostrar_ventas(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, id_producto, cantidad, DATE_FORMAT(fecha, '%d-%m-%Y'), total FROM ventas")
        ventas = cursor.fetchall()
        conexion.close()

        for v in ventas:
            self.tabla.insert("", tk.END, values=v)


    def eliminar_venta(self):
        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning("⚠️ Error", "Selecciona una venta.")
            return

        id_venta = self.tabla.item(seleccionado)["values"][0]

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM ventas WHERE id = %s", (id_venta,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("🗑️ Eliminado", "Venta eliminada correctamente.")
        self.mostrar_ventas()
