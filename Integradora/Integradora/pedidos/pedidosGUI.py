import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from conexionBD import crear_conexion


class PedidosGUI:
    def __init__(self, master=None, regresar_callback=None):
        self.master = tk.Toplevel(master)
        self.master.title("Gestión de Pedidos")
        self.master.geometry("1300x1000")

        # 🎨 COLORES
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

        frame = tk.Frame(self.master, bg=self.color_fondo)
        frame.pack(pady=10)

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

        for i, (texto, key) in enumerate(campos):
            tk.Label(frame, text=texto, bg=self.color_fondo, fg=self.color_texto)\
                .grid(row=i, column=0, padx=5, pady=5, sticky="e")
            self.entries[key] = tk.Entry(frame)
            self.entries[key].grid(row=i, column=1, padx=5, pady=5)

        self.entries["estado"].insert(0, "Pendiente")

        tk.Button(
            self.master, text="Registrar Pedido", width=30,
            bg=self.color_boton, fg=self.color_texto,
            command=self.registrar_pedido
        ).pack(pady=10)

        tk.Button(
            self.master, text="Regresar al Menú Principal", width=30,
            bg=self.color_boton, fg=self.color_texto,
            command=self.regresar_menu
        ).pack(pady=5)

        columnas = ("ID", "Cliente", "Producto", "Cantidad", "Precio",
                    "Anticipo", "Total", "Restante",
                    "Fecha Entrega", "Estado")

        self.tabla = ttk.Treeview(self.master, columns=columnas, show="headings", height=12)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)

        self.tabla.pack(pady=10, fill="both", expand=True)

        tk.Button(
            self.master, text="Modificar Pedido Seleccionado", width=30,
            bg=self.color_boton, fg=self.color_texto,
            command=self.modificar_pedido
        ).pack(pady=5)

        tk.Button(
            self.master, text="Eliminar Pedido Seleccionado", width=30,
            bg=self.color_boton, fg=self.color_texto,
            command=self.eliminar_pedido
        ).pack(pady=5)

        self.mostrar_pedidos()


    def registrar_pedido(self):
        datos = {key: entry.get().strip() for key, entry in self.entries.items()}

        if any(not x for x in datos.values()):
            messagebox.showwarning("⚠️ Campos vacíos", "Todos los campos son obligatorios.")
            return

        try:
            fecha_guardar = datetime.strptime(datos["fecha"], "%d-%m-%Y").strftime("%Y-%m-%d")

            cantidad = float(datos["cantidad"])
            precio = float(datos["precio"])
            anticipo = float(datos["anticipo"])

            total = cantidad * precio
            restante = total - anticipo

            estado_final = "Pagado" if restante <= 0 else datos["estado"]

            conexion = crear_conexion()
            cursor = conexion.cursor()

            # 🔥 VALIDAR STOCK
            cursor.execute("SELECT stock FROM productos WHERE nombre = %s", (datos["producto"],))
            res = cursor.fetchone()

            if not res:
                messagebox.showerror("❌ Error", "El producto no existe.")
                conexion.close()
                return

            stock_actual = float(res[0])

            if cantidad > stock_actual:
                messagebox.showwarning(
                    "❌ Stock insuficiente",
                    f"Solo hay {stock_actual} unidades disponibles."
                )
                conexion.close()
                return

            nuevo_stock = stock_actual - cantidad

            cursor.execute(
                "UPDATE productos SET stock=%s WHERE nombre=%s",
                (nuevo_stock, datos["producto"])
            )

            # 🧾 GUARDAR PEDIDO
            cursor.execute("""
                INSERT INTO pedidos (cliente, producto, cantidad, precio, anticipo,
                                     total, restante, fecha_entrega, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (datos["cliente"], datos["producto"], cantidad, precio,
                  anticipo, total, restante, fecha_guardar, estado_final))

            conexion.commit()
            conexion.close()

            messagebox.showinfo("💰 Pedido Registrado",
                                f"Total: ${total:.2f}\n"
                                f"Anticipo: ${anticipo:.2f}\n"
                                f"Restante: ${restante:.2f}\n"
                                f"Nuevo stock: {nuevo_stock}")

            self.mostrar_pedidos()

            for entry in self.entries.values():
                entry.delete(0, tk.END)

            self.entries["estado"].insert(0, "Pendiente")

        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al registrar pedido:\n{e}")


    def mostrar_pedidos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_pedido, cliente, producto, cantidad, precio,
                   anticipo, total, restante,
                   DATE_FORMAT(fecha_entrega, '%d-%m-%Y'), estado
            FROM pedidos
        """)
        pedidos = cursor.fetchall()
        conexion.close()

        for pedido in pedidos:
            self.tabla.insert("", tk.END, values=pedido)


    def modificar_pedido(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("⚠️ Selección requerida", "Selecciona un pedido.")
            return

        datos = self.tabla.item(seleccionado)["values"]
        id_pedido = datos[0]

        ventana = tk.Toplevel(self.master)
        ventana.title("Modificar Pedido")
        ventana.geometry("400x500")
        ventana.config(bg=self.color_fondo)

        labels = ["Cliente", "Producto", "Cantidad", "Precio", "Anticipo", "Fecha (DD-MM-YYYY)", "Estado"]
        campos = {}
        valores_actuales = [
            datos[1], datos[2], datos[3], datos[4], datos[5],
            datos[8], datos[9]
        ]

        for i, (label, valor) in enumerate(zip(labels, valores_actuales)):
            tk.Label(ventana, text=label, bg=self.color_fondo, fg=self.color_texto)\
                .grid(row=i, column=0, padx=10, pady=5)
            entrada = tk.Entry(ventana)
            entrada.grid(row=i, column=1)
            entrada.insert(0, valor)
            campos[label] = entrada

        def guardar_cambios():
            try:
                cliente = campos["Cliente"].get()
                producto = campos["Producto"].get()
                cantidad = float(campos["Cantidad"].get())
                precio = float(campos["Precio"].get())
                anticipo = float(campos["Anticipo"].get())
                fecha = campos["Fecha (DD-MM-YYYY)"].get()
                estado = campos["Estado"].get()

                fecha_sql = datetime.strptime(fecha, "%d-%m-%Y").strftime("%Y-%m-%d")

                total = cantidad * precio
                restante = total - anticipo

                estado_final = "Pagado" if restante <= 0 else estado

                conexion = crear_conexion()
                cursor = conexion.cursor()

                cursor.execute("""
                    UPDATE pedidos 
                    SET cliente=%s, producto=%s, cantidad=%s, precio=%s,
                        anticipo=%s, total=%s, restante=%s, fecha_entrega=%s, estado=%s
                    WHERE id_pedido=%s
                """, (cliente, producto, cantidad, precio, anticipo,
                      total, restante, fecha_sql, estado_final, id_pedido))

                conexion.commit()
                conexion.close()

                messagebox.showinfo("✔️ Modificado", "Pedido actualizado correctamente.")
                ventana.destroy()
                self.mostrar_pedidos()

            except Exception as e:
                messagebox.showerror("❌ Error", f"No se pudo modificar:\n{e}")

        tk.Button(
            ventana, text="Guardar Cambios",
            bg=self.color_boton, fg=self.color_texto,
            command=guardar_cambios
        ).grid(row=10, column=0, columnspan=2, pady=20)


    def eliminar_pedido(self):
        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning("⚠️ Selección requerida", "Seleccione un pedido.")
            return

        id_pedido = self.tabla.item(seleccionado)["values"][0]

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id_pedido = %s", (id_pedido,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("🗑️ Eliminado", "Pedido eliminado correctamente.")
        self.mostrar_pedidos()


    def regresar_menu(self):
        self.master.destroy()
        if self.regresar_callback:
            self.regresar_callback()
