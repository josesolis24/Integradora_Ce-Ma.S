import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion
from datetime import datetime

class ComprasGUI(tk.Toplevel):
    def __init__(self, menu_principal):
        super().__init__(menu_principal)
        self.menu_principal = menu_principal
        self.title("Gestión de Compras")
      
        try:
             self.state('zoomed') 
        except tk.TclError:
             self.attributes('-fullscreen', True) 
        if self.attributes('-fullscreen'):
            self.bind('<Escape>', lambda e: self.attributes('-fullscreen', False))
            
        self.config(bg="#FADADD")

        self.compra_seleccionada = None
   
        tk.Label(
            self,
            text="Módulo de Compras",
            font=("Arial", 18, "bold"),
            bg="#FADADD",
            fg="black"
        ).pack(pady=15)

        # --- Botones principales ---
        frame_btn = tk.Frame(self, bg="#FADADD")
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Registrar Compra", width=18, bg="white",
                  command=self.abrir_formulario).grid(row=0, column=0, padx=8)
        tk.Button(frame_btn, text="Modificar", width=18, bg="white",
                  command=self.abrir_formulario_editar).grid(row=0, column=1, padx=8)
        tk.Button(frame_btn, text="Eliminar", width=18, bg="white",
                  command=self.eliminar_compra).grid(row=0, column=2, padx=8)
        tk.Button(frame_btn, text="Volver", width=18, bg="white",
                  command=self.volver_al_menu).grid(row=0, column=3, padx=8)

        # --- Tabla (Se agregó Categoría como tercera columna) ---
        self.tabla = ttk.Treeview(
            self,
            columns=("ID", "Producto", "Categoría", "Cantidad", "Proveedor", "Total", "Fecha"),
            show="headings"
        )

        # Configuración de columnas
        self.tabla.heading("ID", text="ID"); self.tabla.column("ID", width=50)
        self.tabla.heading("Producto", text="Producto"); self.tabla.column("Producto", width=180)
        self.tabla.heading("Categoría", text="Categoría"); self.tabla.column("Categoría", width=120)
        self.tabla.heading("Cantidad", text="Cantidad"); self.tabla.column("Cantidad", width=70)
        self.tabla.heading("Proveedor", text="Proveedor"); self.tabla.column("Proveedor", width=120)
        self.tabla.heading("Total", text="Total"); self.tabla.column("Total", width=90)
        self.tabla.heading("Fecha", text="Fecha"); self.tabla.column("Fecha", width=100)

        self.tabla.pack(pady=10, fill="both", expand=True)
        self.tabla.bind("<Double-1>", self.sel_fila)

        # --- Diccionarios de datos ---
        self.productos_dict = self.obtener_productos()
        self.proveedores_dict = self.obtener_proveedores()
        self.categorias_dict = self.obtener_categorias() # Carga de Categorías

        self.mostrar_compras()

    # =============================
    # CARGAR DATOS (BD)
    # =============================
    def obtener_productos(self):
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_producto, nombre FROM productos")
        productos = cursor.fetchall()
        conn.close()
        return {nombre: pid for pid, nombre in productos}

    def obtener_proveedores(self):
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_proveedor, nombre FROM proveedores")
        proveedores = cursor.fetchall()
        conn.close()
        return {nombre: pid for pid, nombre in proveedores}

    # NUEVA FUNCIÓN: Obtener categorías
    def obtener_categorias(self):
        conn = crear_conexion()
        cursor = conn.cursor()
        try:
            # Asegúrate que tu tabla se llame 'categorias' y tenga 'id_categoria' y 'nombre'
            cursor.execute("SELECT id_categoria, nombre FROM categorias") 
            categorias = cursor.fetchall()
        except Exception as e:
            categorias = []
            messagebox.showerror("Error de BD", f"No se pudo cargar la tabla de categorías. Revise la tabla 'categorias'. Error: {e}")
        finally:
            conn.close()
        return {nombre: cid for cid, nombre in categorias}

    # =============================
    # SELECCIONAR FILA
    # =============================
    def sel_fila(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            self.compra_seleccionada = self.tabla.item(seleccion[0])["values"][0]

    # =============================
    # FORMULARIO NUEVA COMPRA / MODIFICAR
    # =============================
    def abrir_formulario(self, editar=False):
        self.form = tk.Toplevel(self)
        self.form.title("Registrar Compra" if not editar else "Modificar Compra")
        self.form.geometry("400x400")
        self.form.config(bg="#FFE4EC")
        self.form.transient(self)
        self.form.grab_set()

        frame = tk.Frame(self.form, bg="#FFE4EC")
        frame.pack(pady=10)

        # 1. Producto (Fila 0)
        tk.Label(frame, text="Producto:", bg="#FFE4EC").grid(row=0, column=0, padx=5, pady=5)
        self.combo_producto = ttk.Combobox(frame, values=list(self.productos_dict.keys()), width=25, state="readonly")
        self.combo_producto.grid(row=0, column=1)

        # 2. Categoría (Fila 1)
        tk.Label(frame, text="Categoría:", bg="#FFE4EC").grid(row=1, column=0, padx=5, pady=5)
        self.combo_categoria = ttk.Combobox(frame, values=list(self.categorias_dict.keys()), width=25, state="readonly")
        self.combo_categoria.grid(row=1, column=1)

        # 3. Cantidad (Fila 2)
        tk.Label(frame, text="Cantidad:", bg="#FFE4EC").grid(row=2, column=0, padx=5, pady=5)
        self.entry_cantidad = tk.Entry(frame, width=25)
        self.entry_cantidad.grid(row=2, column=1)

        # 4. Proveedor (Fila 3)
        tk.Label(frame, text="Proveedor:", bg="#FFE4EC").grid(row=3, column=0, padx=5, pady=5)
        lista_proveedores = list(self.proveedores_dict.keys())
        self.combo_proveedor = ttk.Combobox(frame, values=lista_proveedores, width=25)
        self.combo_proveedor.grid(row=3, column=1)

        # Lógica de carga para edición
        if editar and self.compra_seleccionada:
            conn = crear_conexion()
            cursor = conn.cursor()
            # Se selecciona id_categoria
            cursor.execute("""
                SELECT id_producto, cantidad, id_proveedor, id_categoria 
                FROM compras WHERE id_compra=%s
            """, (self.compra_seleccionada,))
            datos = cursor.fetchone()
            conn.close()

            if datos:
                # Set producto
                for nombre, pid in self.productos_dict.items():
                    if pid == datos[0]:
                        self.combo_producto.set(nombre)
                        break
                
                # Set cantidad
                self.entry_cantidad.insert(0, datos[1])

                # Set proveedor
                if datos[2]:
                    for nombre, pid in self.proveedores_dict.items():
                        if pid == datos[2]:
                            self.combo_proveedor.set(nombre)
                            break
                
                # Set categoría
                if datos[3]:
                    for nombre, cid in self.categorias_dict.items():
                        if cid == datos[3]:
                            self.combo_categoria.set(nombre)
                            break

        tk.Button(self.form, text="Guardar", bg="white", width=15,
                  command=lambda: self.guardar(editar)).pack(pady=15)

    def abrir_formulario_editar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una fila primero.")
            return
        self.compra_seleccionada = self.tabla.item(seleccion[0])["values"][0]
        self.abrir_formulario(editar=True)

    # =============================
    # GUARDAR COMPRA
    # =============================
    def guardar(self, editar=False):
        nombre_producto = self.combo_producto.get()
        nombre_categoria = self.combo_categoria.get()
        cantidad = self.entry_cantidad.get().strip()
        nombre_proveedor = self.combo_proveedor.get().strip()

        if not nombre_producto or not cantidad:
            messagebox.showerror("Error", "Producto y cantidad obligatorios.")
            return

        try:
            cantidad = float(cantidad)
        except:
            messagebox.showerror("Error", "La cantidad debe ser numérica.")
            return

        # Obtener IDs, usando .get() para evitar KeyError si el diccionario está vacío
        id_producto = self.productos_dict.get(nombre_producto)
        id_categoria = self.categorias_dict.get(nombre_categoria)
        id_proveedor = self.proveedores_dict.get(nombre_proveedor)
        
        if id_producto is None:
             messagebox.showerror("Error", "El producto seleccionado no es válido.")
             return

        conn = crear_conexion()
        cursor = conn.cursor()

        # Obtener precio del producto
        cursor.execute("SELECT precio FROM productos WHERE id_producto=%s", (id_producto,))
        res = cursor.fetchone()
        precio = float(res[0]) if res else 0.0
        
        total = cantidad * precio
        fecha = datetime.now().strftime("%Y-%m-%d")

        try:
            if editar:
                cursor.execute("""
                    UPDATE compras
                    SET id_producto=%s, nombre_producto=%s,
                        id_proveedor=%s, proveedor_nombre=%s,
                        id_categoria=%s, nombre_categoria=%s,
                        cantidad=%s, total=%s
                    WHERE id_compra=%s
                """, (id_producto, nombre_producto,
                      id_proveedor, nombre_proveedor or 'N/A',
                      id_categoria, nombre_categoria or 'N/A',
                      cantidad, total, self.compra_seleccionada))
            else:
                cursor.execute("""
                    INSERT INTO compras (fecha, id_producto, nombre_producto,
                                         id_proveedor, proveedor_nombre,
                                         id_categoria, nombre_categoria,
                                         cantidad, total)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (fecha, id_producto, nombre_producto,
                      id_proveedor, nombre_proveedor or 'N/A',
                      id_categoria, nombre_categoria or 'N/A',
                      cantidad, total))

            conn.commit()
            messagebox.showinfo("Éxito", "Compra guardada correctamente.")
            self.form.destroy()
            self.mostrar_compras()

        except Exception as e:
            messagebox.showerror("Error de base de datos", f"Verifique su conexión o las columnas en la tabla 'compras'. Error: {e}")
        finally:
            conn.close()

    # =============================
    # MOSTRAR COMPRAS EN TABLA (Se ajustó la consulta para incluir Categoría)
    # =============================
    def mostrar_compras(self):
        self.tabla.delete(*self.tabla.get_children())
        conn = crear_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_compra, nombre_producto, 
                   IFNULL(nombre_categoria, 'N/A'), 
                   cantidad,
                   IFNULL(proveedor_nombre,'N/A'), 
                   total,
                   DATE_FORMAT(fecha,'%d-%m-%Y')
            FROM compras
            ORDER BY id_compra DESC
        """)
        
        for row in cursor.fetchall():
            # Los valores de 'row' coinciden con las 7 columnas definidas en __init__
            self.tabla.insert("", "end", values=row)

        cursor.close()
        conn.close()

    # =============================
    # ELIMINAR COMPRA
    # =============================
    def eliminar_compra(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una compra.")
            return

        id_compra = self.tabla.item(seleccion[0])["values"][0]

        if not messagebox.askyesno("Confirmar", "¿Desea eliminar esta compra?"):
            return

        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM compras WHERE id_compra=%s", (id_compra,))
        conn.commit()
        cursor.close()
        conn.close()

        self.mostrar_compras()
        messagebox.showinfo("Éxito", "Compra eliminada.")

    def volver_al_menu(self):
        self.destroy()
        self.menu_principal.deiconify()