
import tkinter as tk
from tkinter import messagebox


class Componente:
    def __init__(self, codigo, nombre, cantidad):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad


class Inventario:
    def __init__(self):
        self.componentes = []
        self.cargar()

        if len(self.componentes) == 0:
            self.componentes.append(Componente("C001", "Resistencias 220 ohm", 100))
            self.componentes.append(Componente("C002", "Resistencias 330 ohm", 100))
            self.componentes.append(Componente("C003", "LED rojo", 50))
            self.componentes.append(Componente("C004", "Protoboard", 15))
            self.componentes.append(Componente("C005", "Cables jumper", 100))
            self.componentes.append(Componente("C006", "Integrado 74HC08", 20))
            self.componentes.append(Componente("C007", "Display 7 segmentos", 20))
            self.guardar()

    def guardar(self):
        archivo = open("inventario.txt", "w")

        for c in self.componentes:
            archivo.write(c.codigo + "," + c.nombre + "," + str(c.cantidad) + "\n")

        archivo.close()

    def cargar(self):
        try:
            archivo = open("inventario.txt", "r")

            for linea in archivo:
                datos = linea.strip().split(",")

                if len(datos) == 3:
                    c = Componente(datos[0], datos[1], int(datos[2]))
                    self.componentes.append(c)

            archivo.close()

        except FileNotFoundError:
            pass


class Usuario:
    def __init__(self, nombre, documento, contrasena, rol):
        self.nombre = nombre
        self.documento = documento
        self.contrasena = contrasena
        self.rol = rol


