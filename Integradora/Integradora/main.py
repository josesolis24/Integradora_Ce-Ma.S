import tkinter as tk
from menu import abrir_menu_principal      
from login.loginGUI import login_gui



def main():
    root = tk.Tk()
    root.withdraw()  # Oculta ventana mientras no inicias sesión

    # Abrir login primero y luego abrir menú principal
    login_gui(root, abrir_menu_principal)

    root.mainloop()


if __name__ == "__main__":
    main()

