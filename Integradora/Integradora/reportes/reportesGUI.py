import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
import traceback

# === PDF ===
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from conexionBD import crear_conexion


class ReportesGUI:
    def __init__(self, master=None, usuario_actual=None):
        self.usuario_actual = usuario_actual  
        self.master = tk.Toplevel(master)
        self.master.title("Reportes del Sistema — Diagnóstico incluido")

        try:
            self.master.state('zoomed')
        except:
            self.master.attributes('-fullscreen', True)
            self.master.bind('<Escape>', lambda e: self.master.attributes('-fullscreen', False))

        self.master.configure(bg="#1e1e1e")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TCombobox",
                        fieldbackground="#2d2d2d",
                        background="#2d2d2d",
                        foreground="white",
                        bordercolor="#3c3c3c",
                        selectbackground="#3c3c3c")

        style.configure("Treeview",
                        background="#2d2d2d",
                        foreground="white",
                        fieldbackground="#2d2d2d",
                        rowheight=25,
                        bordercolor="#3c3c3c")

        style.configure("Treeview.Heading",
                        background="#007acc",
                        foreground="white",
                        font=("Arial", 10, "bold"))

        style.map("Treeview", background=[("selected", "#005f99")])

        tk.Label(self.master, text="📊 Reportes del Sistema",
                 font=("Arial", 18, "bold"),
                 fg="#4fc1ff", bg="#1e1e1e").pack(pady=10)

        # listas de reportes
        self.reportes_lista = [
            "Productos registrados",
            "Categorias registradas",
            "Ventas registradas",
            "Compras registradas",
            "Pedidos registrados",
            "Proveedores registrados"
        ]

        self.combo_reportes = ttk.Combobox(
            self.master, state="readonly",
            values=self.reportes_lista,
            width=40
        )
        self.combo_reportes.pack(pady=6)
        self.combo_reportes.set("Seleccione un reporte...")
        self.combo_reportes.bind("<<ComboboxSelected>>", self._limpiar_log)

        frame_btn = tk.Frame(self.master, bg="#1e1e1e")
        frame_btn.pack(pady=6)

        self.btn_style = {
            "bg": "#007acc",
            "fg": "white",
            "activebackground": "#005f99",
            "activeforeground": "white",
            "font": ("Arial", 10, "bold"),
            "width": 20
        }

        tk.Button(frame_btn, text="Generar Reporte (SELECT *)",
                  command=self.generar_reporte, **self.btn_style).grid(row=0, column=0, padx=6)

        tk.Button(frame_btn, text="Diagnosticar tablas",
                  command=self.diagnosticar, **self.btn_style).grid(row=0, column=1, padx=6)

        tk.Button(frame_btn, text="Exportar PDF del reporte",
                  command=self.exportar_pdf, **self.btn_style).grid(row=0, column=2, padx=6)

        tk.Button(frame_btn, text="Regresar al Menú",
                  command=self.master.destroy, **self.btn_style).grid(row=0, column=3, padx=6)

        self.tabla = ttk.Treeview(self.master, show="headings")
        self.tabla.pack(expand=True, fill="both", padx=10, pady=12)

        tk.Label(self.master, text="Salida de diagnóstico:",
                 font=("Arial", 10, "bold"),
                 fg="#4fc1ff", bg="#1e1e1e").pack(anchor="w", padx=12)

        self.txt_diag = tk.Text(self.master, height=6, bg="#252526", fg="white")
        self.txt_diag.pack(fill="x", padx=12, pady=(0, 12))

        # Mapeo de fallback
        self._primary_table = {
            "Productos registrados": "productos",
            "Categorias registradas": "categorias",
            "Ventas registradas": "ventas",
            "Compras registradas": "compras",
            "Pedidos registrados": "pedidos",
            "Proveedores registrados": "proveedores"
        }

    # ===========================================================
    #  QUERIES
    # ===========================================================
    def obtener_query(self, reporte):

        if reporte == "Productos registrados":
            return """
                SELECT 
                    id_producto,
                    nombre,
                    descripcion,
                    precio,
                    stock,
                    id_categoria,
                    id_proveedor,
                    creado_por,
                    actualizado_por
                FROM productos
            """

        if reporte == "Categorias registradas":
            return """
                SELECT 
                    id_categoria,
                    nombre,
                    creado_por,
                    actualizado_por
                FROM categorias
            """

        if reporte == "Ventas registradas":
            return """
                SELECT
                    id_venta,
                    fecha,
                    id_producto,
                    nombre_producto,
                    cantidad,
                    total,
                    creado_por,
                    actualizado_por,
                    cliente
                FROM ventas
            """

        if reporte == "Compras registradas":
            return """
                SELECT
                    id_compra,
                    fecha,
                    id_proveedor,
                    proveedor_nombre,
                    id_producto,
                    nombre_producto,
                    cantidad,
                    total,
                    id_categoria,
                    nombre_categoria
                FROM compras
            """

        if reporte == "Pedidos registrados":
            return """
                SELECT
                    id_pedido,
                    cliente,
                    producto AS id_producto,
                    nombre_producto,
                    cantidad,
                    precio,
                    anticipo,
                    total,
                    restante,
                    fecha_entrega,
                    estado,
                    creado_por,
                    actualizado_por
                FROM pedidos
            """

        if reporte == "Proveedores registrados":
            return """
                SELECT
                    id_proveedor,
                    nombre,
                    telefono,
                    direccion,
                    correo_electronico
                FROM proveedores
            """

        return None

    # ===========================================================
    #   GUARDAR REPORTE EN BD
    # ===========================================================
    def registrar_reporte_en_bd(self, nombre_reporte, total_registros):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reportes_generados (
                    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_reporte VARCHAR(255),
                    total_registros INT,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usuario VARCHAR(255)
                )
            """)

            cursor.execute("""
                INSERT INTO reportes_generados (nombre_reporte, total_registros, usuario)
                VALUES (%s, %s, %s)
            """, (nombre_reporte, total_registros, self.usuario_actual or "Desconocido"))

            conexion.commit()
            cursor.close()
            conexion.close()

            self._log(f"✔ Reporte guardado en BD correctamente")

        except Exception as e:
            self._log(f"❌ ERROR guardando el reporte en BD: {e}")

    # ===========================================================
    #   GENERAR REPORTE
    # ===========================================================
    def generar_reporte(self):
        reporte = self.combo_reportes.get().strip()

        if reporte == "Seleccione un reporte..." or not reporte:
            messagebox.showwarning("⚠️", "Selecciona un reporte válido.")
            return

        self._limpiar_log()
        query = self.obtener_query(reporte)

        conexion = None
        cursor = None

        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            try:
                cursor.execute(query)
            except Exception:
                tabla = self._primary_table[reporte]
                cursor.execute(f"SELECT * FROM `{tabla}`")

            datos = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]

            self.configurar_tabla(columnas)
            for fila in datos:
                self.tabla.insert("", tk.END, values=fila)

            self._log(f"Reporte generado: {reporte} ({len(datos)} registros)")

            # 🔥 GUARDAR EN BD →
            self.registrar_reporte_en_bd(reporte, len(datos))

        except Exception as e:
            tb = traceback.format_exc()
            self.txt_diag.insert(tk.END, f"{e}\n{tb}")
            messagebox.showerror("ERROR", str(e))

        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    # ===========================================================
    #   EXPORTAR PDF
    # ===========================================================
    def exportar_pdf(self):
        try:
            columnas = self.tabla["columns"]
            filas = [self.tabla.item(i, "values") for i in self.tabla.get_children()]

            if not filas:
                messagebox.showwarning("⚠️", "No hay datos para exportar.")
                return

            carpeta = "reportes"
            os.makedirs(carpeta, exist_ok=True)

            import datetime
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo = os.path.join(carpeta, f"reporte_exportado_{ts}.pdf")

            pdf = SimpleDocTemplate(archivo, pagesize=letter)
            styles = getSampleStyleSheet()
            contenido = []

            ruta_logo = r"C:\Users\emili\OneDrive\Documentos\Integradora\Integradora\CeYMa-Icono.jpg"

            if os.path.exists(ruta_logo):
                img = RLImage(ruta_logo, width=120, height=120)
                img.hAlign = "LEFT"
                contenido.append(img)
                contenido.append(Spacer(1, 10))

            contenido.append(Paragraph("<b>Reporte Exportado</b>", styles["Title"]))
            contenido.append(Spacer(1, 12))

            filas_norm = []
            for r in filas:
                r = ["" if x is None else str(x) for x in r]
                filas_norm.append(r)

            tabla_pdf = Table([list(columnas)] + filas_norm, repeatRows=1)

            tabla_pdf.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ffb6c1")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.7, colors.gray),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]))

            contenido.append(tabla_pdf)
            pdf.build(contenido)

            messagebox.showinfo("PDF generado", f"PDF guardado en:\n{archivo}")

        except Exception as e:
            tb = traceback.format_exc()
            self.txt_diag.insert(tk.END, f"ERROR:\n{e}\n{tb}")
            messagebox.showerror("ERROR PDF", str(e))

    # ===========================================================
    def configurar_tabla(self, columnas):
        self.tabla.delete(*self.tabla.get_children())
        self.tabla["columns"] = columnas

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150, anchor="w")

    # ===========================================================
    def diagnosticar(self):
        tablas = ["productos", "categorias", "ventas", "compras", "pedidos", "proveedores"]
        salida = []

        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            for t in tablas:
                try:
                    cursor.execute(f"DESCRIBE `{t}`")
                    col = cursor.fetchall()
                    cursor.execute(f"SELECT COUNT(*) FROM `{t}`")
                    filas = cursor.fetchone()[0]
                    salida.append(f"[{t}] OK | {len(col)} columnas | {filas} filas")
                except Exception as e:
                    salida.append(f"[{t}] ERROR: {e}")

            self.txt_diag.delete("1.0", tk.END)
            self.txt_diag.insert(tk.END, "\n".join(salida))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ===========================================================
    def _limpiar_log(self, event=None):
        self.txt_diag.delete("1.0", tk.END)

    def _log(self, texto):
        self.txt_diag.insert(tk.END, texto + "\n")
        self.txt_diag.see(tk.END)
