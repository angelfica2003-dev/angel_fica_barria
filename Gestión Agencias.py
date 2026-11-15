import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class AgenciaEspacialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Agencias Espaciales")
        self.root.geometry("650x500")

        # Configuración de credenciales de conexión
        self.config = {
            'host': 'localhost',
            'port': 3307,
            'user': 'root',
            'password': '',
            'database': 'agencias_db'
        }

        # --- CAMPOS DE ENTRADA (FORMULARIO) ---
        frame_form = tk.LabelFrame(root, text=" Datos de la Agencia ", padx=10, pady=10)
        frame_form.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="e", pady=2)
        self.entry_id = tk.Entry(frame_form)
        self.entry_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="e", pady=2)
        self.entry_nombre = tk.Entry(frame_form, width=40)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="País:").grid(row=2, column=0, sticky="e", pady=2)
        self.entry_pais = tk.Entry(frame_form, width=30)
        self.entry_pais.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Fecha Creación (AAAA-MM-DD):").grid(row=3, column=0, sticky="e", pady=2)
        self.entry_fecha = tk.Entry(frame_form, width=20)
        self.entry_fecha.grid(row=3, column=1, padx=5, pady=2)

        # --- BOTONES DE OPERACIÓN (CRUD) ---
        frame_btn = tk.Frame(root)
        frame_btn.pack(pady=5)

        tk.Button(frame_btn, text="Agregar", command=self.agregar, bg="#4CAF50", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Mostrar", command=self.mostrar, bg="#2196F3", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Actualizar", command=self.actualizar, bg="#FF9800", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Borrar", command=self.borrar, bg="#f44336", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Limpiar", command=self.limpiar_campos, width=10).pack(side="left", padx=5)

        # --- TABLA DE DATOS (TREEVIEW) ---
        frame_tabla = tk.Frame(root)
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        self.tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Pais", "Fecha"), show="headings")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Pais", text="País")
        self.tabla.heading("Fecha", text="Fecha Creación")

        self.tabla.column("ID", width=40, anchor="center")
        self.tabla.column("Nombre", width=250)
        self.tabla.column("Pais", width=120)
        self.tabla.column("Fecha", width=100, anchor="center")

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)

        # Cargar datos al iniciar
        self.mostrar()

    def obtener_conexion(self):
        return mysql.connector.connect(**self.config)

    # C = CREATE (Agregar)
    def agregar(self):
        id_agencia = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        pais = self.entry_pais.get().strip()
        fecha = self.entry_fecha.get().strip()

        if not (id_agencia and nombre and pais and fecha):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios")
            return

        try:
            conn = self.obtener_conexion()
            cursor = conn.cursor()
            # Se usa fecha_Creacion en lugar de FechaCreacion
            sql = "INSERT INTO AgenciaEspacial (id, nombre, pais, fecha_Creacion) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_agencia, nombre, pais, fecha))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Agencia registrada correctamente")
            self.limpiar_campos()
            self.mostrar()
        except mysql.connector.Error as err:
            messagebox.showerror("Error SQL", f"No se pudo guardar: {err}")

    # R = READ (Mostrar)
    def mostrar(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        try:
            conn = self.obtener_conexion()
            cursor = conn.cursor()
            # Se usa fecha_Creacion en lugar de FechaCreacion
            cursor.execute("SELECT id, nombre, pais, fecha_Creacion FROM AgenciaEspacial")
            registros = cursor.fetchall()
            for reg in registros:
                self.tabla.insert("", "end", values=reg)
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error SQL", f"Error al cargar datos: {err}")

    # U = UPDATE (Actualizar)
    def actualizar(self):
        id_agencia = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        pais = self.entry_pais.get().strip()
        fecha = self.entry_fecha.get().strip()

        if not id_agencia:
            messagebox.showwarning("Atención", "Selecciona una agencia de la tabla o ingresa el ID")
            return

        try:
            conn = self.obtener_conexion()
            cursor = conn.cursor()
            # Se usa fecha_Creacion en lugar de FechaCreacion
            sql = "UPDATE AgenciaEspacial SET nombre=%s, pais=%s, fecha_Creacion=%s WHERE id=%s"
            cursor.execute(sql, (nombre, pais, fecha, id_agencia))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Agencia actualizada correctamente")
            self.limpiar_campos()
            self.mostrar()
        except mysql.connector.Error as err:
            messagebox.showerror("Error SQL", f"Error al actualizar: {err}")

    # D = DELETE (Borrar con confirmación)
    def borrar(self):
        id_agencia = self.entry_id.get().strip()
        if not id_agencia:
            messagebox.showwarning("Atención", "Selecciona una agencia de la tabla para borrar")
            return

        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de eliminar la agencia con ID {id_agencia}?")
        if confirmar:
            try:
                conn = self.obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM AgenciaEspacial WHERE id=%s", (id_agencia,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Éxito", "Agencia eliminada correctamente")
                self.limpiar_campos()
                self.mostrar()
            except mysql.connector.Error as err:
                messagebox.showerror("Error SQL", f"Error al borrar: {err}")

    def seleccionar_registro(self, event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.limpiar_campos()
            self.entry_id.insert(0, valores[0])
            self.entry_id.config(state="disabled")
            self.entry_nombre.insert(0, valores[1])
            self.entry_pais.insert(0, valores[2])
            self.entry_fecha.insert(0, valores[3])

    def limpiar_campos(self):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_pais.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AgenciaEspacialApp(root)
    root.mainloop()