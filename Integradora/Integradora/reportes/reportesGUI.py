import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

# Asegura que podemos encontrar conexionBD.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from conexionBD import crear_conexion


class ReportesGUI:
    def __init__(self, master=None):
        self.master = tk.Toplevel(master)
        self.master.title("Reportes del Sistema — Diagnóstico incluido")
        self.master.geometry("1000x600")

        # ====================== ESTILO DE COLORES ======================
        self.master.configure(bg="#1e1e1e")

        style = ttk.Style()
        style.theme_use("clam")

        # Combobox
        style.configure(
            "TCombobox",
            fieldbackground="#2d2d2d",
            background="#2d2d2d",
            foreground="white",
            bordercolor="#3c3c3c",
            selectbackground="#3c3c3c"
        )

        # Treeview
        style.configure(
            "Treeview",
            background="#2d2d2d",
            foreground="white",
            fieldbackground="#2d2d2d",
            rowheight=25,
            bordercolor="#3c3c3c"
        )
        style.configure(
            "Treeview.Heading",
            background="#007acc",
            foreground="white",
            font=("Arial", 10, "bold")
        )
        style.map("Treeview", background=[("selected", "#005f99")])

        tk.Label(
            self.master, text="📊 Reportes del Sistema",
            font=("Arial", 18, "bold"),
            fg="#4fc1ff", bg="#1e1e1e"
        ).pack(pady=10)

        # ====================== COMBOBOX CON PROVEEDORES ======================
        self.combo_reportes = ttk.Combobox(
            self.master, state="readonly",
            values=[
                "Productos registrados",
                "Categorias registradas",
                "Ventas registradas",
                "Compras registradas",
                "Pedidos registrados",
                "Proveedores registrados"   # 🔥 NUEVO
            ],
            width=40
        )
        self.combo_reportes.pack(pady=6)
        self.combo_reportes.set("Seleccione un reporte...")

        # ====================== BOTONES ======================
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

        tk.Button(frame_btn, text="Regresar al Menú",
                  command=self.master.destroy, **self.btn_style).grid(row=0, column=2, padx=6)

        # ====================== TABLA ======================
        self.tabla = ttk.Treeview(self.master, show="headings")
        self.tabla.pack(expand=True, fill="both", padx=10, pady=12)

        # ====================== ZONA DE DIAGNOSTICO ======================
        tk.Label(
            self.master, text="Salida de diagnóstico:",
            font=("Arial", 10, "bold"),
            fg="#4fc1ff", bg="#1e1e1e"
        ).pack(anchor="w", padx=12)

        self.txt_diag = tk.Text(self.master, height=6, bg="#252526", fg="white")
        self.txt_diag.pack(fill="x", padx=12, pady=(0, 12))


    # ========================= FUNCIONES =========================

    def registrar_reporte(self, tipo, descripcion):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO reportes (tipo, descripcion)
                VALUES (%s, %s)
            """, (tipo, descripcion))
            conexion.commit()
            conexion.close()
        except Exception as e:
            self._log(f"⚠️ Error guardando en reportes: {e}")


    def generar_reporte(self):
        reporte = self.combo_reportes.get().strip()
        if reporte == "Seleccione un reporte..." or not reporte:
            messagebox.showwarning("⚠️", "Selecciona un reporte válido.")
            return

        # 📌 ahora incluye proveedores
        mapping = {
            "Productos registrados": "productos",
            "Categorias registradas": "categorias",
            "Ventas registradas": "ventas",
            "Compras registradas": "compras",
            "Pedidos registrados": "pedidos",
            "Proveedores registrados": "proveedores"   # 🔥 NUEVO
        }

        tabla = mapping.get(reporte)

        query = f"SELECT * FROM `{tabla}` LIMIT 1000"

        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute(query)
            datos = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]

            self.configurar_tabla(columnas)
            for fila in datos:
                self.tabla.insert("", tk.END, values=fila)

            descripcion = f"Reporte generado: {tabla} ({len(datos)} registros)"
            self.registrar_reporte(reporte, descripcion)
            self._log(descripcion)

            if not datos:
                messagebox.showinfo("ℹ️", f"La tabla `{tabla}` está vacía.")

        except Exception as e:
            messagebox.showerror("❌ ERROR", f"{e}")

        finally:
            try: conexion.close()
            except: pass


    def configurar_tabla(self, columnas):
        for c in self.tabla.get_children(): self.tabla.delete(c)
        self.tabla["columns"] = columnas
        self.tabla["show"] = "headings"

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150, anchor="w")


    def diagnosticar(self):
        tablas = ["productos", "categorias", "ventas", "compras", "pedidos", "proveedores"]  # 🔥 agregado proveedores
        salida = []

        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            for t in tablas:
                try:
                    cursor.execute(f"DESCRIBE `{t}`")
                    columnas = [c[0] for c in cursor.fetchall()]
                    cursor.execute(f"SELECT COUNT(*) FROM `{t}`")
                    filas = cursor.fetchone()[0]

                    salida.append(f"[{t}] columnas: {columnas}")
                    salida.append(f"[{t}] filas: {filas}\n")

                except Exception as e:
                    salida.append(f"[{t}] ❌ ERROR: {e}\n")

            self.txt_diag.delete("1.0", tk.END)
            self.txt_diag.insert(tk.END, "".join(salida))

        except Exception as e:
            messagebox.showerror("❌", f"{e}")

        finally:
            try: conexion.close()
            except: pass


    def _log(self, texto):
        self.txt_diag.insert(tk.END, texto + "\n")
        self.txt_diag.see(tk.END)