class Sistema:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Inventario de Electronica - UPN")
        self.ventana.geometry("650x600")

        self.usuarios = []
        self.cargar_usuarios()

        self.inventario = Inventario()
        self.usuario_actual = None

        self.login()

    def limpiar(self):
        for elemento in self.ventana.winfo_children():
            elemento.destroy()

    # CARGAR USUARIOS

    def cargar_usuarios(self):
        try:
            archivo = open("usuarios.txt", "r")

            for linea in archivo:
                datos = linea.strip().split(",")

                if len(datos) == 4:
                    usuario = Usuario(datos[0], datos[1], datos[2], datos[3])
                    self.usuarios.append(usuario)

            archivo.close()

        except FileNotFoundError:
            pass

    def guardar_usuarios(self):
        archivo = open("usuarios.txt", "w")

        for u in self.usuarios:
            archivo.write(u.nombre + "," + u.documento + "," +
                          u.contrasena + "," + u.rol + "\n")

        archivo.close()


    def login(self):
        self.limpiar()

        tk.Label(self.ventana, text="INVENTARIO DE ELECTRONICA",
                 font=("Arial", 20, "bold")).pack(pady=20)

        tk.Label(self.ventana, text="UNIVERSIDAD UPN",
                 font=("Arial", 14)).pack(pady=5)

        tk.Label(self.ventana, text="Numero de documento").pack()
        self.documento = tk.Entry(self.ventana)
        self.documento.pack(pady=5)

        tk.Label(self.ventana, text="Contrasena").pack()
        self.contrasena = tk.Entry(self.ventana, show="*")
        self.contrasena.pack(pady=5)

        tk.Button(self.ventana, text="Iniciar sesion",
                  command=self.iniciar_sesion).pack(pady=10)

        tk.Button(self.ventana, text="Crear cuenta",
                  command=self.registrar).pack(pady=5)

    def iniciar_sesion(self):
        documento = self.documento.get()
        contrasena = self.contrasena.get()

        for usuario in self.usuarios:
            if usuario.documento == documento and usuario.contrasena == contrasena:
                self.usuario_actual = usuario
                self.menu()
                return

        messagebox.showerror("Error", "Documento o contrasena incorrectos")


    def registrar(self):
        self.limpiar()

        tk.Label(self.ventana, text="CREAR CUENTA",
                 font=("Arial", 20, "bold")).pack(pady=20)

        tk.Label(self.ventana, text="Nombre completo").pack()
        self.nombre = tk.Entry(self.ventana)
        self.nombre.pack(pady=5)

        tk.Label(self.ventana, text="Documento").pack()
        self.doc = tk.Entry(self.ventana)
        self.doc.pack(pady=5)

        tk.Label(self.ventana, text="Contrasena").pack()
        self.pass_registro = tk.Entry(self.ventana, show="*")
        self.pass_registro.pack(pady=5)

        tk.Label(self.ventana, text="Seleccione su rol").pack()

        self.rol = tk.StringVar()
        self.rol.set("estudiante")

        tk.OptionMenu(self.ventana, self.rol,
                      "estudiante", "profesor").pack(pady=5)

        tk.Label(self.ventana, text="Clave de profesor (si aplica)").pack()
        self.clave = tk.Entry(self.ventana, show="*")
        self.clave.pack(pady=5)

        tk.Button(self.ventana, text="Registrar",
                  command=self.guardar_registro).pack(pady=10)

        tk.Button(self.ventana, text="Volver",
                  command=self.login).pack(pady=5)

    def guardar_registro(self):
        nombre = self.nombre.get()
        documento = self.doc.get()
        contrasena = self.pass_registro.get()
        rol = self.rol.get()

        if nombre == "" or documento == "" or contrasena == "":
            messagebox.showwarning("Aviso", "Complete todos los campos")
            return

        for u in self.usuarios:
            if u.documento == documento:
                messagebox.showerror("Error", "Ese documento ya existe")
                return

        if rol == "profesor":
            if self.clave.get() != "PROFE2026":
                messagebox.showerror("Error", "Clave de profesor incorrecta")
                return

        usuario = Usuario(nombre, documento, contrasena, rol)
        self.usuarios.append(usuario)
        self.guardar_usuarios()

        messagebox.showinfo("Correcto", "Cuenta creada correctamente")
        self.login()


    def menu(self):
        self.limpiar()

        tk.Label(self.ventana, text="INVENTARIO DE ELECTRONICA",
                 font=("Arial", 20, "bold")).pack(pady=10)

        tk.Label(self.ventana, text="Usuario: " + self.usuario_actual.nombre).pack()
        tk.Label(self.ventana, text="Rol: " + self.usuario_actual.rol).pack()

        tk.Label(self.ventana, text="COMPONENTES",
                 font=("Arial", 14, "bold")).pack(pady=10)

        self.lista = tk.Listbox(self.ventana, width=65, height=12)
        self.lista.pack(pady=5)

        self.actualizar_lista()

        tk.Label(self.ventana, text="Codigo del componente").pack()
        self.codigo = tk.Entry(self.ventana)
        self.codigo.pack(pady=5)

        tk.Button(self.ventana, text="Buscar",
                  command=self.buscar).pack(pady=3)

        tk.Button(self.ventana, text="Prestar",
                  command=self.prestar).pack(pady=3)

        tk.Button(self.ventana, text="Devolver",
                  command=self.devolver).pack(pady=3)

        if self.usuario_actual.rol == "profesor":

            tk.Label(self.ventana, text="Nombre del componente").pack()
            self.nombre_componente = tk.Entry(self.ventana)
            self.nombre_componente.pack(pady=3)

            tk.Label(self.ventana, text="Cantidad").pack()
            self.cantidad = tk.Entry(self.ventana)
            self.cantidad.pack(pady=3)

            tk.Button(self.ventana, text="Agregar componente",
                      command=self.agregar).pack(pady=3)

            tk.Button(self.ventana, text="Eliminar componente",
                      command=self.eliminar).pack(pady=3)

        tk.Button(self.ventana, text="Cerrar sesion",
                  command=self.login).pack(pady=10)


    def actualizar_lista(self):
        self.lista.delete(0, tk.END)

        for c in self.inventario.componentes:
            texto = c.codigo + " - " + c.nombre + " - Cantidad: " + str(c.cantidad)
            self.lista.insert(tk.END, texto)

    # BUSCAR COMPONENTE

    def buscar(self):
        codigo = self.codigo.get()

        for c in self.inventario.componentes:
            if c.codigo == codigo:
                messagebox.showinfo("Componente encontrado",
                                    "Codigo: " + c.codigo +
                                    "\nNombre: " + c.nombre +
                                    "\nCantidad: " + str(c.cantidad))
                return

        messagebox.showerror("Error", "Componente no encontrado")


    def prestar(self):
        codigo = self.codigo.get()

        for c in self.inventario.componentes:
            if c.codigo == codigo:
                if c.cantidad > 0:
                    c.cantidad -= 1
                    self.inventario.guardar()
                    self.actualizar_lista()
                    messagebox.showinfo("Correcto", "Componente prestado")
                else:
                    messagebox.showwarning("Aviso", "No hay unidades disponibles")
                return

        messagebox.showerror("Error", "Componente no encontrado")



    def devolver(self):
        codigo = self.codigo.get()

        for c in self.inventario.componentes:
            if c.codigo == codigo:
                c.cantidad += 1
                self.inventario.guardar()
                self.actualizar_lista()
                messagebox.showinfo("Correcto", "Componente devuelto")
                return

        messagebox.showerror("Error", "Componente no encontrado")

   

    def agregar(self):
        codigo = self.codigo.get()
        nombre = self.nombre_componente.get()

        try:
            cantidad = int(self.cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Digite una cantidad valida")
            return

        if codigo == "" or nombre == "" or cantidad <= 0:
            messagebox.showwarning("Aviso", "Complete los campos correctamente")
            return

        for c in self.inventario.componentes:
            if c.codigo == codigo:
                messagebox.showerror("Error", "Ese codigo ya existe")
                return

        componente = Componente(codigo, nombre, cantidad)
        self.inventario.componentes.append(componente)

        self.inventario.guardar()
        self.actualizar_lista()

        messagebox.showinfo("Correcto", "Componente agregado")



    def eliminar(self):
        codigo = self.codigo.get()

        for c in self.inventario.componentes:
            if c.codigo == codigo:
                self.inventario.componentes.remove(c)
                self.inventario.guardar()
                self.actualizar_lista()
                messagebox.showinfo("Correcto", "Componente eliminado")
                return

        messagebox.showerror("Error", "Componente no encontrado")


ventana = tk.Tk()
sistema = Sistema(ventana)
ventana.mainloop()
