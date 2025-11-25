
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


def abrir_menu_principal(rol_usuario):
    menu = tk.Toplevel()
    menu.title(f"Inventario Ce&Ma — Rol: {rol_usuario}")
    menu.geometry("420x520")

    # ---- COLORES ----
    rosa_fuerte = "#FFC0CB"
    rosa_suave = "#FFE4E9"
    blanco = "#FFFFFF"
    negro = "#000000"

    # Fondo
    fondo = tk.Frame(menu, bg=rosa_suave)
    fondo.pack(fill="both", expand=True)

    # ---- TÍTULO ----
    tk.Label(
        fondo,
        text="Inventario Ce&Ma",
        font=("Arial", 18, "bold"),
        bg=rosa_suave,
        fg=negro
    ).pack(pady=20)

    # --- FUNCIÓN PARA CREAR BOTONES BONITOS ---
    def boton(texto, comando):
        return tk.Button(
            fondo,
            text=texto,
            width=25,
            bg=blanco,
            fg=negro,
            activebackground=rosa_fuerte,
            activeforeground=negro,
            command=comando,
            relief="ridge",
            bd=3
        )

    # --- BOTONES ---
    btn_usuarios = boton("Usuarios", lambda: UsuariosGUI(menu))
    btn_usuarios.pack(pady=6)

    btn_productos = boton("Productos", lambda: ProductosGUI(menu))
    btn_productos.pack(pady=6)

    btn_categorías = boton("Categorías", lambda: CategoriasGUI(menu))
    btn_categorías.pack(pady=6)

    btn_compras = boton("Compras", lambda: ComprasGUI(menu))
    btn_compras.pack(pady=6)

    btn_ventas = boton("Ventas", lambda: VentasGUI(menu))
    btn_ventas.pack(pady=6)

    btn_pedidos = boton("Pedidos", lambda: PedidosGUI(menu))
    btn_pedidos.pack(pady=6)

    btn_reportes = boton("Reportes", lambda: ReportesGUI(menu))
    btn_reportes.pack(pady=6)

    # -----------------------------
    # 👉 CONTROL DE PERMISOS POR ROL
    # -----------------------------
    # Ocultar módulos según el rol
    if rol_usuario != "Administrador General":
        btn_usuarios.pack_forget()
        btn_reportes.pack_forget()
        # Puedes agregar más restricciones si quieres

    # Botón Salir
    boton("Salir", menu.destroy).pack(pady=25)
