import tkinter as tk
import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox

# --- Importar GUIs ---
from login.loginGUI import login_gui
from usuarios.usuariosGUI import UsuariosGUI
from productos.productosGUI import ProductosGUI
from compras.comprasGUI import ComprasGUI
from ventas.ventasGUI import VentasGUI
from pedidos.pedidosGUI import PedidosGUI
from reportes.reportesGUI import ReportesGUI
from proveedores.proveedoresGUI import ProveedoresGUI

# --- Referencias globales para imágenes ---
icono_usuario_global = None
icono_productos_global = None
icono_compras_global = None
icono_ventas_global = None
icono_pedidos_global = None
icono_reportes_global = None
icono_proveedores_global = None
icono_salir_global = None

def abrir_menu_principal(usuario_actual, rol_usuario):
    global icono_usuario_global
    global icono_productos_global
    global icono_compras_global
    global icono_ventas_global
    global icono_pedidos_global
    global icono_reportes_global
    global icono_proveedores_global
    global icono_salir_global

    if not usuario_actual:
        usuario_actual = "Desconocido"

    rol_usuario = (rol_usuario or "").strip().lower()

    menu = tk.Toplevel()
    menu.title(f"Inventario Ce&Ma — {usuario_actual} — Rol: {rol_usuario}")
    menu.geometry("420x520")
    menu.state('zoomed')
    menu.resizable(True, True)

    rosa_suave = "#FFE4E9"
    negro = "#000000"

    fondo = tk.Frame(menu, bg=rosa_suave)
    fondo.pack(fill="both", expand=True)

    carpeta_busqueda = os.path.dirname(os.path.abspath(__file__))

    # ===========================================================
    #                LOGO ELEGANTE PROFESIONAL
    # ===========================================================

    try:
        ruta_logo = os.path.join(carpeta_busqueda, "CeYMa-Icono.jpg")
        LOGO_SIZE = (130, 130)

        # Cargar logo
        logo_img = Image.open(ruta_logo).resize(LOGO_SIZE, Image.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo_img)
        menu.logo_tk = logo_tk  # Evita garbage collector

        # Sombra del marco
        sombra = tk.Frame(menu, bg="#c4c4c4")
        sombra.place(x=95, y=48, width=150, height=150)

        # Marco tipo tarjeta elegante
        frame_logo = tk.Frame(
            menu,
            bg="white",
            highlightthickness=0,
            bd=0
        )
        frame_logo.place(x=90, y=40, width=150, height=150)

        # Centrar logo dentro del marco
        tk.Label(frame_logo, image=logo_tk, bg="white").pack(expand=True)

    except Exception as e:
        print("Error cargando logo:", e)

    # ===========================================================
    #                 TÍTULO CENTRADO
    # ===========================================================
    tk.Label(
        fondo,
        text=f"Inventario Ce&Ma — Usuario: {usuario_actual}",
        font=("Arial", 22, "bold"),
        bg=rosa_suave,
        fg=negro
    ).pack(pady=(10, 40))

    # ===========================================================
    #                 CARGA DE ICONOS
    # ===========================================================

    ICON_SIZE = (110, 110)

    def cargar_icono(nombres):
        for n in nombres:
            ruta = os.path.join(carpeta_busqueda, n)
            if os.path.exists(ruta):
                img = Image.open(ruta)
                img = img.resize(ICON_SIZE, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
        return None

    icono_productos_global = cargar_icono(["Producto-Icono.jpg", "Producto-Icono.png"])
    icono_compras_global = cargar_icono(["Compra-Icono.png", "Compra-Icono.jpg"])
    icono_ventas_global = cargar_icono(["Ventas-Icono.png", "Ventas-Icono.jpg"])
    icono_pedidos_global = cargar_icono(["Pedidos-Icono.png", "Pedidos-Icono.jpg"])
    icono_reportes_global = cargar_icono(["Reportes-Icono.png", "Reportes-Icono.jpg"])
    icono_proveedores_global = cargar_icono(["Proveedores-Icono.png", "Proveedores-Icono.jpg"])
    icono_salir_global = cargar_icono(["Salir-Icono.png", "Salir-Icono.jpg"])

    # ===========================================================
    #        ICONO USUARIO ARRIBA DERECHA (SOLO ADMIN)
    # ===========================================================

    if rol_usuario == "administrador general":
        try:
            img = Image.open(os.path.join(carpeta_busqueda, "Usuario-Icono.jpg"))
            img = img.resize((55, 55), Image.LANCZOS)
            icono_usuario_global = ImageTk.PhotoImage(img)
            widget_usuario = tk.Label(fondo, image=icono_usuario_global, bg=rosa_suave, cursor="hand2")
            widget_usuario.place(relx=0.93, y=10)
            widget_usuario.bind("<Button-1>", lambda e: UsuariosGUI(menu))
        except:
            tk.Button(fondo, text="Usuarios", command=lambda: UsuariosGUI(menu)).place(relx=0.90, y=10)

    # ===========================================================
    #                   CUERPO CENTRAL
    # ===========================================================

    frame_central = tk.Frame(fondo, bg=rosa_suave)
    frame_central.pack(pady=30)

    def crear_icono_con_texto(frame, icono, texto, comando):
        cont = tk.Frame(frame, bg=rosa_suave)
        cont.pack(side="left", padx=70)

        if icono:
            lbl = tk.Label(cont, image=icono, bg=rosa_suave, cursor="hand2")
            lbl.pack()
            lbl.bind("<Button-1>", lambda e: comando())
        else:
            tk.Button(cont, text=texto, command=comando, width=15).pack()

        tk.Label(cont, text=texto, bg=rosa_suave, font=("Arial", 14, "bold")).pack(pady=5)

    # FILA 1
    fila1 = tk.Frame(frame_central, bg=rosa_suave)
    fila1.pack(pady=15)

    if rol_usuario == "administrador general":
        crear_icono_con_texto(fila1, icono_compras_global, "Compras", lambda: ComprasGUI(menu))

    crear_icono_con_texto(
        fila1,
        icono_productos_global,
        "Productos",
        lambda: ProductosGUI(menu, usuario_actual=usuario_actual)
    )

    # FILA 2
    fila2 = tk.Frame(frame_central, bg=rosa_suave)
    fila2.pack(pady=15)

    crear_icono_con_texto(
        fila2,
        icono_pedidos_global,
        "Pedidos",
        lambda: PedidosGUI(menu, usuario_actual=usuario_actual)
    )

    crear_icono_con_texto(
        fila2,
        icono_ventas_global,
        "Ventas",
        lambda: VentasGUI(menu, usuario_actual=usuario_actual)
    )

    # FILA 3
    fila3 = tk.Frame(frame_central, bg=rosa_suave)
    fila3.pack(pady=15)

    if rol_usuario == "administrador general":
        crear_icono_con_texto(fila3, icono_reportes_global, "Reportes", lambda: ReportesGUI(menu, usuario_actual))
        crear_icono_con_texto(fila3, icono_proveedores_global, "Proveedores", lambda: ProveedoresGUI(menu))

    # ===========================================================
    #                   BOTÓN SALIR
    # ===========================================================

    frame_salir = tk.Frame(fondo, bg=rosa_suave)
    frame_salir.pack(pady=30)

    if icono_salir_global:
        lbl_salir = tk.Label(frame_salir, image=icono_salir_global, bg=rosa_suave, cursor="hand2")
        lbl_salir.pack()
        lbl_salir.bind("<Button-1>", lambda e: menu.destroy())
    else:
        tk.Button(frame_salir, text="Salir", command=menu.destroy, width=20).pack()
