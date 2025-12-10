import tkinter as tk
from tkinter import ttk, messagebox
# Asegúrate de que 'conexionBD' sea accesible
try:
    from conexionBD import crear_conexion
except ImportError:
    messagebox.showerror("Error", "No se encontró el módulo 'conexionBD'.")
    # Define una función dummy si no se puede importar para evitar errores fatales,
    # aunque esto debería resolverse en el entorno de ejecución.
    def crear_conexion(): return None


class ProveedoresGUI:
    def __init__(self, master=None, regresar_callback=None):
        self.master = tk.Toplevel(master)
        self.master.title("Gestión de Proveedores")

        # ❌ ELIMINADO: self.master.geometry("1100x520")

        # 🎯 MODIFICACIÓN PARA PANTALLA COMPLETA
        try:
             # Intenta maximizar (zoomed)
             self.master.state('zoomed')
        except tk.TclError:
             # Si falla (ej. en Mac), usa fullscreen y añade un escape
             self.master.attributes('-fullscreen', True)
             self.master.bind('<Escape>', lambda e: self.master.attributes('-fullscreen', False))

        self.regresar_callback = regresar_callback

        rosa_suave = "#FFE4E9"
        blanco = "#FFFFFF"

        self.master.configure(bg=rosa_suave)

        # TÍTULO
        tk.Label(self.master, text="Módulo de Proveedores",
                 font=("Arial", 18, "bold"), bg=rosa_suave).pack(pady=10)

        # ================= BOTONES =================
        frame_btn = tk.Frame(self.master, bg=rosa_suave)
        frame_btn.pack()

        tk.Button(frame_btn, text="Registrar proveedor", bg="#98FB98",
                  width=20, command=self.abrir_formulario_agregar).grid(row=0, column=0, padx=10)

        tk.Button(frame_btn, text="Modificar", bg="#87CEEB",
                  width=20, command=self.abrir_formulario_modificar).grid(row=0, column=1, padx=10)

        tk.Button(frame_btn, text="Eliminar", bg="#FF7F7F",
                  width=20, command=self.eliminar_proveedor).grid(row=0, column=2, padx=10)

        tk.Button(frame_btn, text="Regresar", bg="#D3D3D3",
                  width=20, command=self.regresar).grid(row=0, column=3, padx=10)

        # ================= TABLA =================
        frame_tabla = tk.Frame(self.master, bg=blanco)
        # Usar fill="both" y expand=True para que ocupe todo el espacio de la ventana maximizada
        frame_tabla.pack(expand=True, fill="both", pady=20, padx=10)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Proveedor.Treeview",
                        background=blanco,
                        fieldbackground=blanco)

        style.configure("Proveedor.Treeview.Heading",
                        background="#FFC0CB")

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("id_proveedor", "nombre", "telefono", "direccion", "correo_electronico"),
            show="headings",
            style="Proveedor.Treeview"
        )

        self.tabla.heading("id_proveedor", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("telefono", text="Teléfono")
        self.tabla.heading("direccion", text="Dirección")
        self.tabla.heading("correo_electronico", text="Correo Electrónico")

        # Ajuste de anchos - estos anchos son solo sugerencias, el layout se adaptará.
        self.tabla.column("id_proveedor", width=50, stretch=tk.NO)
        self.tabla.column("nombre", width=150)
        self.tabla.column("telefono", width=100)
        # Distribuir el espacio restante entre Dirección y Correo
        self.tabla.column("direccion", width=250)
        self.tabla.column("correo_electronico", width=200)


        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.mostrar_proveedores()

    # ===========================================================
    # NUEVA VENTANA: AGREGAR PROVEEDOR
    # ===========================================================
    def abrir_formulario_agregar(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Registrar proveedor")
        # Ajuste de tamaño para el nuevo campo
        ventana.geometry("400x350")
        ventana.transient(self.master) # Mantenerla sobre la ventana principal
        ventana.grab_set() # Bloquear la interacción con otras ventanas
        
        tk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack()

        tk.Label(ventana, text="Teléfono:").pack(pady=5)
        entry_telefono = tk.Entry(ventana)
        entry_telefono.pack()

        tk.Label(ventana, text="Dirección:").pack(pady=5)
        entry_direccion = tk.Entry(ventana)
        entry_direccion.pack()
        
        # Nuevo campo para el Correo Electrónico
        tk.Label(ventana, text="Correo Electrónico:").pack(pady=5)
        entry_correo = tk.Entry(ventana)
        entry_correo.pack()

        def guardar():
            nombre = entry_nombre.get().strip()
            telefono = entry_telefono.get().strip()
            direccion = entry_direccion.get().strip()
            correo_electronico = entry_correo.get().strip()

            if not nombre:
                messagebox.showwarning("Campos vacíos", "El nombre es obligatorio.", parent=ventana)
                return

            try:
                cnx = crear_conexion()
                if cnx:
                    cursor = cnx.cursor()
                    
                    # Actualizar el INSERT con el campo 'correo_electronico'
                    cursor.execute("INSERT INTO proveedores (nombre, telefono, direccion, correo_electronico) VALUES (%s, %s, %s, %s)",
                                   (nombre, telefono, direccion, correo_electronico))
                    cnx.commit()
                    messagebox.showinfo("Éxito", "Proveedor agregado correctamente.", parent=ventana)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar:\n{e}", parent=ventana)
            finally:
                try: cursor.close()
                except: pass
                try: cnx.close()
                except: pass

            ventana.destroy()
            self.mostrar_proveedores()

        tk.Button(ventana, text="Guardar", bg="#90EE90", command=guardar).pack(pady=20)
        ventana.wait_window() # Esperar a que se cierre la ventana


    # ===========================================================
    # NUEVA VENTANA: MODIFICAR PROVEEDOR
    # ===========================================================
    def abrir_formulario_modificar(self):
        item = self.tabla.selection()
        if not item:
            messagebox.showwarning("Error", "Selecciona un proveedor.")
            return

        fila = self.tabla.item(item)["values"]
        id_proveedor = fila[0]

        ventana = tk.Toplevel(self.master)
        ventana.title("Modificar proveedor")
        # Ajuste de tamaño para el nuevo campo
        ventana.geometry("400x350")
        ventana.transient(self.master)
        ventana.grab_set()

        tk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.insert(0, fila[1])
        entry_nombre.pack()

        tk.Label(ventana, text="Teléfono:").pack(pady=5)
        entry_telefono = tk.Entry(ventana)
        entry_telefono.insert(0, fila[2])
        entry_telefono.pack()

        tk.Label(ventana, text="Dirección:").pack(pady=5)
        entry_direccion = tk.Entry(ventana)
        entry_direccion.insert(0, fila[3])
        entry_direccion.pack()
        
        # Nuevo campo para el Correo Electrónico
        tk.Label(ventana, text="Correo Electrónico:").pack(pady=5)
        entry_correo = tk.Entry(ventana)
        # Rellenar con el valor actual (fila[4])
        entry_correo.insert(0, fila[4]) 
        entry_correo.pack()


        def modificar():
            nombre = entry_nombre.get()
            telefono = entry_telefono.get()
            direccion = entry_direccion.get()
            correo_electronico = entry_correo.get()
            
            try:
                cnx = crear_conexion()
                if cnx:
                    cursor = cnx.cursor()
                    
                    # Actualizar el UPDATE con el nuevo campo 'correo_electronico'
                    cursor.execute("""
                        UPDATE proveedores SET nombre=%s, telefono=%s, direccion=%s, correo_electronico=%s WHERE id_proveedor=%s
                    """, (nombre, telefono, direccion, correo_electronico, id_proveedor))
                    
                    cnx.commit()
                    messagebox.showinfo("Éxito", "Proveedor modificado correctamente.", parent=ventana)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar:\n{e}", parent=ventana)
            finally:
                try: cursor.close()
                except: pass
                try: cnx.close()
                except: pass

            ventana.destroy()
            self.mostrar_proveedores()

        tk.Button(ventana, text="Guardar cambios", bg="#87CEEB", command=modificar).pack(pady=20)
        ventana.wait_window()

    # ===========================================================
    # ELIMINAR (Sin cambios)
    # ===========================================================
    def eliminar_proveedor(self):
        item = self.tabla.selection()
        if not item:
            messagebox.showwarning("Error", "Selecciona un proveedor.")
            return

        id_proveedor = self.tabla.item(item)["values"][0]

        # Reemplazado askyesno por showwarning para usar un diálogo simple
        if not messagebox.askyesno("Confirmar", f"¿Eliminar proveedor ID {id_proveedor}?"):
            return

        try:
            cnx = crear_conexion()
            if cnx:
                cursor = cnx.cursor()
                cursor.execute("DELETE FROM proveedores WHERE id_proveedor=%s", (id_proveedor,))
                cnx.commit()
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
        finally:
            try: cursor.close()
            except: pass
            try: cnx.close()
            except: pass

        self.mostrar_proveedores()

    def mostrar_proveedores(self):
        self.tabla.delete(*self.tabla.get_children())

        try:
            cnx = crear_conexion()
            if cnx:
                cursor = cnx.cursor()
                # Incluir 'correo_electronico' en el SELECT
                cursor.execute("SELECT id_proveedor, nombre, telefono, direccion, correo_electronico FROM proveedores")
                datos = cursor.fetchall()
            else:
                 datos = []
        except Exception as e:
            messagebox.showerror("Error BD", f"Error al cargar proveedores: {e}")
            datos = []
        finally:
            try: cursor.close()
            except: pass
            try: cnx.close()
            except: pass

        for fila in datos:
            self.tabla.insert("", "end", values=fila)

    def regresar(self):
        if self.regresar_callback:
            self.regresar_callback()
        self.master.destroy()