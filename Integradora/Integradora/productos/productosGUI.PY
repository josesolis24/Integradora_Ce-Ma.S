import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion


class ProductosGUI:
    def __init__(self, master=None):
        self.master = tk.Toplevel(master)
        self.master.title("Productos")
        self.master.geometry("1500x500")

        # 🎨 COLORES
        self.color_fondo = "#F8C8DC"
        self.color_boton = "#FFFFFF"

        # Marco principal
        frame = tk.Frame(self.master, bg=self.color_fondo)
        frame.pack(fill="both", expand=True)

        # Título
        tk.Label(frame, text="Gestión de Productos", font=("Arial", 24, "bold"), bg=self.color_fondo).pack(pady=20)

        # Formulario
        form_frame = tk.Frame(frame, bg=self.color_fondo)
        form_frame.pack()

        # ---------------------------------------------------
        # CAMPOS DEL FORMULARIO
        # ---------------------------------------------------

        # Nombre
        tk.Label(form_frame, text="Nombre:", bg=self.color_fondo, font=("Arial", 12)).grid(
            row=0, column=0, padx=10, pady=10, sticky="e")
        self.nombre_entry = tk.Entry(form_frame, font=("Arial", 12), width=40)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=10)

        # Descripción (CAMBIO: ahora es igual al de nombre)
        tk.Label(form_frame, text="Descripción:", bg=self.color_fondo, font=("Arial", 12)).grid(
            row=1, column=0, padx=10, pady=10, sticky="e")
        self.descripcion_entry = tk.Entry(form_frame, font=("Arial", 12), width=40)
        self.descripcion_entry.grid(row=1, column=1, padx=10, pady=10)

        # Precio
        tk.Label(form_frame, text="Precio:", bg=self.color_fondo, font=("Arial", 12)).grid(
            row=2, column=0, padx=10, pady=10, sticky="e")
        self.precio_entry = tk.Entry(form_frame, font=("Arial", 12), width=40)
        self.precio_entry.grid(row=2, column=1, padx=10, pady=10)

        # Stock
        tk.Label(form_frame, text="Stock:", bg=self.color_fondo, font=("Arial", 12)).grid(
            row=3, column=0, padx=10, pady=10, sticky="e")
        self.stock_entry = tk.Entry(form_frame, font=("Arial", 12), width=40)
        self.stock_entry.grid(row=3, column=1, padx=10, pady=10)

        # Categoría
        tk.Label(form_frame, text="Categoría:", bg=self.color_fondo, font=("Arial", 12)).grid(
            row=4, column=0, padx=10, pady=10, sticky="e")
        self.categoria_combo = ttk.Combobox(form_frame, font=("Arial", 12), width=38, state="readonly")
        self.categoria_combo.grid(row=4, column=1, padx=10, pady=10)

        # Proveedor
        tk.Label(form_frame, text="Proveedor:", bg=self.color_fondo, font=("Arial", 12)).grid(
            row=5, column=0, padx=10, pady=10, sticky="e")
        self.proveedor_combo = ttk.Combobox(form_frame, font=("Arial", 12), width=38, state="readonly")
        self.proveedor_combo.grid(row=5, column=1, padx=10, pady=10)

        # Cargar combos
        self.cargar_categorias()
        self.cargar_proveedores()

        # ---------------------------------------------------
        # BOTONES CRUD
        # ---------------------------------------------------
        botones_frame = tk.Frame(frame, bg=self.color_fondo)
        botones_frame.pack(pady=20)

        tk.Button(botones_frame, text="Agregar", width=15, bg=self.color_boton,
                  command=self.agregar_producto).grid(row=0, column=0, padx=10)

        tk.Button(botones_frame, text="Modificar", width=15, bg=self.color_boton,
                  command=self.modificar_producto).grid(row=0, column=1, padx=10)

        tk.Button(botones_frame, text="Eliminar", width=15, bg=self.color_boton,
                  command=self.eliminar_producto).grid(row=0, column=2, padx=10)

        tk.Button(botones_frame, text="Regresar", width=15, bg=self.color_boton,
                  command=self.master.destroy).grid(row=0, column=3, padx=10)

        # ---------------------------------------------------
        # TABLA
        # ---------------------------------------------------
        columnas = ("id", "nombre", "descripcion", "precio", "stock", "categoria", "proveedor")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tabla.heading(col, text=col.upper())

        self.tabla.pack(pady=20)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)

        self.cargar_tabla()

    # ====================================================
    # CARGAR COMBOS
    # ====================================================
    def cargar_categorias(self):
        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id_categoria, nombre FROM categorias")
        datos = cursor.fetchall()

        self.categorias = {nombre: id for id, nombre in datos}
        self.categoria_combo["values"] = list(self.categorias.keys())

        conexion.close()

    def cargar_proveedores(self):
        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id_proveedor, nombre FROM proveedores")
        datos = cursor.fetchall()

        self.proveedores = {nombre: id for id, nombre in datos}
        self.proveedor_combo["values"] = list(self.proveedores.keys())

        conexion.close()

    # ====================================================
    # CRUD
    # ====================================================
    def agregar_producto(self):
        nombre = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()
        categoria = self.categoria_combo.get()
        proveedor = self.proveedor_combo.get()

        if not all([nombre, descripcion, precio, stock, categoria, proveedor]):
            messagebox.showerror("Error", "Rellena todos los campos")
            return

        id_categoria = self.categorias[categoria]
        id_proveedor = self.proveedores[proveedor]

        conexion = crear_conexion()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, id_proveedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, descripcion, precio, stock, id_categoria, id_proveedor))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Producto agregado")
        self.cargar_tabla()

    def modificar_producto(self):
        selected = self.tabla.focus()
        if not selected:
            messagebox.showerror("Error", "Selecciona un producto")
            return

        valores = self.tabla.item(selected, "values")
        id_producto = valores[0]

        nombre = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()
        categoria = self.categoria_combo.get()
        proveedor = self.proveedor_combo.get()

        id_categoria = self.categorias[categoria]
        id_proveedor = self.proveedores[proveedor]

        conexion = crear_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s,
                                 id_categoria=%s, id_proveedor=%s
            WHERE id_producto=%s
        """
        cursor.execute(sql, (nombre, descripcion, precio, stock, id_categoria, id_proveedor, id_producto))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Producto actualizado")
        self.cargar_tabla()

    def eliminar_producto(self):
        selected = self.tabla.focus()
        if not selected:
            messagebox.showerror("Error", "Selecciona un producto")
            return

        valores = self.tabla.item(selected, "values")
        id_producto = valores[0]

        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Producto eliminado")
        self.cargar_tabla()

    # ====================================================
    # TABLA Y SELECCIÓN
    # ====================================================
    def cargar_tabla(self):
        conexion = crear_conexion()
        cursor = conexion.cursor()

        sql = """
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock,
               c.nombre, pr.nombre
        FROM productos p
        INNER JOIN categorias c ON p.id_categoria = c.id_categoria
        INNER JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
        """
        cursor.execute(sql)

        registros = cursor.fetchall()

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for fila in registros:
            self.tabla.insert("", tk.END, values=fila)

        conexion.close()

    def seleccionar_fila(self, event):
        selected = self.tabla.focus()
        if not selected:
            return

        valores = self.tabla.item(selected, "values")

        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, valores[1])

        self.descripcion_entry.delete(0, tk.END)
        self.descripcion_entry.insert(0, valores[2])

        self.precio_entry.delete(0, tk.END)
        self.precio_entry.insert(0, valores[3])

        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, valores[4])

        self.categoria_combo.set(valores[5])
        self.proveedor_combo.set(valores[6])
