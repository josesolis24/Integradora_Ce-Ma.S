import tkinter as tk
from tkinter import ttk, messagebox
from conexionBD import crear_conexion


class LoginGUI(tk.Toplevel):
    """
    Login con verificación de usuario, contraseña y ROL.
    Envía (username, rol) a la función on_success.
    """

    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.title("Inicio de Sesión")
        self.geometry("320x220")
        self.on_success = on_success

        # ------ Etiquetas y entradas ------
        ttk.Label(self, text="Usuario:", font=("Arial", 12)).pack(pady=(12, 4))
        self.entry_usuario = ttk.Entry(self, width=28)
        self.entry_usuario.pack()
        self.entry_usuario.focus_set()

        ttk.Label(self, text="Contraseña:", font=("Arial", 12)).pack(pady=(8, 4))
        self.entry_contra = ttk.Entry(self, width=28, show="*")
        self.entry_contra.pack()

        # ------ Botón ------
        btn = ttk.Button(self, text="Iniciar Sesión", command=self.verificar)
        btn.pack(pady=15)

        # Permitir enviar con Enter
        self.bind("<Return>", lambda e: self.verificar())

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

    # ================================================================
    def verificar(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contra.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Aviso", "Por favor completa todos los campos.")
            return

        conexion = crear_conexion()
        if not conexion:
            messagebox.showerror("Error", "❌ No se pudo conectar a la base de datos.")
            return

        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id_usuario, username, rol
                FROM usuarios 
                WHERE username = %s AND password = %s
            """, (usuario, contrasena))

            resultado = cursor.fetchone()

            if resultado:
                user_id, user_name, rol = resultado

                rol_normalizado = rol.strip() if isinstance(rol, str) else str(rol)

                messagebox.showinfo(
                    "Bienvenido",
                    f"Inicio de sesión exitoso 👋\nUsuario: {user_name}\nRol: {rol_normalizado}"
                )

                # Llamada consistente: enviamos (username, rol)
                try:
                    self.on_success(user_name, rol_normalizado)
                except TypeError:
                    # Compatibilidad con callers que esperan sólo un arg
                    try:
                        self.on_success(user_name)
                    except Exception:
                        pass

                self.destroy()
            else:
                messagebox.showwarning("Error", "Usuario o contraseña incorrectos.")

        except Exception as e:
            messagebox.showerror("Error SQL", f"⚠️ Ocurrió un error: {e}")

        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            try:
                conexion.close()
            except:
                pass


def login_gui(parent, on_success):
    ventana = LoginGUI(parent, on_success)
    ventana.grab_set()
    return ventana
