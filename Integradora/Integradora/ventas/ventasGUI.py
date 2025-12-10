import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion
from datetime import datetime

class VentasGUI(tk.Toplevel):
    def __init__(self, parent, usuario_actual):
        super().__init__(parent)
        self.usuario_actual = usuario_actual

        self.title("Gestión de Ventas")
        self.state('zoomed')
        self.attributes('-fullscreen', False)

        self.color_fondo = "#FADADD"
        self.color_boton = "white"
        self.venta_seleccionada = None

        self.config(bg=self.color_fondo)

        tk.Label(self, text="Módulo de Ventas",
                 font=("Arial", 20, "bold"), bg=self.color_fondo).pack(pady=15)

        # --------- BOTONES ----------
        botones = tk.Frame(self, bg=self.color_fondo)
        botones.pack(pady=10)

        tk.Button(botones, text="Registrar Venta", width=18, bg=self.color_boton,
                  command=self.abrir_formulario).grid(row=0, column=0, padx=10)

        tk.Button(botones, text="Modificar", width=18, bg=self.color_boton,
                  command=self.abrir_formulario_modificar).grid(row=0, column=1, padx=10)

        tk.Button(botones, text="Eliminar", width=18, bg=self.color_boton,
                  command=self.eliminar_venta).grid(row=0, column=2, padx=10)

        tk.Button(botones, text="Regresar", width=18, bg=self.color_boton,
                  command=self.destroy).grid(row=0, column=3, padx=10)

        # -------- TABLA DE VENTAS ----------
        self.tabla = ttk.Treeview(
            self,
            columns=("ID", "Producto", "Cantidad", "Fecha", "Total",
                     "Creado por", "Actualizado por"),
            show="headings",
            height=12
        )

        columnas = [
            ("ID", 60),
            ("Producto", 180),
            ("Cantidad", 90),
            ("Fecha", 120),
            ("Total", 100),
            ("Creado por", 120),
            ("Actualizado por", 120)
        ]

        for col, ancho in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho)

        self.tabla.pack(pady=20, fill="x")
        self.tabla.bind("<ButtonRelease-1>", self.detectar_fila)

        # ==================================================
        # TABLA: PEDIDOS
        # ==================================================
        tk.Label(self, text="Pedidos Registrados",
                 font=("Arial", 16, "bold"), bg=self.color_fondo).pack(pady=10)

        self.tabla_pedidos = ttk.Treeview(
            self,
            columns=("ID Pedido", "Producto", "Cliente", "Cantidad", "Fecha", "Estado"),
            show="headings",
            height=10
        )

        columnas_ped = [
            ("ID Pedido", 90),
            ("Producto", 160),
            ("Cliente", 180),
            ("Cantidad", 90),
            ("Fecha", 120),
            ("Estado", 120)
        ]

        for col, ancho in columnas_ped:
            self.tabla_pedidos.heading(col, text=col)
            self.tabla_pedidos.column(col, width=ancho)

        self.tabla_pedidos.pack(pady=10, fill="x")

        # Cargar inventarios
        self.mostrar_ventas()
        self.mostrar_pedidos()

    # ==================================================
    # CARGAR LISTA DE PRODUCTOS
    # ==================================================
    def obtener_productos(self):
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_producto, nombre FROM productos")
        productos = cursor.fetchall()
        conexion.close()

        return {nombre: pid for pid, nombre in productos}

    # ==================================================
    # FORMULARIOS
    # ==================================================
    def abrir_formulario(self):
        self.venta_seleccionada = None
        self.formulario("Registrar Venta", self.registrar_venta)

    def abrir_formulario_modificar(self):
        if not self.venta_seleccionada:
            messagebox.showwarning("Aviso", "Selecciona una venta primero.")
            return
        
        valores = self.tabla.item(self.venta_seleccionada)["values"]
        self.formulario("Modificar Venta", self.guardar_cambios)

        self.combo_producto.set(valores[1])
        self.entry_cantidad.insert(0, valores[2])

    def formulario(self, titulo, callback):
        self.form = tk.Toplevel(self)
        self.form.title(titulo)
        self.form.geometry("400x350")
        self.form.configure(bg=self.color_fondo)

        tk.Label(self.form, text=titulo, font=("Arial", 16, "bold"),
                 bg=self.color_fondo).pack(pady=15)

        frame = tk.Frame(self.form, bg=self.color_fondo)
        frame.pack(pady=10)

        self.productos_dict = self.obtener_productos()
        lista_productos = list(self.productos_dict.keys())

        # Producto
        tk.Label(frame, text="Producto:", bg=self.color_fondo).grid(row=0, column=0, padx=5, pady=10)
        self.combo_producto = ttk.Combobox(frame, values=lista_productos,
                                           width=25, state="readonly")
        self.combo_producto.grid(row=0, column=1)

        # Cantidad
        tk.Label(frame, text="Cantidad:", bg=self.color_fondo).grid(row=1, column=0, padx=5, pady=10)
        self.entry_cantidad = tk.Entry(frame, width=25)
        self.entry_cantidad.grid(row=1, column=1)

        tk.Button(self.form, text="Guardar", bg=self.color_boton,
                  width=15, command=callback).pack(pady=15)

        tk.Button(self.form, text="Cancelar", bg=self.color_boton,
                  width=15, command=self.form.destroy).pack()

    # ==================================================
    # Registrar venta
    # ==================================================
    def registrar_venta(self):
        self.guardar_en_bd(insert=True)

    # ==================================================
    # Guardar cambios
    # ==================================================
    def guardar_cambios(self):
        self.guardar_en_bd(insert=False)

    # ==================================================
    # GUARDAR BD (con creado_por y actualizado_por)
    # ==================================================
    def guardar_en_bd(self, insert=True):
        nombre_producto = self.combo_producto.get()
        cantidad = self.entry_cantidad.get()

        if not nombre_producto or not cantidad:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser numérica mayor a 0.")
            return

        id_producto = self.productos_dict[nombre_producto]

        conexion = crear_conexion()
        cursor = conexion.cursor()

        # Precio
        cursor.execute("SELECT precio FROM productos WHERE id_producto=%s", (id_producto,))
        precio = cursor.fetchone()[0]
        total = float(precio) * int(cantidad)

        try:
            if insert:
                cursor.execute("""
                    INSERT INTO ventas
                    (fecha, id_producto, nombre_producto, cantidad, total,
                     creado_por, actualizado_por)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    datetime.now(), id_producto, nombre_producto,
                    cantidad, total, self.usuario_actual, self.usuario_actual
                ))
            else:
                id_venta = self.tabla.item(self.venta_seleccionada)["values"][0]
                cursor.execute("""
                    UPDATE ventas
                    SET id_producto=%s, nombre_producto=%s,
                        cantidad=%s, total=%s, actualizado_por=%s
                    WHERE id_venta=%s
                """, (
                    id_producto, nombre_producto, cantidad,
                    total, self.usuario_actual, id_venta
                ))

            conexion.commit()
            messagebox.showinfo("Éxito", "Venta guardada correctamente.")
            self.form.destroy()
            self.mostrar_ventas()

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            conexion.close()

    # ==================================================
    # Mostrar ventas
    # ==================================================
    def mostrar_ventas(self):
        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id_venta, nombre_producto, cantidad,
                   DATE_FORMAT(fecha, '%d-%m-%Y'), total,
                   creado_por, actualizado_por
            FROM ventas
            ORDER BY id_venta DESC
        """)

        registros = cursor.fetchall()
        conexion.close()

        self.tabla.delete(*self.tabla.get_children())

        for fila in registros:
            self.tabla.insert("", tk.END, values=fila)

    # ==================================================
    # Mostrar pedidos
    # ==================================================
    def mostrar_pedidos(self):
        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id_pedido, nombre_producto, cliente, cantidad,
                   DATE_FORMAT(fecha_entrega, '%d-%m-%Y'), estado
            FROM pedidos
            ORDER BY id_pedido DESC
        """)

        pedidos = cursor.fetchall()
        conexion.close()

        self.tabla_pedidos.delete(*self.tabla_pedidos.get_children())

        for fila in pedidos:
            self.tabla_pedidos.insert("", tk.END, values=fila)

    # ==================================================
    # Seleccionar fila
    # ==================================================
    def detectar_fila(self, event):
        self.venta_seleccionada = self.tabla.focus()

    # ==================================================
    # Eliminar venta
    # ==================================================
    def eliminar_venta(self):
        if not self.venta_seleccionada:
            messagebox.showwarning("Aviso", "Selecciona una venta primero.")
            return

        id_venta = self.tabla.item(self.venta_seleccionada)["values"][0]

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM ventas WHERE id_venta=%s", (id_venta,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Eliminado", "Venta eliminada correctamente.")
        self.mostrar_ventas()
