import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion 

# ------------------------
# Helper: normalizar usuario a cadena segura
# ------------------------
def normalizar_usuario_raw(valor):
    """
    Devuelve string representando el usuario para guardar en DB.
    Si viene None/empty/NULL -> devuelve 'Desconocido'
    """
    if valor is None:
        return "Desconocido"
    try:
        s = str(valor).strip()
        if s == "" or s.lower() in ("none", "null"):
            return "Desconocido"
        return s
    except Exception:
        return "Desconocido"


class CategoriasFrame(tk.Frame):
    def __init__(self, parent, master_notebook):
        super().__init__(parent, bg="#FADADD")
        self.master_notebook = master_notebook
        self.categoria_seleccionada = None
        self.form = None
        self.crear_gui()
        self.cargar_categorias()

    def crear_gui(self):
        tk.Label(self, text="Gestión de Categorías",
                 font=("Arial", 16, "bold"),
                 bg="#FADADD").pack(pady=10)

        frame_btn = tk.Frame(self, bg="#FADADD")
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Registrar Categoría", width=18, bg="white",
                  command=self.abrir_formulario).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Editar", width=18, bg="white",
                  command=self.abrir_edicion).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Eliminar", width=18, bg="white",
                  command=self.eliminar_categoria).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Regresar al Menú", width=18, bg="white",
                  command=self.master_notebook.master.destroy).grid(row=0, column=3, padx=5)

        self.tabla = ttk.Treeview(self, columns=("id", "nombre", "creado_por", "actualizado_por"), show="headings")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("creado_por", text="Creado por")
        self.tabla.heading("actualizado_por", text="Actualizado por")

        self.tabla.column("id", width=60)
        self.tabla.column("nombre", width=200)
        self.tabla.column("creado_por", width=120)
        self.tabla.column("actualizado_por", width=120)

        self.tabla.pack(pady=10, fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.on_categoria_select)

    def on_categoria_select(self, event):
        pass

    def abrir_formulario(self, editar=False):
        if self.form and self.form.winfo_exists():
            self.form.lift()
            return

        self.form = tk.Toplevel(self.master_notebook.master)
        self.form.title("Registrar Categoría" if not editar else "Editar Categoría")
        self.form.geometry("400x200")
        self.form.config(bg="#FFE4EC")
        self.form.transient(self.master_notebook.master)
        self.form.grab_set()

        tk.Label(self.form, text="Nombre de categoría:", bg="#FFE4EC").pack(pady=10)
        self.entry_form = tk.Entry(self.form, width=40)
        self.entry_form.pack(pady=5)

        if editar and self.categoria_seleccionada:
            try:
                conn = crear_conexion()
                cursor = conn.cursor()
                cursor.execute("SELECT nombre FROM categorias WHERE id_categoria=%s", (self.categoria_seleccionada,))
                nombre = cursor.fetchone()
                cursor.close()
                conn.close()
                if nombre:
                    self.entry_form.insert(0, nombre[0])
            except Exception as e:
                messagebox.showerror("Error de Carga", f"No se pudo cargar la categoría: {e}")

        tk.Button(self.form, text="Guardar", bg="white", width=15,
                  command=lambda: self.guardar(editar)).pack(pady=15)

    def abrir_edicion(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una categoría.")
            return
        self.categoria_seleccionada = self.tabla.item(seleccion[0])["values"][0]
        self.abrir_formulario(editar=True)

    def guardar(self, editar=False):
        nombre = self.entry_form.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return

        # Obtener usuario desde ProductosGUI (notebook)
        usuario_raw = getattr(self.master_notebook, 'usuario_actual', None)
        usuario = normalizar_usuario_raw(usuario_raw)

        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            if editar:
                cursor.execute("UPDATE categorias SET nombre=%s, actualizado_por=%s WHERE id_categoria=%s",
                               (nombre, usuario, self.categoria_seleccionada))
            else:
                cursor.execute("INSERT INTO categorias (nombre, creado_por, actualizado_por) VALUES (%s, %s, %s)",
                               (nombre, usuario, usuario))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Categoría guardada correctamente.")
            self.cargar_categorias()
            # llamar recargar_comboboxes solo si existe y es seguro (master_notebook es ProductosGUI)
            if hasattr(self.master_notebook, 'recargar_comboboxes'):
                try:
                    self.master_notebook.recargar_comboboxes()
                except Exception:
                    # Si por alguna razón el notebook o combobox fue destruido, no hacer nada
                    pass
        except Exception as e:
            messagebox.showerror("ERROR BD", str(e))
        finally:
            if hasattr(self, 'form') and self.form and self.form.winfo_exists():
                self.form.destroy()

    def cargar_categorias(self):
        self.tabla.delete(*self.tabla.get_children())
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_categoria, nombre, creado_por, actualizado_por FROM categorias ORDER BY id_categoria ASC")
            filas = cursor.fetchall()
            cursor.close()
            conn.close()

            for fila in filas:
                idc, nombre, creado_por, actualizado_por = fila
                creado_por_disp = creado_por if (creado_por is not None and str(creado_por).strip().lower() not in ("", "none", "null")) else "Desconocido"
                actualizado_por_disp = actualizado_por if (actualizado_por is not None and str(actualizado_por).strip().lower() not in ("", "none", "null")) else ""
                self.tabla.insert("", "end", values=(idc, nombre, creado_por_disp, actualizado_por_disp))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar categorías: {e}")

    def eliminar_categoria(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una categoría.")
            return
        categoria_id = self.tabla.item(seleccion[0])["values"][0]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la categoría {categoria_id}?"):
            return
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categorias WHERE id_categoria=%s", (categoria_id,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Categoría eliminada.")
            self.cargar_categorias()
            if hasattr(self.master_notebook, 'recargar_comboboxes'):
                try:
                    self.master_notebook.recargar_comboboxes()
                except Exception:
                    pass
        except Exception as e:
            messagebox.showerror("Error", str(e))


class ProductosGUI:
    def __init__(self, master=None, usuario_actual=None):
        self.master = tk.Toplevel(master) if master else tk.Tk()
        self.master.title("Gestión: Productos y Categorías")

        self.master.state('zoomed')
        self.master.geometry("1500x550")

        self.producto_seleccionado = None
        self.color_fondo = "#F8C8DC"
        self.color_boton = "#FFFFFF"

        # usuario_actual viene como username (string) desde el login/menu
        self.usuario_actual = normalizar_usuario_raw(usuario_actual)
        self.form = None

        frame = tk.Frame(self.master, bg=self.color_fondo)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Inventario Ce&Ma — Usuario: {self.usuario_actual}",
                 font=("Arial", 24, "bold"), bg=self.color_fondo).pack(pady=10)

        self.notebook = ttk.Notebook(frame)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.frame_productos = tk.Frame(self.notebook, bg=self.color_fondo)
        self.notebook.add(self.frame_productos, text="📦 Productos")
        self.crear_gui_productos(self.frame_productos)

        # Aseguramos que los combos estén cargados al abrir la pestaña
        # (esto evita guardados con id_categoria/id_proveedor vacíos cuando entra un empleado)
        # NOTA: estas funciones ahora comprueban existencia de widgets internamente
        self.cargar_categorias()
        self.cargar_proveedores()

        self.frame_categorias = CategoriasFrame(self.notebook, self)
        self.notebook.add(self.frame_categorias, text="🏷️ Categorías")

    def recargar_comboboxes(self):
        """
        Actualiza comboboxes sólo si existen y están vivos.
        Evita el error 'invalid command name ... combobox' si el formulario fue cerrado.
        """
        # categoria_combo puede existir solo dentro de un formulario (self.form)
        if hasattr(self, 'categoria_combo') and getattr(self, 'categoria_combo') is not None:
            try:
                if self.categoria_combo.winfo_exists():
                    self.cargar_categorias()
            except Exception:
                pass

        if hasattr(self, 'proveedor_combo') and getattr(self, 'proveedor_combo') is not None:
            try:
                if self.proveedor_combo.winfo_exists():
                    self.cargar_proveedores()
            except Exception:
                pass

    def crear_gui_productos(self, frame):
        frame_btn = tk.Frame(frame, bg=self.color_fondo)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Registrar Producto", width=18,
                  bg=self.color_boton, fg="black",
                  command=self.abrir_formulario).grid(row=0, column=0, padx=5)

        tk.Button(frame_btn, text="Editar", width=18,
                  bg=self.color_boton, fg="black",
                  command=self.abrir_formulario_editar).grid(row=0, column=1, padx=5)

        tk.Button(frame_btn, text="Eliminar", width=18,
                  bg=self.color_boton, fg="black",
                  command=self.eliminar_producto).grid(row=0, column=2, padx=5)

        tk.Button(frame_btn, text="Regresar al Menú", width=18,
                  bg=self.color_boton, fg="black",
                  command=self.master.destroy).grid(row=0, column=3, padx=5)

        # ---------- Treeview + scrollbar ----------
        self.tabla = ttk.Treeview(frame, columns=("id", "nombre", "descripcion", "precio", "stock",
                                                 "categoria", "proveedor", "creado_por", "actualizado_por"),
                                  show="headings")

        # scrollbar vertical
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")

        for col, head, width in [
            ("id", "ID", 50), ("nombre", "Nombre", 150), ("descripcion", "Descripción", 250),
            ("precio", "Precio", 80), ("stock", "Stock", 60), ("categoria", "Categoría", 120),
            ("proveedor", "Proveedor", 120), ("creado_por", "Creado por", 120), ("actualizado_por", "Actualizado por", 120)
        ]:
            self.tabla.heading(col, text=head)
            self.tabla.column(col, width=width)

        # importante: rellenar ambos e permitir expandirse para que no se oculten filas/columnas
        self.tabla.pack(pady=10, fill="both", expand=True)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        # ------------------------------------------

        # Cargar tabla (al final de la creación de GUI)
        self.cargar_tabla()

    def _check_form_status(self):
        if self.form and self.form.winfo_exists():
            self.form.lift()
            return True
        return False

    def abrir_formulario(self):
        if self._check_form_status(): return
        self.producto_seleccionado = None
        self.crear_formulario(titulo="Registrar Producto", callback=self.agregar_producto)

    def abrir_formulario_editar(self):
        if self._check_form_status(): return
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto para editar.")
            return
        self.producto_seleccionado = seleccion[0]
        producto_id = self.tabla.item(self.producto_seleccionado)["values"][0]

        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            # USAR LEFT JOIN aquí también para recuperar productos aunque falte categoría/proveedor
            cursor.execute("""
                SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock,
                       c.nombre, pr.nombre
                FROM productos p
                LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
                LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
                WHERE p.id_producto = %s
            """, (producto_id,))
            initial_data = cursor.fetchone()
            cursor.close()
            conn.close()

            if initial_data:
                self.crear_formulario(titulo="Editar Producto", callback=self.guardar_cambios, initial_data=initial_data)
            else:
                messagebox.showerror("Error", "No se pudo recuperar los datos del producto.")
        except Exception as e:
            messagebox.showerror("Error BD", f"Error al cargar datos para edición: {e}")

    def crear_formulario(self, titulo, callback, initial_data=None):
        self.form = tk.Toplevel(self.master)
        self.form.title(titulo)
        self.form.geometry("500x350")
        self.form.config(bg=self.color_fondo)
        form_frame = tk.Frame(self.form, padx=10, pady=10, bg=self.color_fondo)
        form_frame.pack()

        self.nombre_entry = self.crear_label_entry(form_frame, "Nombre:", 0)
        self.descripcion_entry = self.crear_label_entry(form_frame, "Descripción:", 1)
        self.precio_entry = self.crear_label_entry(form_frame, "Precio:", 2)
        self.stock_entry = self.crear_label_entry(form_frame, "Stock:", 3)

        tk.Label(form_frame, text="Categoría:", bg=self.color_fondo).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.categoria_combo = ttk.Combobox(form_frame, state="readonly", width=37)
        self.categoria_combo.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Proveedor:", bg=self.color_fondo).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.proveedor_combo = ttk.Combobox(form_frame, state="readonly", width=37)
        self.proveedor_combo.grid(row=5, column=1, padx=10, pady=10)

        # cargar los valores en combos (asegura que estén disponibles)
        # las funciones comprobarán si el widget existe antes de asignar valores
        self.cargar_categorias()
        self.cargar_proveedores()

        if initial_data:
            # initial_data = (id_producto, nombre, descripcion, precio, stock, categoria_nombre, proveedor_nombre)
            self.nombre_entry.insert(0, initial_data[1])
            self.descripcion_entry.insert(0, initial_data[2])
            self.precio_entry.insert(0, initial_data[3])
            self.stock_entry.insert(0, initial_data[4])
            if initial_data[5] is not None:
                self.categoria_combo.set(initial_data[5])
            else:
                self.categoria_combo.set("")
            if initial_data[6] is not None:
                self.proveedor_combo.set(initial_data[6])
            else:
                self.proveedor_combo.set("")

        tk.Button(self.form, text="Guardar", width=15, bg=self.color_boton, command=callback).pack(pady=15)
        tk.Button(self.form, text="Cancelar", width=15, bg=self.color_boton, command=self.form.destroy).pack()

    def crear_label_entry(self, parent, texto, fila):
        tk.Label(parent, text=texto, bg=self.color_fondo).grid(row=fila, column=0, padx=10, pady=10, sticky="w")
        entry = tk.Entry(parent, width=40)
        entry.grid(row=fila, column=1, padx=10, pady=10)
        return entry

    def cargar_categorias(self):
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_categoria, nombre FROM categorias")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            # guardamos el dict siempre
            self.categorias = {nombre: id_ for id_, nombre in datos}
            # solo intentamos asignar valores si el combobox existe y sigue vivo
            if hasattr(self, 'categoria_combo') and self.categoria_combo is not None:
                try:
                    if self.categoria_combo.winfo_exists():
                        self.categoria_combo["values"] = list(self.categorias.keys())
                except Exception:
                    # si dio problema (widget destruido), lo ignoramos
                    pass
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar categorías: {e}")

    def cargar_proveedores(self):
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_proveedor, nombre FROM proveedores")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            self.proveedores = {nombre: id_ for id_, nombre in datos}
            if hasattr(self, 'proveedor_combo') and self.proveedor_combo is not None:
                try:
                    if self.proveedor_combo.winfo_exists():
                        self.proveedor_combo["values"] = list(self.proveedores.keys())
                except Exception:
                    pass
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar proveedores: {e}")

    def agregar_producto(self):
        self.guardar_en_bd(insert=True)

    def guardar_cambios(self):
        self.guardar_en_bd(insert=False)

    def guardar_en_bd(self, insert=True):
        try:
            nombre = self.nombre_entry.get()
            descripcion = self.descripcion_entry.get()
            precio = float(self.precio_entry.get())
            stock = int(self.stock_entry.get())
            categoria_nombre = self.categoria_combo.get()
            proveedor_nombre = self.proveedor_combo.get()

            id_categoria = self.categorias.get(categoria_nombre)
            id_proveedor = self.proveedores.get(proveedor_nombre)

            if not id_categoria or not id_proveedor:
                messagebox.showwarning("Advertencia", "Debes seleccionar categoría y proveedor válidos.")
                return

            conn = crear_conexion()
            cursor = conn.cursor()

            usuario = normalizar_usuario_raw(self.usuario_actual)

            if insert:
                cursor.execute("""
                    INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, id_proveedor, creado_por, actualizado_por)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (nombre, descripcion, precio, stock, id_categoria, id_proveedor, usuario, usuario))
            else:
                producto_id = self.tabla.item(self.producto_seleccionado)["values"][0]
                cursor.execute("""
                    UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s, 
                    id_categoria=%s, id_proveedor=%s, actualizado_por=%s 
                    WHERE id_producto=%s
                """, (nombre, descripcion, precio, stock, id_categoria, id_proveedor, usuario, producto_id))

            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Producto guardado correctamente")
            if self.form and self.form.winfo_exists():
                self.form.destroy()
            self.cargar_tabla()
        except ValueError:
            messagebox.showerror("Error de Formato", "El precio y el stock deben ser números válidos.")
        except Exception as e:
            messagebox.showerror("Error de Guardado", str(e))

    def eliminar_producto(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return
        producto_id = self.tabla.item(seleccion[0])["values"][0]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el producto {producto_id}?"):
            return
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id_producto=%s", (producto_id,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Producto eliminado.")
            self.cargar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def cargar_tabla(self):
        try:
            conn = crear_conexion()
            cursor = conn.cursor()

            # 🔥 CORREGIDO — LEFT JOIN (solución al problema)
            cursor.execute("""
                SELECT 
                       p.id_producto, p.nombre, p.descripcion, p.precio, p.stock,
                       c.nombre AS categoria_nombre, pr.nombre AS proveedor_nombre, 
                       p.creado_por, p.actualizado_por
                FROM productos p
                LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
                LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
                ORDER BY p.id_producto ASC
            """)

            registros = cursor.fetchall()
            cursor.close()
            conn.close()

            self.tabla.delete(*self.tabla.get_children())
            for fila in registros:
                idp, nom, desc, precio, stock, cat, prov, creado_por, actualizado_por = fila
                creado_disp = creado_por if (creado_por is not None and str(creado_por).strip().lower() not in ("", "none", "null")) else "Desconocido"
                actualizado_disp = actualizado_por if (actualizado_por is not None and str(actualizado_por).strip().lower() not in ("", "none", "null")) else ""
                self.tabla.insert("", tk.END, values=(idp, nom, desc, precio, stock, cat, prov, creado_disp, actualizado_disp))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar productos: {e}")

    def seleccionar_fila(self, event):
        self.producto_seleccionado = self.tabla.focus()
