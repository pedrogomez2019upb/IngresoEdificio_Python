import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class TarjetaFormulario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Agregar Tarjeta")

        self.etiqueta_usuario = tk.Label(self, text="Usuario:")
        self.etiqueta_usuario.grid(row=0, column=0, padx=5, pady=5)

        self.usuario = tk.StringVar(self)
        self.menu_usuario = tk.OptionMenu(self, self.usuario, *obtener_usuarios())
        self.menu_usuario.grid(row=0, column=1, padx=5, pady=5)

        self.etiqueta_numero = tk.Label(self, text="Número de Tarjeta:")
        self.etiqueta_numero.grid(row=1, column=0, padx=5, pady=5)

        self.numero = tk.Entry(self)
        self.numero.grid(row=1, column=1, padx=5, pady=5)

        self.boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_tarjeta)
        self.boton_guardar.grid(row=2, column=1, padx=5, pady=5)

    def guardar_tarjeta(self):
        print(self.usuario.get())
        print("Hola")
        if not self.usuario.get() or not self.numero.get():
            messagebox.showerror("Error", "Por favor, complete todos los campos")
        else:
            print(self.usuario.get())
            insertar_tarjeta(self.usuario.get(), self.numero.get())
            messagebox.showerror("Tarjeta Agregada", "Se guardó exitosamente la tarjeta")
            self.destroy(TarjetaFormulario)


class AccesoFormulario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Validar Tarjeta")

        self.etiqueta_numero = tk.Label(self, text="Número de Tarjeta:")
        self.etiqueta_numero.grid(row=0, column=0, padx=5, pady=5)

        self.numero = tk.Entry(self)
        self.numero.grid(row=0, column=1, padx=5, pady=5)

        self.boton_validar = tk.Button(self, text="Validar", command=self.validar_tarjeta)
        self.boton_validar.grid(row=1, column=1, padx=5, pady=5)

    def validar_tarjeta(self):
        numero = self.numero.get()
        if not numero:
            messagebox.showerror("Error", "Por favor, ingrese el número de tarjeta")
        else:
            usuario = obtener_usuario_por_tarjeta(numero)
            if usuario:
                messagebox.showinfo("Bienvenido", "Bienvenido {usuario[1]} {usuario[2]}")
            else:
                messagebox.showerror("Error", "Tarjeta no válida")
        self.numero.delete(0, tk.END)


