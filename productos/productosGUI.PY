import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion


class ProductosGUI:
    def __init__(self, parent):
        self.parent = parent
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Productos")
        self.ventana.geometry("700x600")

        self.categorias = []
        self.crear_gui()

    def crear_gui(self):

        tk.Label(self.ventana, text="Gestión de Productos",
                 font=("Arial", 16, "bold")).pack(pady=10)

        frame_inputs = tk.Frame(self.ventana)
        frame_inputs.pack(pady=10)

        # === CAMPOS ===
        tk.Label(frame_inputs, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_inputs, width=30)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(frame_inputs, text="Precio:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_precio = tk.Entry(frame_inputs, width=30)
        self.entry_precio.grid(row=1, column=1)

        tk.Label(frame_inputs, text="Stock:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_stock = tk.Entry(frame_inputs, width=30)
        self.entry_stock.grid(row=2, column=1)

        tk.Label(frame_inputs, text="Categoría:").grid(row=3, column=0, padx=5, pady=5)
        self.combo_categoria = ttk.Combobox(frame_inputs, width=27, state="readonly")
        self.combo_categoria.grid(row=3, column=1)

        # Cargar categorías al iniciar
        self.cargar_categorias()

        # === BOTONES ===
        frame_btn = tk.Frame(self.ventana)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Agregar", width=15,
                  command=self.agregar_producto).grid(row=0, column=0, padx=5)

        tk.Button(frame_btn, text="Eliminar", width=15,
                  command=self.eliminar_producto).grid(row=0, column=1, padx=5)

        tk.Button(frame_btn, text="Regresar", width=15,
                  command=self.ventana.destroy).grid(row=0, column=2, padx=5)

        # === TABLA ===
        self.tabla = ttk.Treeview(self.ventana,
                                  columns=("id", "nombre", "precio", "stock", "categoria"),
                                  show="headings")

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")
        self.tabla.heading("categoria", text="Categoría")

        self.tabla.column("id", width=50)
        self.tabla.column("nombre", width=200)
        self.tabla.column("precio", width=100)
        self.tabla.column("stock", width=80)
        self.tabla.column("categoria", width=150)

        self.tabla.pack(pady=10, fill="both", expand=True)

        self.cargar_productos()

    # ============================================================
    #   Cargar Categorías en ComboBox
    # ============================================================
    def cargar_categorias(self):
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM categorias")
        self.categorias = cursor.fetchall()
        conexion.close()

        self.combo_categoria['values'] = [c[1] for c in self.categorias]

    # ============================================================
    #   AGREGAR PRODUCTO
    # ============================================================
    def agregar_producto(self):
        nombre = self.entry_nombre.get().strip()
        precio = self.entry_precio.get().strip()
        stock = self.entry_stock.get().strip()
        categoria_nombre = self.combo_categoria.get()

        if not nombre or not precio or not stock or not categoria_nombre:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            precio = float(precio)
            stock = int(stock)
        except:
            messagebox.showerror("Error", "Precio y Stock deben ser numéricos.")
            return

        # Obtener ID de la categoría seleccionada
        id_categoria = None
        for cat in self.categorias:
            if cat[1] == categoria_nombre:
                id_categoria = cat[0]
                break

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio, stock, id_categoria) VALUES (%s, %s, %s, %s)",
            (nombre, precio, stock, id_categoria)
        )
        conexion.commit()
        conexion.close()

        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.combo_categoria.set("")

        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        self.cargar_productos()

    # ============================================================
    #   CARGAR PRDUCTOS EN LA TABLA
    # ============================================================
    def cargar_productos(self):
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT productos.id, productos.nombre, productos.precio, productos.stock, categorias.nombre
            FROM productos
            LEFT JOIN categorias ON productos.id_categoria = categorias.id
        """)
        filas = cursor.fetchall()
        conexion.close()

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for fila in filas:
            self.tabla.insert("", "end", values=fila)

    # ============================================================
    #   ELIMINAR PRODUCTO
    # ============================================================
    def eliminar_producto(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un producto.")
            return

        item = self.tabla.item(seleccion)
        prod_id = item["values"][0]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que deseas eliminar el producto con ID {prod_id}?"
        )

        if not confirmar:
            return

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (prod_id,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Producto eliminado.")
        self.cargar_productos()
