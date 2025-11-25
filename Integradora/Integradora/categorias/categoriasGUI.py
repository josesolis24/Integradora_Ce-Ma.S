import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion


class CategoriasGUI:
    def __init__(self, parent):
        self.parent = parent
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Categorías")
        self.ventana.geometry("600x520")

        self.ventana.config(bg="#FADADD")

        self.crear_gui()

    def crear_gui(self):
        tk.Label(
            self.ventana,
            text="Gestión de Categorías",
            font=("Arial", 16, "bold"),
            bg="#FADADD",
            fg="black"
        ).pack(pady=10)

        tk.Label(
            self.ventana,
            text="Nombre de la categoría:",
            bg="#FADADD",
            fg="black"
        ).pack()

        self.entry_nombre = tk.Entry(self.ventana, width=40)
        self.entry_nombre.pack(pady=5)

        frame_btn = tk.Frame(self.ventana, bg="#FADADD")
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Agregar", width=15,
                  bg="white", fg="black",
                  command=self.agregar_categoria).grid(row=0, column=0, padx=5)

        tk.Button(frame_btn, text="Eliminar", width=15,
                  bg="white", fg="black",
                  command=self.eliminar_categoria).grid(row=0, column=1, padx=5)

        tk.Button(frame_btn, text="Regresar", width=15,
                  bg="white", fg="black",
                  command=self.ventana.destroy).grid(row=0, column=2, padx=5)

        self.tabla = ttk.Treeview(self.ventana, columns=("id", "nombre"), show="headings")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")

        self.tabla.column("id", width=50)
        self.tabla.column("nombre", width=300)
        self.tabla.pack(pady=10, fill="both", expand=True)

        self.cargar_categorías()

    # ===============================
    # Agregar Categoría
    # ===============================
    def agregar_categoria(self):
        nombre = self.entry_nombre.get().strip()

        if not nombre:
            messagebox.showerror("Error", "Debes ingresar un nombre.")
            return

        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
        conn.commit()
        conn.close()

        self.entry_nombre.delete(0, tk.END)
        messagebox.showinfo("Éxito", "Categoría agregada correctamente.")
        self.cargar_categorías()

    # ===============================
    # Cargar Categorías
    # ===============================
    def cargar_categorías(self):
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categorias")
        filas = cursor.fetchall()
        conn.close()

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for fila in filas:
            self.tabla.insert("", "end", values=fila)

    # ===============================
    # Eliminar Categoría
    # ===============================
    def eliminar_categoria(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una categoría.")
            return

        item = self.tabla.item(seleccion)
        categoria_id = item["values"][0]

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar la categoría con ID {categoria_id}?"
        )

        if not confirmar:
            return

        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM categorias WHERE id_categoria = %s", (categoria_id,))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Categoría eliminada correctamente.")
            self.cargar_categorías()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
