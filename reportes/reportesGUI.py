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

        tk.Label(self.master, text="📊 Reportes del Sistema", font=("Arial", 18, "bold")).pack(pady=10)

        # Opciones de reporte
        self.combo_reportes = ttk.Combobox(
            self.master, state="readonly",
            values=[
                "Productos registrados",
                "Categorias registradas",
                "Ventas registradas",
                "Compras registradas"
            ], width=40
        )
        self.combo_reportes.pack(pady=6)
        self.combo_reportes.set("Seleccione un reporte...")

        frame_btn = tk.Frame(self.master)
        frame_btn.pack(pady=6)

        tk.Button(frame_btn, text="Generar Reporte (SELECT *)", width=22, command=self.generar_reporte).grid(row=0, column=0, padx=6)
        tk.Button(frame_btn, text="Diagnosticar tablas", width=18, command=self.diagnosticar).grid(row=0, column=1, padx=6)
        tk.Button(frame_btn, text="Regresar al Menú", width=18, command=self.master.destroy).grid(row=0, column=2, padx=6)

        # Treeview para resultados
        self.tabla = ttk.Treeview(self.master, show="headings")
        self.tabla.pack(expand=True, fill="both", padx=10, pady=12)

        # Area de log/diagnóstico (texto)
        tk.Label(self.master, text="Salida de diagnóstico:", font=("Arial", 10, "bold")).pack(anchor="w", padx=12)
        self.txt_diag = tk.Text(self.master, height=6)
        self.txt_diag.pack(fill="x", padx=12, pady=(0,12))

    def generar_reporte(self):
        reporte = self.combo_reportes.get().strip()
        if not reporte or reporte == "Seleccione un reporte...":
            messagebox.showwarning("⚠️", "Selecciona un reporte válido.")
            return

        # Mapeo de etiqueta a tabla real (ajusta si tus tablas se llaman distinto)
        mapping = {
            "Productos registrados": "productos",
            "Categorias registradas": "categorias",
            "Ventas registradas": "ventas",
            "Compras registradas": "compras"
        }

        tabla = mapping.get(reporte)
        if not tabla:
            messagebox.showerror("❌", "Reporte no mapeado correctamente.")
            return

        query = f"SELECT * FROM `{tabla}` LIMIT 1000"  # LIMIT para no petar si hay muchísimos registros

        conexion = None
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute(query)
            datos = cursor.fetchall()

            # Si no hay filas, igual obtenemos nombres de columnas
            cols = []
            if cursor.description:
                cols = [desc[0] for desc in cursor.description]
            else:
                cols = []

            # Configurar tabla con nombres reales de columnas
            self.configurar_tabla(cols)

            # Insertar filas (si hay)
            for fila in datos:
                # Convertir valores None a string vacío para evitar problemas
                row = tuple("" if v is None else v for v in fila)
                self.tabla.insert("", tk.END, values=row)

            # Mensaje si no hay datos
            if not datos:
                self._log(f"No se encontraron registros en la tabla `{tabla}` (0 filas).")
                messagebox.showinfo("ℹ️ Sin registros", f"La tabla `{tabla}` está vacía o no tiene registros visibles.")
            else:
                self._log(f"Mostrando {len(datos)} filas de `{tabla}`. Columnas: {cols}")

        except Exception as e:
            # Mostrar error detallado para depuración
            self._log(f"ERROR al ejecutar query sobre `{tabla}`: {e}")
            messagebox.showerror("❌ Error al generar reporte", f"Error al ejecutar:\n{e}")
        finally:
            if conexion:
                conexion.close()

    def configurar_tabla(self, columnas):
        # Limpiar antes
        for c in self.tabla.get_children():
            self.tabla.delete(c)
        self.tabla["columns"] = columnas
        self.tabla["show"] = "headings"
        # Eliminar encabezados previos
        for col in self.tabla["columns"]:
            # no-op, nos aseguramos de reconfigurar
            pass
        # Configurar cada columna
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150, anchor="w")

    def diagnosticar(self):
        """
        Ejecuta DESCRIBE + COUNT(*) para cada tabla y despliega resultados en el cuadro de texto.
        Esto te dirá exactamente cómo se llaman las columnas y cuántas filas hay.
        """
        tablas = ["productos", "categorias", "ventas", "compras"]
        conexion = None
        salida = []
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            for t in tablas:
                try:
                    cursor.execute(f"DESCRIBE `{t}`")
                    desc = cursor.fetchall()
                    if not desc:
                        salida.append(f"[{t}] DESCRIBE devolvió vacío (tabla puede no existir).")
                        continue

                    cols = [row[0] for row in desc]
                    salida.append(f"[{t}] columnas: {cols}")

                    # contar filas
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM `{t}`")
                        cnt = cursor.fetchone()[0]
                        salida.append(f"[{t}] filas: {cnt}")
                    except Exception as e_cnt:
                        salida.append(f"[{t}] ERROR al contar filas: {e_cnt}")

                except Exception as e_desc:
                    salida.append(f"[{t}] ERROR DESCRIBE: {e_desc}")

            # Mostrar salida en cuadro de diagnóstico
            self.txt_diag.delete("1.0", tk.END)
            self.txt_diag.insert(tk.END, "\n".join(salida))
            messagebox.showinfo("✅ Diagnóstico completado", "Revisa el cuadro de diagnóstico abajo para ver esquemas y conteos.")
        except Exception as e:
            messagebox.showerror("❌ Error en diagnóstico", f"Ocurrió un error al conectar: {e}")
            self._log(f"ERROR en diagnosticar: {e}")
        finally:
            if conexion:
                conexion.close()

    def _log(self, texto):
        """Agrega una línea al cuadro de diagnóstico (también útil para mensajes)."""
        self.txt_diag.insert(tk.END, texto + "\n")
        self.txt_diag.see(tk.END)
