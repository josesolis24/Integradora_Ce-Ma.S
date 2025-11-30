import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion


class UsuariosGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Usuarios")
        self.geometry("700x500")

        ttk.Label(self, text="Módulo de Usuarios", font=("Arial", 16, "bold")).pack(pady=10)

        # ----------- Entrada de datos ----------- 
        frame_form = tk.Frame(self)
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Nombre de usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_form, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_pass = tk.Entry(frame_form, width=30, show="*")
        self.entry_pass.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Rol:").grid(row=2, column=0, padx=5, pady=5)
        self.combo_rol = ttk.Combobox(frame_form, width=28, state="readonly",
                                      values=["Administrador General", "Empleado", "Invitado"])
        self.combo_rol.grid(row=2, column=1, padx=5, pady=5)
        self.combo_rol.current(0)

        # ----------- Botones ----------- 
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Registrar usuario", width=18,
                  command=self.registrar_usuario).grid(row=0, column=0, padx=5)

        tk.Button(frame_btn, text="Eliminar usuario", width=18,
                  command=self.eliminar_usuario).grid(row=0, column=1, padx=5)

        tk.Button(frame_btn, text="Regresar al menú", width=18,
                  command=self.destroy).grid(row=0, column=2, padx=5)

        # ----------- Tabla ----------- 
        self.tabla = ttk.Treeview(self, columns=("id_usuario", "username", "rol"), show="headings")
        self.tabla.heading("id_usuario", text="ID")
        self.tabla.heading("username", text="Nombre de Usuario")
        self.tabla.heading("rol", text="Rol")

        self.tabla.column("id_usuario", width=60)
        self.tabla.column("username", width=200)
        self.tabla.column("rol", width=200)
        self.tabla.pack(pady=10, fill="both", expand=True)

        self.cargar_usuarios()

    # =============================================================
    def registrar_usuario(self):
        nombre = self.entry_nombre.get().strip()
        contraseña = self.entry_pass.get().strip()
        rol = self.combo_rol.get()

        if not nombre or not contraseña:
            messagebox.showwarning("Error", "Debes llenar todos los campos.")
            return

        try:
            conn = crear_conexion()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO usuarios (username, password, Rol) VALUES (%s, %s, %s)",
                (nombre, contraseña, rol)
            )

            conn.commit()
            conn.close()

            self.entry_nombre.delete(0, tk.END)
            self.entry_pass.delete(0, tk.END)
            self.combo_rol.current(0)

            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.cargar_usuarios()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    # =============================================================
    def cargar_usuarios(self):
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, username, Rol FROM usuarios")
        filas = cursor.fetchall()
        conn.close()

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
            conn.close()

            messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
            self.cargar_usuarios()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
