import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from conexionBD import crear_conexion
from decimal import Decimal

# reportlab para generar PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet


class PedidosGUI:
    def __init__(self, master=None, usuario_actual=None, regresar_callback=None):
        self.master = tk.Toplevel(master)
        self.master.title("Gestión de Pedidos")
        self.master.state("zoomed")

        # usuario_actual puede ser el nombre o rol; lo usaremos para permisos (inferir rol)
        self.usuario_actual = usuario_actual or "Desconocido"

        self.color_fondo = "#FADADD"
        self.color_boton = "white"
        self.color_texto = "black"
        self.master.config(bg=self.color_fondo)
        self.regresar_callback = regresar_callback

        tk.Label(
            self.master, text="Módulo de Pedidos",
            font=("Arial", 18, "bold"),
            bg=self.color_fondo, fg=self.color_texto
        ).pack(pady=10)

        # ------------------ BOTONES ------------------
        frame_btn = tk.Frame(self.master, bg=self.color_fondo)
        frame_btn.pack(pady=5)

        tk.Button(frame_btn, text="Registrar Pedido", width=25,
                  bg=self.color_boton, fg=self.color_texto,
                  command=self.abrir_formulario_registro).grid(row=0, column=0, padx=10)

        tk.Button(frame_btn, text="Modificar Pedido", width=25,
                  bg=self.color_boton, fg=self.color_texto,
                  command=self.modificar_pedido).grid(row=0, column=1, padx=10)

        tk.Button(frame_btn, text="Eliminar Pedido", width=25,
                  bg=self.color_boton, fg=self.color_texto,
                  command=self.eliminar_pedido).grid(row=0, column=2, padx=10)

        tk.Button(frame_btn, text="Regresar al Menú", width=25,
                  bg=self.color_boton, fg=self.color_texto,
                  command=self.regresar_menu).grid(row=0, column=3, padx=10)

        # ------------------ TABLA DE PEDIDOS ------------------
        columnas = (
            "ID", "Cliente", "Producto", "Cantidad", "Precio",
            "Anticipo", "Total", "Restante",
            "Fecha Entrega", "Estado",
            "Creado por", "Actualizado por"
        )

        self.tabla = ttk.Treeview(self.master, columns=columnas, show="headings", height=14)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120)

        self.tabla.pack(padx=10, pady=10, fill="x")

        # ------------------ TABLA DE PRODUCTOS ------------------
        tk.Label(
            self.master, text="Productos en Existencia",
            font=("Arial", 15, "bold"), bg=self.color_fondo
        ).pack(pady=5)

        # Agregada la columna "Descripción" si la tienes en BD
        columnas_prod = ("ID", "Producto", "Descripción", "Stock", "Precio")
        self.tabla_prod = ttk.Treeview(self.master, columns=columnas_prod, show="headings", height=10)

        for col in columnas_prod:
            self.tabla_prod.heading(col, text=col)
            # Ajusto ancho para que la descripción tenga espacio
            if col == "Descripción":
                self.tabla_prod.column(col, width=300)
            else:
                self.tabla_prod.column(col, width=120)

        self.tabla_prod.pack(padx=10, pady=10, fill="x")

        # Diccionario producto_nombre -> id
        self.productos_dict = self.obtener_productos()
        self.mostrar_pedidos()
        self.mostrar_productos()

    # ----------------- Helpers -----------------
    def _inferir_rol(self):
        """Inferir rol a partir de self.usuario_actual (si viene como texto)."""
        if isinstance(self.usuario_actual, str):
            low = self.usuario_actual.strip().lower()
            if low in ("administrador", "admin", "administrador general"):
                return "Administrador"
            if low in ("empleado", "emple"):
                return "Empleado"
            if low in ("invitado", "guest"):
                return "Invitado"
        # por defecto, tratamos como Empleado (permite editar cantidad y fecha)
        return "Empleado"

    # ---------------------------------------------------------
    # MOSTRAR TABLAS
    # ---------------------------------------------------------
    def obtener_productos(self):
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_producto, nombre FROM productos")
        productos = cursor.fetchall()
        conn.close()
        return {nombre: pid for pid, nombre in productos}

    def mostrar_productos(self):
        for row in self.tabla_prod.get_children():
            self.tabla_prod.delete(row)

        conn = crear_conexion()
        cursor = conn.cursor()
        # Si tu tabla productos tiene descripcion, la mostramos; si no, ajusta la query.
        cursor.execute("SELECT id_producto, nombre, descripcion, stock, precio FROM productos")
        productos = cursor.fetchall()
        conn.close()

        for p in productos:
            self.tabla_prod.insert("", tk.END, values=p)

    def mostrar_pedidos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_pedido, cliente, nombre_producto, cantidad, precio,
                   anticipo, total, restante,
                   DATE_FORMAT(fecha_entrega, '%d-%m-%Y'), estado,
                   creado_por, actualizado_por
            FROM pedidos
            ORDER BY id_pedido DESC
        """)
        pedidos = cursor.fetchall()
        conn.close()

        for p in pedidos:
            self.tabla.insert("", tk.END, values=p)

    # ---------------------------------------------------------
    # REGISTRAR PEDIDO
    # ---------------------------------------------------------
    def abrir_formulario_registro(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Registrar Pedido")
        ventana.geometry("450x500")
        ventana.config(bg=self.color_fondo)

        campos = [
            ("Cliente:", "cliente"),
            ("Producto:", "producto"),
            ("Cantidad:", "cantidad"),
            ("Precio unidad:", "precio"),
            ("Anticipo:", "anticipo"),
            ("Fecha entrega (DD-MM-YYYY):", "fecha"),
            ("Estado:", "estado")
        ]

        self.entries = {}
        nombres_productos = list(self.productos_dict.keys())

        for i, (texto, key) in enumerate(campos):
            tk.Label(ventana, text=texto, bg=self.color_fondo, fg=self.color_texto)\
                .grid(row=i, column=0, padx=5, pady=5, sticky="e")

            if key == "producto":
                self.entries[key] = ttk.Combobox(ventana, values=nombres_productos, state="readonly")
            else:
                self.entries[key] = tk.Entry(ventana)

            self.entries[key].grid(row=i, column=1, padx=5, pady=5)

        self.entries["estado"].insert(0, "Pendiente")

        tk.Button(
            ventana, text="Guardar Pedido", width=30,
            bg=self.color_boton, fg=self.color_texto,
            command=lambda: self.registrar_pedido(ventana)
        ).grid(row=10, column=0, columnspan=2, pady=20)

    def registrar_pedido(self, ventana_form):
        datos = {k: e.get().strip() for k, e in self.entries.items()}

        if any(not v for v in datos.values()):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        try:
            fecha_guardar = datetime.strptime(datos["fecha"], "%d-%m-%Y").strftime("%Y-%m-%d")
            cantidad = float(datos["cantidad"])
            precio = float(datos["precio"])
            anticipo = float(datos["anticipo"]) if datos["anticipo"] != "" else 0.0
            total = cantidad * precio
            restante = total - anticipo
            estado_final = "Pagado" if restante <= 0 else datos["estado"]

            id_producto = self.productos_dict[datos["producto"]]

            conexion = crear_conexion()
            cursor = conexion.cursor()

            cursor.execute("SELECT stock FROM productos WHERE id_producto=%s", (id_producto,))
            stock_actual = float(cursor.fetchone()[0])

            if cantidad > stock_actual:
                messagebox.showwarning("Stock insuficiente", f"Solo hay {stock_actual} disponibles.")
                conexion.close()
                return

            stock_nuevo = stock_actual - cantidad

            if not messagebox.askyesno("Confirmación",
                f"Total: ${total}\nAnticipo: ${anticipo}\nRestante: ${restante}\n\n¿Continuar?"):
                conexion.close()
                return

            cursor.execute("UPDATE productos SET stock=%s WHERE id_producto=%s",
                           (stock_nuevo, id_producto))

            cursor.execute("""
                INSERT INTO pedidos
                (cliente, producto, nombre_producto, cantidad, precio, anticipo,
                 total, restante, fecha_entrega, estado, creado_por, actualizado_por)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                datos["cliente"], id_producto, datos["producto"], cantidad, precio,
                anticipo, total, restante, fecha_guardar, estado_final,
                self.usuario_actual, self.usuario_actual
            ))

            conexion.commit()
            conexion.close()
            messagebox.showinfo("Guardado", "Pedido registrado exitosamente.")
            ventana_form.destroy()
            self.mostrar_pedidos()
            self.mostrar_productos()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # MODIFICAR PEDIDO
    # ---------------------------------------------------------
    def modificar_pedido(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccionar", "Selecciona un pedido.")
            return

        valores = self.tabla.item(seleccionado)["values"]
        id_pedido = valores[0]

        ventana_mod = tk.Toplevel(self.master)
        ventana_mod.title(f"Modificar Pedido ID {id_pedido}")
        ventana_mod.geometry("450x500")
        ventana_mod.config(bg=self.color_fondo)

        campos = [
            ("Cliente:", "cliente", valores[1]),
            ("Producto:", "producto", valores[2]),
            ("Cantidad:", "cantidad", valores[3]),
            ("Precio unidad:", "precio", valores[4]),
            ("Anticipo:", "anticipo", valores[5]),
            ("Fecha entrega (DD-MM-YYYY):", "fecha", valores[8]),
            ("Estado:", "estado", valores[9])
        ]

        self.edit_entries = {}
        nombres_productos = list(self.productos_dict.keys())

        for i, (texto, key, valor) in enumerate(campos):
            tk.Label(ventana_mod, text=texto, bg=self.color_fondo, fg=self.color_texto)\
                .grid(row=i, column=0, padx=5, pady=5, sticky="e")

            if key == "producto":
                cmb = ttk.Combobox(ventana_mod, values=nombres_productos, state="readonly")
                cmb.set(valor)
                self.edit_entries[key] = cmb
            else:
                ent = tk.Entry(ventana_mod)
                ent.insert(0, valor)
                self.edit_entries[key] = ent

            self.edit_entries[key].grid(row=i, column=1, padx=5, pady=5)

        # Determinar rol
        rol = self._inferir_rol()

        # ---------------- BLOQUEO (RESPETANDO TU LÓGICA ORIGINAL) ----------------
        # Según nos dijiste varias veces: cliente, producto, precio, anticipo y estado
        # deben quedarse bloqueados como los tenías. Solo cantidad y fecha son editables
        # para Administrador y Empleado; Invitado no puede editar nada.
        try:
            # Bloqueados siempre (tal como estaban en tu UI de ejemplo)
            try:
                self.edit_entries["cliente"].config(state="disabled")
            except:
                pass
            try:
                # combobox -> config state, Entry -> config state
                if isinstance(self.edit_entries["producto"], ttk.Combobox):
                    self.edit_entries["producto"].config(state="disabled")
                else:
                    self.edit_entries["producto"].config(state="disabled")
            except:
                pass
            try:
                self.edit_entries["precio"].config(state="disabled")
            except:
                pass
            try:
                self.edit_entries["anticipo"].config(state="disabled")
            except:
                pass
            try:
                self.edit_entries["estado"].config(state="disabled")
            except:
                pass

            # Cantidad y Fecha según rol
            if rol in ("Administrador", "Empleado"):
                try:
                    self.edit_entries["cantidad"].config(state="normal")
                except:
                    pass
                try:
                    self.edit_entries["fecha"].config(state="normal")
                except:
                    pass
            else:
                # Invitado: todo bloqueado (ya están bloqueados arriba)
                try:
                    self.edit_entries["cantidad"].config(state="disabled")
                except:
                    pass
                try:
                    self.edit_entries["fecha"].config(state="disabled")
                except:
                    pass
        except Exception:
            # si falla algo, no romper la ventana
            pass
        # -------------------------------------------------------------------------

        tk.Button(
            ventana_mod, text="Guardar Cambios", width=30,
            bg="lightgreen", fg="black",
            command=lambda: self.guardar_cambios_pedido(id_pedido, ventana_mod)
        ).grid(row=10, column=0, columnspan=2, pady=20)

        tk.Button(
            ventana_mod, text="Agregar Abono / Anticipo", width=30,
            bg="#FFEB99", fg="black",
            command=lambda: self.abrir_ventana_abono(id_pedido)
        ).grid(row=11, column=0, columnspan=2, pady=8)

    # ---------------------------------------------------------
    # GUARDAR CAMBIOS PEDIDO
    # ---------------------------------------------------------
    def guardar_cambios_pedido(self, id_pedido, ventana):
        try:
            datos = {k: e.get().strip() for k, e in self.edit_entries.items()}
            fecha_guardar = datetime.strptime(datos["fecha"], "%d-%m-%Y").strftime("%Y-%m-%d")

            # Lo que ingresa el usuario en el campo "cantidad" (se interpreta como cantidad a agregar)
            try:
                entrada_cantidad = float(datos["cantidad"])
            except Exception:
                messagebox.showwarning("Error", "Cantidad inválida.")
                return

            try:
                precio = float(datos["precio"])
            except Exception:
                messagebox.showwarning("Error", "Precio inválido.")
                return

            # anticipo: puede venir vacío o con valor
            try:
                anticipo = float(datos["anticipo"]) if datos["anticipo"] != "" else None
            except Exception:
                messagebox.showwarning("Error", "Anticipo inválido.")
                return

            producto_nombre = datos["producto"]
            if producto_nombre not in self.productos_dict:
                messagebox.showerror("Error", "Producto no encontrado.")
                return
            id_producto = self.productos_dict[producto_nombre]

            conn = crear_conexion()
            cursor = conn.cursor()

            # cantidad original en pedido
            cursor.execute("SELECT cantidad, anticipo FROM pedidos WHERE id_pedido=%s", (id_pedido,))
            fila = cursor.fetchone()
            if not fila:
                messagebox.showerror("Error", "No se encontró la cantidad original del pedido.")
                conn.close()
                return
            cantidad_original = float(fila[0])
            anticipo_original = float(fila[1]) if fila[1] is not None else 0.0

            # stock actual en productos (ya descontado por pedidos previos)
            cursor.execute("SELECT stock FROM productos WHERE id_producto=%s", (id_producto,))
            stock_row = cursor.fetchone()
            if not stock_row:
                messagebox.showerror("Error", "No se encontró el producto en inventario.")
                conn.close()
                return
            stock_actual = float(stock_row[0])

            # ---------------------------
            #  🔥 LÓGICA: SIEMPRE SUMA LA ENTRADA
            # ---------------------------
            # Interpretamos lo que el usuario escribió como "cantidad a agregar".
            # cantidad_final = cantidad_original + entrada_cantidad
            # diferencia = entrada_cantidad (lo que se descontará del stock)

            cantidad_final = cantidad_original + entrada_cantidad
            diferencia = entrada_cantidad

            # Verificar stock suficiente para la diferencia (si aumentamos)
            if diferencia > 0 and stock_actual < diferencia:
                messagebox.showwarning("Stock insuficiente", f"No hay suficiente stock para aumentar. Disponibles: {stock_actual}")
                conn.close()
                return

            # calcular nuevo stock
            stock_nuevo = stock_actual - diferencia

            # recalcular totales con la cantidad_final
            total_final = cantidad_final * precio

            # Si el usuario dejó el campo anticipo vacío, conservar el anticipo anterior
            if anticipo is None:
                anticipo = anticipo_original

            # --- Validación: anticipo no puede ser mayor que el total_final ---
            if anticipo > total_final:
                conn.close()
                messagebox.showwarning("Error en anticipo", f"El anticipo no puede ser mayor que el total.\n\nTotal: {total_final:.2f}\nAnticipo ingresado: {anticipo:.2f}")
                return

            # recalcular restante según nuevo total y anticipo
            restante_final = total_final - anticipo
            estado_final = "Pagado" if restante_final <= 0 else datos["estado"]

            # Confirmación al usuario mostrando la operación real
            if not messagebox.askyesno("Confirmación",
                                       f"Cantidad original: {cantidad_original}\n"
                                       f"Cantidad agregada: {entrada_cantidad}\n"
                                       f"Cantidad final: {cantidad_final}\n"
                                       f"Stock actual: {stock_actual}\n"
                                       f"Stock nuevo: {stock_nuevo}\n\n¿Continuar?"):
                conn.close()
                return

            # Aplicar cambios en productos y pedido
            cursor.execute("UPDATE productos SET stock=%s WHERE id_producto=%s",
                           (stock_nuevo, id_producto))

            cursor.execute("""
                UPDATE pedidos SET cliente=%s, producto=%s, nombre_producto=%s,
                    cantidad=%s, precio=%s, anticipo=%s, total=%s,
                    restante=%s, fecha_entrega=%s, estado=%s, actualizado_por=%s
                WHERE id_pedido=%s
            """, (
                datos["cliente"], id_producto, producto_nombre, cantidad_final,
                precio, anticipo, total_final, restante_final, fecha_guardar,
                estado_final, self.usuario_actual, id_pedido
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Actualizado", "Pedido modificado correctamente.")
            ventana.destroy()
            self.mostrar_pedidos()
            self.mostrar_productos()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # ABONOS — (GUARDAR ABONO Y GENERAR TICKET) CORREGIDO
    # ---------------------------------------------------------
    def abrir_ventana_abono(self, id_pedido):

        conn = crear_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cliente, nombre_producto, anticipo, total, restante
            FROM pedidos WHERE id_pedido=%s
        """, (id_pedido,))
        pedido = cursor.fetchone()
        conn.close()

        if not pedido:
            messagebox.showerror("Error", "No se encontró el pedido.")
            return

        cliente, nombre_producto, anticipo_actual, total, restante_actual = pedido

        # convertir a Decimal para cálculos seguros
        anticipo_actual = Decimal(str(anticipo_actual))
        total = Decimal(str(total))
        restante_actual = Decimal(str(restante_actual))

        ventana_abono = tk.Toplevel(self.master)
        ventana_abono.title(f"Agregar Abono al Pedido {id_pedido}")
        ventana_abono.geometry("420x420")
        ventana_abono.config(bg=self.color_fondo)

        tk.Label(ventana_abono,
                 text=f"Cliente: {cliente}",
                 bg=self.color_fondo,
                 font=("Arial", 12, "bold")
        ).pack(pady=5)

        info = (
            f"Producto: {nombre_producto}\n"
            f"Total: ${total}\n"
            f"Anticipo actual: ${anticipo_actual}\n"
            f"Restante actual: ${restante_actual}\n"
        )

        tk.Label(ventana_abono, text=info, bg=self.color_fondo, justify="left").pack(pady=10)

        tk.Label(ventana_abono, text="Nuevo abono:", bg=self.color_fondo).pack()
        entry_abono = tk.Entry(ventana_abono)
        entry_abono.pack(pady=5)

        # variable local para retener datos del último abono guardado en esta ventana
        ultimo_abono_registrado = {"monto": None, "anticipo": None, "restante": None, "estado": None}

        # --------------------------- FUNCIÓN PDF --------------------------
        def generar_ticket_pdf():
            # requiere que exista un abono guardado antes de generar
            if ultimo_abono_registrado["monto"] is None:
                messagebox.showwarning("Sin abono", "Primero guarda el abono (botón 'Guardar Abono') antes de generar el ticket.")
                return

            try:
                carpeta = "tickets"
                if not os.path.exists(carpeta):
                    os.makedirs(carpeta)

                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_pdf = f"ticket_abono_{id_pedido}_{ts}.pdf"
                ruta_pdf = os.path.join(carpeta, nombre_pdf)

                styles = getSampleStyleSheet()
                story = []

                story.append(Paragraph("RECIBO DE ABONO", styles["Title"]))
                story.append(Spacer(1, 12))

                story.append(Paragraph(f"Pedido ID: {id_pedido}", styles["Normal"]))
                story.append(Paragraph(f"Cliente: {cliente}", styles["Normal"]))
                story.append(Paragraph(f"Producto: {nombre_producto}", styles["Normal"]))
                story.append(Spacer(1, 8))

                story.append(Paragraph(f"Total pedido: ${total}", styles["Normal"]))
                story.append(Paragraph(f"Anticipo anterior: ${anticipo_actual}", styles["Normal"]))

                monto = ultimo_abono_registrado["monto"]
                antic = ultimo_abono_registrado["anticipo"]
                rest = ultimo_abono_registrado["restante"]
                estado = ultimo_abono_registrado["estado"]

                story.append(Paragraph(f"Nuevo abono: ${monto}", styles["Normal"]))
                story.append(Paragraph(f"Anticipo nuevo: ${antic}", styles["Normal"]))
                story.append(Paragraph(f"Restante: ${rest}", styles["Normal"]))
                story.append(Spacer(1, 12))

                story.append(Paragraph(f"Estado del pedido: {estado}", styles["Normal"]))
                story.append(Spacer(1, 12))
                story.append(Paragraph(f"Generado por: {self.usuario_actual}", styles["Normal"]))
                story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles["Normal"]))

                doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
                doc.build(story)

                messagebox.showinfo("Ticket generado", f"Ticket PDF creado:\n{ruta_pdf}")

            except Exception as e:
                messagebox.showerror("Error al generar ticket", str(e))

        # -------------------------- GUARDAR ABONO -------------------------
        def guardar_abono():
            try:
                nuevo_abono_str = entry_abono.get().strip()
                if not nuevo_abono_str:
                    messagebox.showwarning("Campo vacío", "Ingresa el monto del abono.")
                    return

                try:
                    nuevo_abono = Decimal(nuevo_abono_str)
                except:
                    messagebox.showerror("Error", "Ingresa un número válido.")
                    return

                if nuevo_abono <= 0:
                    messagebox.showwarning("Error", "El abono debe ser mayor a 0.")
                    return

                # NO permitir abonar más de lo que resta
                if nuevo_abono > restante_actual:
                    messagebox.showwarning("Error", f"No puedes abonar más del restante ({restante_actual}).")
                    return

                anticipo_final = anticipo_actual + nuevo_abono
                restante_final = total - anticipo_final

                if restante_final <= 0:
                    restante_final = Decimal("0.00")
                    anticipo_final = total
                    nuevo_estado = "Pagado"
                else:
                    nuevo_estado = "Pendiente"

                conn2 = crear_conexion()
                cursor2 = conn2.cursor()

                cursor2.execute("""
                    UPDATE pedidos
                    SET anticipo=%s, restante=%s, estado=%s, actualizado_por=%s
                    WHERE id_pedido=%s
                """, (
                    float(anticipo_final),
                    float(restante_final),
                    nuevo_estado,
                    self.usuario_actual,
                    id_pedido
                ))

                conn2.commit()
                conn2.close()

                # Guardar los datos del último abono en memoria (para el botón Generar Ticket)
                ultimo_abono_registrado["monto"] = f"{nuevo_abono:.2f}"
                ultimo_abono_registrado["anticipo"] = f"{anticipo_final:.2f}"
                ultimo_abono_registrado["restante"] = f"{restante_final:.2f}"
                ultimo_abono_registrado["estado"] = nuevo_estado

                messagebox.showinfo("Abono guardado",
                                    f"Abono añadido correctamente.\n"
                                    f"Anticipo nuevo: ${ultimo_abono_registrado['anticipo']}\n"
                                    f"Restante: ${ultimo_abono_registrado['restante']}\n"
                                    f"Estado: {nuevo_estado}")

                # Actualiza la tabla principal
                self.mostrar_pedidos()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        # BOTONES
        tk.Button(
            ventana_abono,
            text="Guardar Abono",
            bg="#90EE90",
            fg="black",
            width=28,
            command=guardar_abono
        ).pack(pady=8)

        tk.Button(
            ventana_abono,
            text="Generar Ticket",
            bg="#FFD27F",
            fg="black",
            width=28,
            command=generar_ticket_pdf
        ).pack(pady=8)

    # ---------------------------------------------------------
    # ELIMINAR PEDIDO
    # ---------------------------------------------------------
    def eliminar_pedido(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Selecciona", "Selecciona un pedido.")
            return

        valores = self.tabla.item(seleccionado)["values"]
        id_pedido = valores[0]
        cantidad = float(valores[3])
        producto_nombre = valores[2]

        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que deseas eliminar el pedido ID {id_pedido}?"):
            return

        try:
            id_producto = self.productos_dict[producto_nombre]

            conn = crear_conexion()
            cursor = conn.cursor()

            cursor.execute("SELECT stock FROM productos WHERE id_producto=%s", (id_producto,))
            stock_actual = float(cursor.fetchone()[0])

            stock_nuevo = stock_actual + cantidad

            cursor.execute("UPDATE productos SET stock=%s WHERE id_producto=%s",
                           (stock_nuevo, id_producto))

            cursor.execute("DELETE FROM pedidos WHERE id_pedido=%s", (id_pedido,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Eliminado", "Pedido eliminado correctamente.")

            self.mostrar_pedidos()
            self.mostrar_productos()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # REGRESAR
    # ---------------------------------------------------------
    def regresar_menu(self):
        if self.regresar_callback:
            self.regresar_callback()
        self.master.destroy()
