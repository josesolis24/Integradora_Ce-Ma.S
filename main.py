import tkinter as tk

# --- Importar GUIs ---
from login.loginGUI import login_gui
from usuarios.usuariosGUI import UsuariosGUI
from productos.productosGUI import ProductosGUI
from categorias.categoriasGUI import CategoriasGUI
from compras.comprasGUI import ComprasGUI
from ventas.ventasGUI import VentasGUI
from pedidos.pedidosGUI import PedidosGUI
from reportes.reportesGUI import ReportesGUI


def abrir_menu_principal():
    menu = tk.Toplevel()
    menu.title("Menú Principal")
    menu.geometry("420x520")

    tk.Label(menu, text="Menú Principal", font=("Arial", 18, "bold")).pack(pady=20)

    # --- BOTONES ---
    tk.Button(menu, text="Usuarios", width=25,
              command=lambda: UsuariosGUI(menu)).pack(pady=6)

    tk.Button(menu, text="Productos", width=25,
              command=lambda: ProductosGUI(menu)).pack(pady=6)

    tk.Button(menu, text="Categorías", width=25,
              command=lambda: CategoriasGUI(menu)).pack(pady=6)

    tk.Button(menu, text="Compras", width=25,
              command=lambda: ComprasGUI(menu)).pack(pady=6)

    tk.Button(menu, text="Ventas", width=25,
              command=lambda: VentasGUI(menu)).pack(pady=6)

    tk.Button(menu, text="Pedidos", width=25,
              command=lambda: PedidosGUI(menu)).pack(pady=6)

    tk.Button(menu, text="Reportes", width=25,
              command=lambda: ReportesGUI(menu)).pack(pady=6)

    tk.Button(menu, text="Salir", width=25, command=menu.destroy).pack(pady=25)


def main():
    root = tk.Tk()
    root.withdraw()  # Oculta ventana mientras no inicias sesión

    # Abrir login primero
    login_gui(root, abrir_menu_principal)

    root.mainloop()


if __name__ == "__main__":
    main()

