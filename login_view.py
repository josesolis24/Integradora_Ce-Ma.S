import tkinter as tk
from tkinter import messagebox
from user_view import DashboardApp

try:
    from auth_controller import validar_credenciales
except ImportError:
    def validar_credenciales(usuario, password):
        # Stub: acepta un usuario de prueba, evita que el import falle
        return usuario == "test" and password == "test"

class LoginApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Inicio de sesión")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        tk.Label(root, text="Bienvenido al sistema",
                 font=("Arial", 16, "bold")).pack(pady=16)

        tk.Label(root, text="Usuario:").pack(pady=8)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Contraseña: ").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Iniciar sesión", command=self.login).pack(pady=20)

    def login(self):
        usuario = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Faltan datos", "Favor de ingresar usuario y contraseña")
            return

        if validar_credenciales(usuario, password):
            messagebox.showinfo("Acceso permitido", f"Bienvenido {usuario}")
            self.root.destroy()
            DashboardApp(usuario)
            
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()


        