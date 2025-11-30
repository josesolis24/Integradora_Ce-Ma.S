import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion


class ProveedoresGUI:
    def __init__(self, master=None, regresar_callback=None):
        self.master = tk.Toplevel(master)
        self.master.title("Gestión de Proveedores")
        self.master.geometry("900x500")

        self.regresar_callback = regresar_callback

        # 🎨 COLORES
        rosa_suave = "#FFE4E9"
        blanco = "#FFFFFF"

        # Fondo rosa
        self.master.configure(bg=rosa_suave)

        # ------------------------------
        # --- TÍTULO
        # ------------------------------
        tk.Label(
            self.master,
            text="Módulo de Proveedores",
            font=("Arial", 16, "bold"),
            bg=rosa_suave
        ).pack(pady=10)

        # ------------------------------
        # --- FORMULARIO
        # ------------------------------
        frame_form = tk.Frame(self.master, bg=blanco, bd=2, relief="ridge")
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Nombre:", bg=blanco).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame_form, text="Teléfono:", bg=blanco).grid(row=1, column=0, padx=5, pady=5)
        tk.Label(frame_form, text="Dirección:", bg=blanco).grid(row=2, column=0, padx=5, pady=5)

        self.entry_nombre = tk.Entry(frame_form)
        self.entry_telefono = tk.Entry(frame_form)
        self.entry_direccion = tk.Entry(frame_form)

        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        self.entry_telefono.grid(row=1, column=1, padx=5, pady=5)
        self.entry_direccion.grid(row=2, column=1, padx=5, pady=5)

        # BOTONES (se mantienen sus colores originales)
        tk.Button(frame_form, text="Agregar", command=self.agregar_proveedor,
                  bg="#90EE90").grid(row=3, column=0, padx=5, pady=10)

        tk.Button(frame_form, text="Actualizar", command=self.actualizar_proveedor,
                  bg="#87CEEB").grid(row=3, column=1, padx=5, pady=10)

        tk.Button(frame_form, text="Eliminar", command=self.eliminar_proveedor,
                  bg="#FF7F7F").grid(row=3, column=2, padx=5, pady=10)

        # ------------------------------
        # --- TABLA
        # ------------------------------
        style = ttk.Style()
        style.configure("Treeview", background=blanco, fieldbackground=blanco)
        style.configure("Treeview.Heading", background="#FFC0CB")

        self.tabla = ttk.Treeview(self.master, columns=("id", "nombre", "telefono", "direccion"), show="headings")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("telefono", text="Teléfono")
        self.tabla.heading("direccion", text="Dirección")

        self.tabla.column("id", width=50)
        self.tabla.pack(fill="both", expand=True, pady=10)

        self.tabla.bind("<<TreeviewSelect>>", self.cargar_datos_seleccionados)

        self.mostrar_proveedores()

        # BOTÓN REGRESAR (gris como en otros módulos)
        tk.Button(self.master, text="Regresar", command=self.regresar,
                  bg="#D3D3D3").pack(pady=10)

    # ---------------------------------------------------------
    def agregar_proveedor(self):
        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()
        direccion = self.entry_direccion.get()

        if not nombre:
            messagebox.showwarning("Error", "El nombre es obligatorio")
            return

        cnx = crear_conexion()
        cursor = cnx.cursor()

        sql = "INSERT INTO proveedores (nombre, telefono, direccion) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, telefono, direccion))
        cnx.commit()
        cnx.close()

        messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
        self.mostrar_proveedores()
        self.limpiar_campos()

    # ---------------------------------------------------------
    def mostrar_proveedores(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        cnx = crear_conexion()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM proveedores")
        datos = cursor.fetchall()
        cnx.close()

        for fila in datos:
            self.tabla.insert("", "end", values=fila)

    # ---------------------------------------------------------
    def cargar_datos_seleccionados(self, event):
        item = self.tabla.selection()
        if not item:
            return

        fila = self.tabla.item(item)["values"]

        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)

        self.entry_nombre.insert(0, fila[1])
        self.entry_telefono.insert(0, fila[2])
        self.entry_direccion.insert(0, fila[3])

    # ---------------------------------------------------------
    def actualizar_proveedor(self):
        item = self.tabla.selection()
        if not item:
            messagebox.showwarning("Error", "Selecciona un proveedor")
            return

        id_proveedor = self.tabla.item(item)["values"][0]

        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()
        direccion = self.entry_direccion.get()

        cnx = crear_conexion()
        cursor = cnx.cursor()

        sql = """UPDATE proveedores SET nombre=%s, telefono=%s, direccion=%s WHERE id_proveedor=%s"""
        cursor.execute(sql, (nombre, telefono, direccion, id_proveedor))
        cnx.commit()
        cnx.close()

        messagebox.showinfo("Éxito", "Proveedor actualizado")
        self.mostrar_proveedores()

    # ---------------------------------------------------------
    def eliminar_proveedor(self):
        item = self.tabla.selection()
        if not item:
            messagebox.showwarning("Error", "Selecciona un proveedor")
            return

        id_proveedor = self.tabla.item(item)["values"][0]

        cnx = crear_conexion()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM proveedores WHERE id_proveedor=%s", (id_proveedor,))
        cnx.commit()
        cnx.close()

        messagebox.showinfo("Éxito", "Proveedor eliminado")
        self.mostrar_proveedores()
        self.limpiar_campos()

    # ---------------------------------------------------------
    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)

    # ---------------------------------------------------------
    def regresar(self):
        if self.regresar_callback:
            self.regresar_callback()
        self.master.destroy()
