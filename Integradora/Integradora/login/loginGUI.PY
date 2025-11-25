import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion


class LoginGUI(tk.Toplevel):
    """
    Login con verificación de usuario, contraseña y ROL.
    Envía el rol al menú principal.
    """

    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.title("Inicio de Sesión")
        self.geometry("320x220")
        self.on_success = on_success

        # ------ Etiquetas ------
        ttk.Label(self, text="Usuario:", font=("Arial", 12)).pack(pady=5)
        self.entry_usuario = ttk.Entry(self, width=28)
        self.entry_usuario.pack()

        ttk.Label(self, text="Contraseña:", font=("Arial", 12)).pack(pady=5)
        self.entry_contra = ttk.Entry(self, width=28, show="*")
        self.entry_contra.pack()

        # ------ Botón ------
        ttk.Button(self, text="Iniciar Sesión", command=self.verificar).pack(pady=15)

        self.update_idletasks()
        self.center_window()

    def center_window(self):
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def verificar(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contra.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Aviso", "Por favor completa todos los campos.")
            return

        conexion = crear_conexion()
        if not conexion:
            messagebox.showerror("Error", "❌ No se pudo conectar a la base de datos.")
            return

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id_usuario, username, Rol 
                FROM usuarios 
                WHERE username=%s AND password=%s
            """, (usuario, contrasena))

            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                user_id, user_name, rol = resultado
                rol = rol if rol else "Sin Rol"

                messagebox.showinfo(
                    "Bienvenido",
                    f"Inicio de sesión exitoso, {user_name}\nRol: {rol}"
                )

                # 👉 Mandamos el rol al menú
                self.on_success(rol)

                self.destroy()

            else:
                messagebox.showwarning("Error", "Usuario o contraseña incorrectos.")

        except Exception as e:
            messagebox.showerror("Error SQL", f"⚠️ Ocurrió un error: {e}")


def login_gui(parent, on_success):
    ventana = LoginGUI(parent, on_success)
    ventana.grab_set()
    return ventana
