import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import csv
from abc import ABC, abstractmethod

# ========== CONFIGURATION LOADER ============
def cargar_configuracion():
    parametros = {}
    with open("config.txt", "r") as archivo:
        for linea in archivo:
            clave, valor = linea.strip().split("=")
            parametros[clave] = valor
    return parametros

# ========== ENTITY ===========================
class Doctor:
    def __init__(self, nombre, especialidad, cedula):
        self.nombre = nombre
        self.especialidad = especialidad
        self.cedula = cedula

# ========== REPOSITORY INTERFACE ============
class RepositorioDoctores(ABC):
    @abstractmethod
    def agregar(self, doctor): pass

    @abstractmethod
    def actualizar(self, cedula, doctor): pass

    @abstractmethod
    def eliminar(self, cedula): pass

    @abstractmethod
    def obtener_todos(self): pass

    @abstractmethod
    def existe_cedula(self, cedula): pass

# ========== MYSQL IMPLEMENTATION ============
class RepositorioMySQL(RepositorioDoctores):
    def __init__(self, config):
        self.conexion = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"]
        )
        self.cursor = self.conexion.cursor()
        self.crear_tabla_si_no_existe()

    def crear_tabla_si_no_existe(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctores (
                cedula VARCHAR(20) PRIMARY KEY,
                nombre VARCHAR(100),
                especialidad VARCHAR(100)
            )
        """)
        self.conexion.commit()

    def agregar(self, doctor):
        self.cursor.execute(
            "INSERT INTO doctores (cedula, nombre, especialidad) VALUES (%s, %s, %s)",
            (doctor.cedula, doctor.nombre, doctor.especialidad)
        )
        self.conexion.commit()

    def actualizar(self, cedula, doctor):
        self.cursor.execute("SELECT cedula FROM doctores WHERE cedula = %s", (cedula,))
        if not self.cursor.fetchone():
            raise ValueError("No existe un registro con esa cédula.")
        self.cursor.execute(
            "UPDATE doctores SET nombre = %s, especialidad = %s WHERE cedula = %s",
            (doctor.nombre, doctor.especialidad, cedula)
        )
        self.conexion.commit()

    def eliminar(self, cedula):
        self.cursor.execute("DELETE FROM doctores WHERE cedula = %s", (cedula,))
        self.conexion.commit()

    def obtener_todos(self):
        self.cursor.execute("SELECT nombre, especialidad, cedula FROM doctores")
        registros = self.cursor.fetchall()
        return [Doctor(nombre, especialidad, cedula) for nombre, especialidad, cedula in registros]

    def existe_cedula(self, cedula):
        self.cursor.execute("SELECT 1 FROM doctores WHERE cedula = %s", (cedula,))
        return self.cursor.fetchone() is not None

# ========== TKINTER GUI ======================
class AplicacionDoctores(tk.Tk):
    def __init__(self, repositorio):
        super().__init__()
        self.repositorio = repositorio
        self.title("Gestión de Doctores")
        self.geometry("520x550")

        self.nombre_var = tk.StringVar()
        self.especialidad_var = tk.StringVar()
        self.cedula_var = tk.StringVar()

        # Formulario
        tk.Label(self, text="Nombre").pack()
        tk.Entry(self, textvariable=self.nombre_var).pack()
        tk.Label(self, text="Especialidad").pack()
        tk.Entry(self, textvariable=self.especialidad_var).pack()
        tk.Label(self, text="Cédula").pack()
        self.cedula_entry = tk.Entry(self, textvariable=self.cedula_var)
        self.cedula_entry.pack()

        # Botones
        tk.Button(self, text="Agregar Doctor", command=self.agregar_doctor).pack(pady=2)
        tk.Button(self, text="Actualizar Doctor", command=self.actualizar_doctor).pack(pady=2)
        tk.Button(self, text="Eliminar Doctor", command=self.eliminar_doctor).pack(pady=2)
        tk.Button(self, text="Refrescar Tabla", command=self.mostrar_todos).pack(pady=2)
        tk.Button(self, text="Exportar CSV", command=self.exportar_csv).pack(pady=2)

        # Buscador
        tk.Label(self, text="Buscar").pack()
        self.buscar_var = tk.StringVar()
        self.buscar_entry = tk.Entry(self, textvariable=self.buscar_var)
        self.buscar_entry.pack()
        self.buscar_entry.bind("<KeyRelease>", self.buscar_doctores)

        # Tabla
        columnas = ("nombre", "especialidad", "cedula")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
        self.tabla.pack(fill=tk.BOTH, expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.mostrar_todos()

    def limpiar_campos(self):
        self.nombre_var.set("")
        self.especialidad_var.set("")
        self.cedula_var.set("")
        self.cedula_entry.config(state="normal")

    def agregar_doctor(self):
        doctor = Doctor(self.nombre_var.get(), self.especialidad_var.get(), self.cedula_var.get())
        if not doctor.nombre or not doctor.especialidad or not doctor.cedula:
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
            return
        if self.repositorio.existe_cedula(doctor.cedula):
            messagebox.showerror("Error", "Ya existe un doctor con esa cédula.")
            return
        try:
            self.repositorio.agregar(doctor)
            messagebox.showinfo("Agregado", "Doctor agregado correctamente.")
            self.limpiar_campos()
            self.mostrar_todos()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))

    def actualizar_doctor(self):
        doctor = Doctor(self.nombre_var.get(), self.especialidad_var.get(), self.cedula_var.get())
        if not doctor.nombre or not doctor.especialidad or not doctor.cedula:
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
            return
        try:
            self.repositorio.actualizar(doctor.cedula, doctor)
            messagebox.showinfo("Actualizado", "Doctor actualizado correctamente.")
            self.limpiar_campos()
            self.mostrar_todos()
        except ValueError as ve:
            messagebox.showwarning("Advertencia", str(ve))
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))

    def eliminar_doctor(self):
        cedula = self.cedula_var.get()
        if not cedula:
            messagebox.showwarning("Cédula vacía", "Selecciona o escribe una cédula válida.")
            return
        try:
            self.repositorio.eliminar(cedula)
            messagebox.showinfo("Eliminado", "Doctor eliminado correctamente.")
            self.limpiar_campos()
            self.mostrar_todos()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))

    def mostrar_todos(self):
        self.tabla.delete(*self.tabla.get_children())
        for doctor in self.repositorio.obtener_todos():
            self.tabla.insert("", "end", values=(doctor.nombre, doctor.especialidad, doctor.cedula))

    def seleccionar_fila(self, event):
        seleccion = self.tabla.focus()
        if seleccion:
            valores = self.tabla.item(seleccion, "values")
            self.nombre_var.set(valores[0])
            self.especialidad_var.set(valores[1])
            self.cedula_var.set(valores[2])
            self.cedula_entry.config(state="disabled")

    def buscar_doctores(self, event):
        termino = self.buscar_var.get().lower()
        doctores = self.repositorio.obtener_todos()
        filtrados = [d for d in doctores if termino in d.nombre.lower() or termino in d.especialidad.lower() or termino in d.cedula.lower()]

        self.tabla.delete(*self.tabla.get_children())
        for doctor in filtrados:
            self.tabla.insert("", "end", values=(doctor.nombre, doctor.especialidad, doctor.cedula))

    def exportar_csv(self):
        doctores = self.repositorio.obtener_todos()
        try:
            with open("doctores.csv", "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(["Nombre", "Especialidad", "Cédula"])
                for d in doctores:
                    escritor.writerow([d.nombre, d.especialidad, d.cedula])
            messagebox.showinfo("Exportado", "Archivo CSV generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# ========== MAIN ============================
if __name__ == "__main__":
    config = cargar_configuracion()
    repositorio = RepositorioMySQL(config)
    app = AplicacionDoctores(repositorio)
    app.mainloop()
