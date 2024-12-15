import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from dao import DAO  # Asegúrate de que el archivo dao.py esté correctamente configurado

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Librería Virtual")
        self.geometry("800x600")
        self.resizable(False, False)

        # DAO para la conexión con la base de datos
        self.dao = DAO()

        # Estilo general
        self.configure(bg="#f5f5f5")

        # Frame principal
        self.frame_actual = None
        self.cambiar_frame(LoginFrame)

    def cambiar_frame(self, frame_class):
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        self.frame_actual = frame_class(self)
        self.frame_actual.pack(fill="both", expand=True)

    def cargar_imagen(self, path, size):
        try:
            image = Image.open(path)
            image = image.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except FileNotFoundError:
            print(f"Archivo no encontrado: {path}")
            return None

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Imagen de fondo
        self.bg_image = master.cargar_imagen("C:/Users/pablo/Documents/tkinter/imagenes/libros.jpg", (800, 600))
        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Título
        self.title = tk.Label(self, text="Inicio de Sesión", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Campos de entrada
        self.username_label = tk.Label(self, text="Usuario:", font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Contraseña:", font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        # Botón de inicio de sesión
        self.login_button = tk.Button(self, text="Iniciar Sesión", font=("Arial", 14, "bold"), bg="#007BFF", fg="white",
                                       command=self.iniciar_sesion)
        self.login_button.pack(pady=20)

        # Botón de registrar usuario
        self.register_button = tk.Button(self, text="Registrar Usuario", font=("Arial", 12, "bold"), bg="#28A745", fg="white",
                                         command=self.abrir_registro)
        self.register_button.pack(pady=5)

    def abrir_registro(self):
        self.master.cambiar_frame(RegistroFrame)

    def iniciar_sesion(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Por favor, ingrese todos los campos")
            return

        # Verificar las credenciales con el DAO
        usuario = self.master.dao.validar_credenciales(username, password)
        if usuario:
            if usuario["role"] == "admin":
                self.master.cambiar_frame(AdminFrame)
            else:
                self.master.cambiar_frame(UserFrame)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

class RegistroFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Imagen de fondo
        self.bg_image = master.cargar_imagen("C:/Users/pablo/Documents/tkinter/imagenes/registro.png", (800, 600))
        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Título
        self.title = tk.Label(self, text="Registrar Usuario", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Campos de entrada
        self.username_label = tk.Label(self, text="Usuario:", font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Contraseña:", font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        self.role_label = tk.Label(self, text="Rol (admin/user):", font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.role_label.pack(pady=5)
        self.role_entry = tk.Entry(self, font=("Arial", 14))
        self.role_entry.pack(pady=5)

        # Botón para registrar
        self.register_button = tk.Button(self, text="Registrar", font=("Arial", 14, "bold"), bg="#007BFF", fg="white",
                                        command=self.registrar_usuario)
        self.register_button.pack(pady=20)

        # Botón para volver
        self.back_button = tk.Button(self, text="Volver", font=("Arial", 12, "bold"), bg="#DC3545", fg="white",
                                     command=lambda: master.cambiar_frame(LoginFrame))
        self.back_button.pack(pady=10)

    def registrar_usuario(self):
        """Registra un nuevo usuario en la base de datos."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if role not in ["admin", "user"]:
            messagebox.showerror("Error", "El rol debe ser 'admin' o 'user'.")
            return

        try:
            self.master.dao.agregar_usuario(username, password, role)
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.master.cambiar_frame(LoginFrame)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

class AdminFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Imagen de fondo
        self.bg_image = master.cargar_imagen("C:/Users/pablo/Documents/tkinter/imagenes/gestion.jpg", (800, 600))
        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tk.Label(self, text="Panel de Administración", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.label.pack(pady=20)

        # Botones de funcionalidades
        self.boton_gestionar_productos = tk.Button(self, text="Gestionar Productos", font=("Arial", 14), bg="#007BFF", fg="white",
                                                   command=lambda: master.cambiar_frame(GestionProductosFrame))
        self.boton_gestionar_productos.pack(pady=10)

        self.boton_gestionar_bodegas = tk.Button(self, text="Gestionar Bodegas", font=("Arial", 14), bg="#007BFF", fg="white",
                                                 command=lambda: master.cambiar_frame(GestionBodegasFrame))
        self.boton_gestionar_bodegas.pack(pady=10)

        self.boton_generar_informes = tk.Button(self, text="Generar Informes", font=("Arial", 14), bg="#007BFF", fg="white",
                                                command=lambda: master.cambiar_frame(GenerarInformesFrame))
        self.boton_generar_informes.pack(pady=10)

        self.logout_button = tk.Button(self, text="Cerrar Sesión", font=("Arial", 14, "bold"), bg="#DC3545", fg="white",
                                        command=lambda: master.cambiar_frame(LoginFrame))
        self.logout_button.pack(pady=20)

class GestionProductosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Título
        self.title = tk.Label(self, text="Gestión de Productos", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Botones de funcionalidad
        self.boton_agregar = tk.Button(self, text="Agregar Producto", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.abrir_formulario_agregar)
        self.boton_agregar.pack(pady=10)

        self.boton_listar = tk.Button(self, text="Listar Productos", font=("Arial", 14), bg="#007BFF", fg="white",
                                      command=self.listar_productos)
        self.boton_listar.pack(pady=10)

        self.boton_volver = tk.Button(self, text="Volver", font=("Arial", 14), bg="#DC3545", fg="white",
                                      command=lambda: master.cambiar_frame(AdminFrame))
        self.boton_volver.pack(pady=20)

    def abrir_formulario_agregar(self):
        # Crear una ventana secundaria para agregar un producto
        ventana = tk.Toplevel(self)
        ventana.title("Agregar Producto")
        ventana.geometry("400x400")
        ventana.resizable(False, False)

        # Campos de entrada
        tk.Label(ventana, text="Nombre del Producto:", font=("Arial", 12)).pack(pady=5)
        nombre_entry = tk.Entry(ventana, font=("Arial", 12))
        nombre_entry.pack(pady=5)

        tk.Label(ventana, text="Tipo (libro/revista/enciclopedia):", font=("Arial", 12)).pack(pady=5)
        tipo_entry = tk.Entry(ventana, font=("Arial", 12))
        tipo_entry.pack(pady=5)

        tk.Label(ventana, text="ID de la Editorial:", font=("Arial", 12)).pack(pady=5)
        editorial_entry = tk.Entry(ventana, font=("Arial", 12))
        editorial_entry.pack(pady=5)

        tk.Label(ventana, text="Descripción:", font=("Arial", 12)).pack(pady=5)
        descripcion_entry = tk.Text(ventana, font=("Arial", 12), height=5, width=40)
        descripcion_entry.pack(pady=5)

        # Botón para guardar
        tk.Button(ventana, text="Guardar", font=("Arial", 12), bg="#007BFF", fg="white",
                  command=lambda: self.guardar_producto(nombre_entry.get(), tipo_entry.get(), editorial_entry.get(),
                                                        descripcion_entry.get("1.0", tk.END), ventana)).pack(pady=10)

    def guardar_producto(self, nombre, tipo, editorial_id, descripcion, ventana):
        """Guarda el producto en la base de datos."""
        if not nombre or not tipo or not editorial_id or not descripcion.strip():
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if tipo not in ["libro", "revista", "enciclopedia"]:
            messagebox.showerror("Error", "El tipo debe ser 'libro', 'revista' o 'enciclopedia'.")
            return

        try:
            # Llamar al DAO para agregar el producto
            editorial_id = int(editorial_id)  # Asegurarse de que el ID sea un entero
            self.master.dao.agregar_producto(nombre, tipo, editorial_id, descripcion.strip())
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            ventana.destroy()  # Cerrar la ventana secundaria
        except ValueError:
            messagebox.showerror("Error", "El ID de la editorial debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")

    def listar_productos(self):
        productos = self.master.dao.obtener_productos()
        mensaje = "\n".join([f"{p['id']} - {p['nombre']} ({p['tipo']})" for p in productos])
        messagebox.showinfo("Lista de Productos", mensaje if mensaje else "No hay productos disponibles.")

class GestionBodegasFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Título
        self.title = tk.Label(self, text="Gestión de Bodegas", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Botones de funcionalidad
        self.boton_agregar = tk.Button(self, text="Agregar Bodega", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.abrir_formulario_agregar)
        self.boton_agregar.pack(pady=10)

        self.boton_listar = tk.Button(self, text="Listar Bodegas", font=("Arial", 14), bg="#007BFF", fg="white",
                                      command=self.listar_bodegas)
        self.boton_listar.pack(pady=10)

        self.boton_volver = tk.Button(self, text="Volver", font=("Arial", 14), bg="#DC3545", fg="white",
                                      command=lambda: master.cambiar_frame(AdminFrame))
        self.boton_volver.pack(pady=20)

    def abrir_formulario_agregar(self):
        """Abre una ventana secundaria para agregar una nueva bodega."""
        ventana = tk.Toplevel(self)
        ventana.title("Agregar Bodega")
        ventana.geometry("400x300")
        ventana.resizable(False, False)

        # Campos del formulario
        tk.Label(ventana, text="Nombre de la Bodega:", font=("Arial", 12)).pack(pady=5)
        nombre_entry = tk.Entry(ventana, font=("Arial", 12))
        nombre_entry.pack(pady=5)

        tk.Label(ventana, text="Dirección de la Bodega:", font=("Arial", 12)).pack(pady=5)
        direccion_entry = tk.Entry(ventana, font=("Arial", 12))
        direccion_entry.pack(pady=5)

        tk.Label(ventana, text="Capacidad (en unidades):", font=("Arial", 12)).pack(pady=5)
        capacidad_entry = tk.Entry(ventana, font=("Arial", 12))
        capacidad_entry.pack(pady=5)

        # Botón para guardar
        tk.Button(ventana, text="Guardar", font=("Arial", 12), bg="#007BFF", fg="white",
                  command=lambda: self.guardar_bodega(nombre_entry.get(), direccion_entry.get(), capacidad_entry.get(),
                                                     ventana)).pack(pady=10)

    def guardar_bodega(self, nombre, direccion, capacidad, ventana):
        """Guarda la bodega en la base de datos."""
        if not nombre or not direccion or not capacidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            capacidad = int(capacidad)  # Validar que la capacidad sea un número entero
            if capacidad <= 0:
                raise ValueError("La capacidad debe ser mayor a 0.")

            # Llamar al DAO para agregar la bodega
            self.master.dao.agregar_bodega(nombre, direccion, capacidad)
            messagebox.showinfo("Éxito", "Bodega agregada correctamente.")
            ventana.destroy()  # Cerrar la ventana secundaria
        except ValueError as e:
            messagebox.showerror("Error", f"Capacidad inválida: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la bodega: {e}")    

    def listar_bodegas(self):
        bodegas = self.master.dao.obtener_bodegas()
        mensaje = "\n".join([f"{b['id']} - {b['nombre']}" for b in bodegas])
        messagebox.showinfo("Lista de Bodegas", mensaje if mensaje else "No hay bodegas disponibles.")

class GenerarInformesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Título
        self.title = tk.Label(self, text="Generar Informes", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Botones de funcionalidad
        self.boton_inventario = tk.Button(self, text="Informe de Inventario", font=("Arial", 14), bg="#007BFF", fg="white",
                                          command=self.generar_informe_inventario)
        self.boton_inventario.pack(pady=10)

        self.boton_movimientos = tk.Button(self, text="Informe de Movimientos", font=("Arial", 14), bg="#007BFF", fg="white",
                                           command=self.generar_informe_movimientos)
        self.boton_movimientos.pack(pady=10)

        self.boton_volver = tk.Button(self, text="Volver", font=("Arial", 14), bg="#DC3545", fg="white",
                                      command=lambda: master.cambiar_frame(AdminFrame))
        self.boton_volver.pack(pady=20)

    def generar_informe_inventario(self):
        """Genera un informe del inventario por bodega."""
        try:
            # Obtener el inventario desde el DAO
            inventario = self.master.dao.obtener_inventario()

            if not inventario:
                messagebox.showinfo("Informe de Inventario", "No hay productos en el inventario.")
                return

            # Formatear el informe
            informe = []
            for item in inventario:
                informe.append(
                    f"Bodega: {item['bodega']} - Producto: {item['producto']} - Tipo: {item['tipo']} - Cantidad: {item['cantidad']}"
                )

            mensaje = "\n".join(informe)
            messagebox.showinfo("Informe de Inventario", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el informe de inventario: {e}")

    def generar_informe_movimientos(self):
        movimientos = self.master.dao.obtener_movimientos()
        mensaje = "\n".join([f"ID: {m['id']} - Origen: {m['bodega_origen_id']} - Destino: {m['bodega_destino_id']}" for m in movimientos])
        messagebox.showinfo("Informe de Movimientos", mensaje if mensaje else "No hay movimientos registrados.")

class UserFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Imagen de fondo
        self.bg_image = master.cargar_imagen("C:/Users/pablo/Documents/tkinter/imagenes/user.jpg", (800, 600))
        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tk.Label(self, text="Bienvenido Bodeguero", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.label.pack(pady=20)

        self.boton_mover_productos = tk.Button(self, text="Mover Productos", font=("Arial", 14), bg="#007BFF", fg="white",
                                               command=lambda: master.cambiar_frame(MoverProductosFrame))
        self.boton_mover_productos.pack(pady=10)

        self.logout_button = tk.Button(self, text="Cerrar Sesión", font=("Arial", 14, "bold"), bg="#DC3545", fg="white",
                                        command=lambda: master.cambiar_frame(LoginFrame))
        self.logout_button.pack(pady=20)

class MoverProductosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Título
        self.title = tk.Label(self, text="Mover Productos", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Campos de entrada
        self.origen_label = tk.Label(self, text="Bodega Origen:", font=("Arial", 14))
        self.origen_label.pack(pady=5)
        self.origen_entry = tk.Entry(self, font=("Arial", 14))
        self.origen_entry.pack(pady=5)

        self.destino_label = tk.Label(self, text="Bodega Destino:", font=("Arial", 14))
        self.destino_label.pack(pady=5)
        self.destino_entry = tk.Entry(self, font=("Arial", 14))
        self.destino_entry.pack(pady=5)

        self.productos_label = tk.Label(self, text="Productos y Cantidades (ID:Cantidad):", font=("Arial", 14))
        self.productos_label.pack(pady=5)
        self.productos_entry = tk.Entry(self, font=("Arial", 14))
        self.productos_entry.pack(pady=5)

        # Botones
        self.boton_confirmar = tk.Button(self, text="Confirmar Movimiento", font=("Arial", 14), bg="#007BFF", fg="white",
                                         command=self.confirmar_movimiento)
        self.boton_confirmar.pack(pady=20)

        self.boton_volver = tk.Button(self, text="Volver", font=("Arial", 14), bg="#DC3545", fg="white",
                                      command=lambda: master.cambiar_frame(UserFrame))
        self.boton_volver.pack(pady=10)

    def confirmar_movimiento(self):
        bodega_origen = self.origen_entry.get()
        bodega_destino = self.destino_entry.get()
        productos_texto = self.productos_entry.get()

        if not bodega_origen or not bodega_destino or not productos_texto:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            # Procesar productos y cantidades
            productos = {}
            for item in productos_texto.split(","):
                producto_id, cantidad = map(str.strip, item.split(":"))
                productos[int(producto_id)] = int(cantidad)

            # Registrar el movimiento
            usuario_id = 1  # Asume que el usuario logueado tiene ID 1; adapta según tu lógica
            self.master.dao.registrar_movimiento(bodega_origen, bodega_destino, usuario_id, productos)
            messagebox.showinfo("Éxito", "Movimiento registrado correctamente.")
            self.master.cambiar_frame(UserFrame)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el movimiento: {e}")

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
