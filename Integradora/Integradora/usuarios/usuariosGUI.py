import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion


class UsuariosGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Usuarios")
        self.geometry("700x500")

        ttk.Label(self, text="Módulo de Usuarios", font=("Arial", 16, "bold")).pack(pady=10)

       
# ----------- Botones -----------
        frame_btn = tk.Frame(self, bg="#f0f0f0")
        frame_btn.pack(pady=10)

        btn_avanzado = tk.Button(frame_btn, text="Registro de Usuario", width=18,
                         bg="#d6e0ff", fg="black", font=("Arial", 10, "bold"),
                         command=self.abrir_registro_avanzado)
        btn_avanzado.grid(row=0, column=1, padx=8, pady=5)

        btn_eliminar = tk.Button(frame_btn, text="Eliminar usuario", width=18,
                         bg="#ffb4b4", fg="black", font=("Arial", 10, "bold"),
                         command=self.eliminar_usuario)
        btn_eliminar.grid(row=0, column=2, padx=8, pady=5)

        btn_regresar = tk.Button(frame_btn, text="Regresar al menú", width=18,
                         bg="#ffe8a6", fg="black", font=("Arial", 10, "bold"),
                         command=self.destroy)
        btn_regresar.grid(row=0, column=3, padx=8, pady=5)

        # ----------- Tabla ----------- 
        self.tabla = ttk.Treeview(self, columns=("id", "username", "rol"), show="headings")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("username", text="Nombre de Usuario")
        self.tabla.heading("rol", text="Rol")

        self.tabla.column("id", width=50)
        self.tabla.column("username", width=200)
        self.tabla.column("rol", width=200)

        self.tabla.pack(pady=10, fill="both", expand=True)

        self.cargar_usuarios()

    # =============================================================
    # 👉👉 VENTANA NUEVA DE REGISTRO AVANZADO
    # =============================================================
    def abrir_registro_avanzado(self):
        ventana = tk.Toplevel(self)
        ventana.title("Registro Avanzado de Usuario")
        ventana.geometry("450x400")

        tk.Label(ventana, text="Registro Avanzado de Usuario",
                 font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(ventana)
        frame.pack(pady=10)

        tk.Label(frame, text="Nombre de usuario:").grid(row=0, column=0, pady=5)
        entry_user = tk.Entry(frame, width=30)
        entry_user.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Contraseña:").grid(row=1, column=0, pady=5)
        entry_pass = tk.Entry(frame, width=30, show="*")
        entry_pass.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Rol adicional:").grid(row=2, column=0, pady=5)
        combo = ttk.Combobox(frame, width=28, state="readonly",
                             values=["Administrador General", "Empleado", "Invitado"])
        combo.grid(row=2, column=1, pady=5)
        combo.current(0)

        tk.Button(ventana, text="Guardar", width=15, bg="#b0ffc8",
                  command=lambda: self.guardar_avanzado(
                      ventana, entry_user.get(), entry_pass.get(), combo.get()
                  )).pack(pady=10)

    def guardar_avanzado(self, ventana, usuario, password, rol):
        if not usuario or not password:
            messagebox.showwarning("Error", "Debes llenar todos los campos.")
            return

        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, password, Rol) VALUES (%s, %s, %s)",
                           (usuario, password, rol))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            ventana.destroy()
            self.cargar_usuarios()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    # =============================================================
    def registrar_usuario(self):
        nombre = self.entry_nombre.get().strip()
        contraseña = self.entry_pass.get().strip()
        rol = self.combo_rol.get()

        if not nombre or not contraseña:
            messagebox.showwarning("Error", "Debes llenar todos los campos.")
            return

        conn = None
        cursor = None

        try:
            conn = crear_conexion()
            cursor = conn.cursor()

            cursor.execute("SELECT id_usuario FROM usuarios WHERE username = %s", (nombre,))
            existe = cursor.fetchone()

            if existe:
                messagebox.showerror("Error", "Este nombre de usuario ya está registrado.")
                return

            cursor.execute(
                "INSERT INTO usuarios (username, password, Rol) VALUES (%s, %s, %s)",
                (nombre, contraseña, rol)
            )
            conn.commit()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        self.entry_nombre.delete(0, tk.END)
        self.entry_pass.delete(0, tk.END)
        self.combo_rol.current(0)

        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        self.cargar_usuarios()

    # =============================================================
    def cargar_usuarios(self):
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, username, Rol FROM usuarios")
            filas = cursor.fetchall()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar usuarios: {e}")
            return

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        self.tabla.delete(*self.tabla.get_children())
        for fila in filas:
            self.tabla.insert("", "end", values=fila)

    # =============================================================
    def eliminar_usuario(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un usuario.")
            return

        item = self.tabla.item(seleccion)
        usuario_id = item["values"][0]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar usuario con ID {usuario_id}?"
        )

        if not confirmar:
            return

        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (usuario_id,))
            conn.commit()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
        self.cargar_usuarios()