def crear_tablas():
    conn = sqlite3.connect("acceso.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        identificacion TEXT UNIQUE,
        nombre TEXT,
        apellido TEXT
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS tarjetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        numero TEXT UNIQUE,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )""")
    conn.commit()
    conn.close()


def insertar_usuario(identificacion, nombre, apellido):
    conn = sqlite3.connect("acceso.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (identificacion, nombre, apellido) VALUES (?, ?, ?)", (identificacion, nombre, apellido))
    usuario_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return usuario_id
def obtener_usuarios():
    conn = sqlite3.connect("acceso.db")
    cursor = conn.cursor()
    cursor.execute("SELECT identificacion, nombre, apellido FROM usuarios")
    usuarios = [(f"{row[0]} - {row[1]} {row[2]}",) for row in cursor.fetchall()]
    conn.close()
    return usuarios


def obtener_usuario_por_tarjeta(numero):
    conn = sqlite3.connect("acceso.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT usuarios.identificacion, usuarios.nombre, usuarios.apellido
        FROM usuarios
        INNER JOIN tarjetas ON usuarios.identificacion = tarjetas.id_usuario
        WHERE tarjetas.numero_tarjeta = ?
    """, (numero,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario


def insertar_tarjeta(identificacion, numero):
    conn = sqlite3.connect("acceso.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tarjetas (id_usuario, numero_tarjeta)
        SELECT identificacion, ? FROM usuarios WHERE identificacion = ?
    """, (numero, identificacion))
    conn.commit()
    conn.close()


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control de Acceso")

        self.boton_agregar_usuario = tk.Button(self, text="Agregar Usuario", command=self.agregar_usuario)
        self.boton_agregar_usuario.pack(padx=10, pady=10)

        self.boton_agregar_tarjeta = tk.Button(self, text="Agregar Tarjeta", command=self.agregar_tarjeta)
        self.boton_agregar_tarjeta.pack(padx=10, pady=10)

        self.boton_validar_tarjeta = tk.Button(self, text="Validar Tarjeta", command=self.validar_tarjeta)
        self.boton_validar_tarjeta.pack(padx=10, pady=10)

    def agregar_usuario(self):
        formulario = tk.Toplevel(self)
        formulario.title("Agregar Usuario")

        etiqueta_identificacion = tk.Label(formulario, text="Identificación:")
        etiqueta_identificacion.grid(row=0, column=0, padx=5, pady=5)

        identificacion = tk.Entry(formulario)
        identificacion.grid(row=0, column=1, padx=5, pady=5)

        etiqueta_nombre = tk.Label(formulario, text="Nombre:")
        etiqueta_nombre.grid(row=1, column=0, padx=5, pady=5)

        nombre = tk.Entry(formulario)
        nombre.grid(row=1, column=1, padx=5, pady=5)

        etiqueta_apellido = tk.Label(formulario, text="Apellido:")
        etiqueta_apellido.grid(row=2, column=0, padx=5, pady=5)

        apellido = tk.Entry(formulario)
        apellido.grid(row=2, column=1, padx=5, pady=5)

        boton_guardar = tk.Button(formulario, text="Guardar", command=lambda: self.guardar_usuario(identificacion.get(), nombre.get(), apellido.get()))
        boton_guardar.grid(row=3, column=1, padx=5, pady=5)

    def guardar_usuario(self, identificacion, nombre, apellido):
        if not identificacion or not nombre or not apellido:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
        else:
            insertar_usuario(identificacion, nombre, apellido)
            messagebox.showerror("Usuario Agregado", "Se agregó el usuario existosamente!")
            self.destroy()

    def agregar_tarjeta(self):
        formulario = TarjetaFormulario(self)

    def validar_tarjeta(self):
        formulario = AccesoFormulario(self)



class TarjetaFormulario(tk.Toplevel):
    def __init__(self, ventana_principal):
        super().__init__(ventana_principal)
        self.title("Agregar Tarjeta")

        self.etiqueta_usuario = tk.Label(self, text="Usuario:")
        self.etiqueta_usuario.grid(row=0, column=0, padx=5, pady=5)

        self.usuario = tk.StringVar()
        self.combo_usuario = ttk.Combobox(self, textvariable=self.usuario, values=obtener_usuarios())
        self.combo_usuario.grid(row=0, column=1, padx=5, pady=5)

        self.etiqueta_numero = tk.Label(self, text="Número:")
        self.etiqueta_numero.grid(row=1, column=0, padx=5, pady=5)

        self.numero = tk.Entry(self)
        self.numero.grid(row=1, column=1, padx=5, pady=5)

        self.boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_tarjeta)
        self.boton_guardar.grid(row=2, column=1, padx=5, pady=5)

    def guardar_tarjeta(self):
        print(self.usuario.get())
        usuario_seleccionado = self.usuario.get()
        numero = self.numero.get()

        if not usuario_seleccionado or not numero:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
        else:
            identificacion = usuario_seleccionado.split("-")[0].strip()
            identificacion = identificacion.replace('{', '')
            print(identificacion)
            insertar_tarjeta(identificacion, numero)
            messagebox.showerror("Tarjeta Agregada", "Se agrego la tarjeta de manera exitosa")
            #self.destroy(TarjetaFormulario);


class AccesoFormulario(tk.Toplevel):
    def __init__(self, ventana_principal):
        super().__init__(ventana_principal)
        self.title("Validar Tarjeta")

        self.etiqueta_numero = tk.Label(self, text="Número:")
        self.etiqueta_numero.grid(row=0, column=0, padx=5, pady=5)

        self.numero = tk.Entry(self)
        self.numero.grid(row=0, column=1, padx=5, pady=5)

        self.boton_validar = tk.Button(self, text="Validar", command=self.validar_tarjeta)
        self.boton_validar.grid(row=1, column=1, padx=5, pady=5)

    def validar_tarjeta(self):
        numero = self.numero.get()

        if not numero:
            messagebox.showerror("Error", "Por favor, complete el campo de número")
        else:
            usuario = obtener_usuario_por_tarjeta(numero)

            if usuario:
                messagebox.showinfo("Acceso permitido", f"Bienvenid@, {usuario[1]} {usuario[2]}")
                self.destroy()
            else:
                messagebox.showerror("Acceso denegado", "Tarjeta no válida")

            self.destroy()


ventana_principal = VentanaPrincipal()
ventana_principal.mainloop()
