import tkinter as tk
import random
import time
import mysql.connector

# Configuración del juego
ANCHO = 400
ALTO = 600
VELOCIDAD_OBSTACULOS_INICIAL = 5
MOVIMIENTO_AUTO = 20
TAMAÑO_AUTO = 50
TAMAÑO_OBSTACULO = 50
NUM_OBSTACULOS = 3

# Conexión a la base de datos
def connect_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='juego'
    )
    return conn

# Clase del juego
class JuegoAutos:
    def __init__(self, root, usuario_id, usuario_nombre, edad, resultados):
        self.root = root
        self.usuario_id = usuario_id
        self.usuario_nombre = usuario_nombre
        self.edad = edad
        self.resultados = resultados
        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="white")
        self.canvas.pack()

        # Variables de juego
        self.auto = None
        self.obstaculos = []
        self.puntos = 0
        self.movimientos = 0
        self.jugando = True
        self.distancia = 0
        self.velocidad_obstaculos = VELOCIDAD_OBSTACULOS_INICIAL
        self.tiempo_inicio = time.time()

        # Crear auto
        self.crear_auto()

        # Eventos de teclado
        self.root.bind("<Left>", self.mover_izquierda)
        self.root.bind("<Right>", self.mover_derecha)

        # Iniciar el juego
        self.actualizar_obstaculos()
        self.actualizar_pantalla()

    def crear_auto(self):
        self.auto_x = ANCHO // 2 - TAMAÑO_AUTO // 2
        self.auto_y = ALTO - TAMAÑO_AUTO - 20
        self.auto = self.canvas.create_rectangle(self.auto_x, self.auto_y, 
                                                 self.auto_x + TAMAÑO_AUTO, 
                                                 self.auto_y + TAMAÑO_AUTO, 
                                                 fill="blue")

    def mover_izquierda(self, event):
        if self.auto_x > 0:
            self.auto_x -= MOVIMIENTO_AUTO
            self.movimientos += 1
        self.canvas.coords(self.auto, self.auto_x, self.auto_y, 
                           self.auto_x + TAMAÑO_AUTO, self.auto_y + TAMAÑO_AUTO)

    def mover_derecha(self, event):
        if self.auto_x < ANCHO - TAMAÑO_AUTO:
            self.auto_x += MOVIMIENTO_AUTO
            self.movimientos += 1
        self.canvas.coords(self.auto, self.auto_x, self.auto_y, 
                           self.auto_x + TAMAÑO_AUTO, self.auto_y + TAMAÑO_AUTO)

    def crear_obstaculo(self):
        x = random.randint(0, ANCHO - TAMAÑO_OBSTACULO)
        obstaculo = self.canvas.create_rectangle(x, -TAMAÑO_OBSTACULO, 
                                                 x + TAMAÑO_OBSTACULO, 0, 
                                                 fill="red")
        self.obstaculos.append(obstaculo)

    def mover_obstaculos(self):
        for obstaculo in self.obstaculos:
            coords = self.canvas.coords(obstaculo)
            self.canvas.move(obstaculo, 0, self.velocidad_obstaculos)
            if coords[1] >= ALTO:
                self.obstaculos.remove(obstaculo)
                self.canvas.delete(obstaculo)
                self.puntos += 1
            elif self.colision(coords):
                self.jugando = False

    def colision(self, coords_obstaculo):
        coords_auto = self.canvas.coords(self.auto)
        if (coords_auto[0] < coords_obstaculo[2] and
            coords_auto[2] > coords_obstaculo[0] and
            coords_auto[1] < coords_obstaculo[3] and
            coords_auto[3] > coords_obstaculo[1]):
            return True
        return False

    def actualizar_obstaculos(self):
        if self.jugando:
            self.mover_obstaculos()
            if random.randint(1, 20) <= NUM_OBSTACULOS:
                self.crear_obstaculo()
            self.root.after(100, self.actualizar_obstaculos)

    def actualizar_pantalla(self):
        if self.jugando:
            self.distancia += self.velocidad_obstaculos
            if self.distancia % 100 == 0:
                self.velocidad_obstaculos += 1

            self.mostrar_datos()
            self.root.after(50, self.actualizar_pantalla)
        else:
            self.registrar_resultado()
            self.mostrar_datos_finales()

    def mostrar_datos(self):
        self.canvas.delete("datos")
        self.canvas.create_text(10, 10, anchor="nw", text=f"Puntos: {self.puntos}", 
                                fill="black", font=("Arial", 12), tags="datos")
        self.canvas.create_text(10, 30, anchor="nw", text=f"Distancia: {self.distancia}", 
                                fill="black", font=("Arial", 12), tags="datos")
        self.canvas.create_text(10, 50, anchor="nw", text=f"Movimientos: {self.movimientos}", 
                                fill="black", font=("Arial", 12), tags="datos")

    def registrar_resultado(self):
        tiempo_jugado = time.time() - self.tiempo_inicio
        conn = connect_db()
        cursor = conn.cursor()

        # Insertar los resultados del juego en la base de datos
        cursor.execute("""
            INSERT INTO resultados_juego (id_usuario, distancia, puntos, tiempo, movimientos) 
            VALUES (%s, %s, %s, %s, %s)
        """, (self.usuario_id, self.distancia, self.puntos, tiempo_jugado, self.movimientos))

        conn.commit()
        cursor.close()
        conn.close()

    def mostrar_datos_finales(self):
        tiempo_jugado = time.time() - self.tiempo_inicio
        self.canvas.create_text(ANCHO // 2, ALTO // 2, text="¡Fin del juego!", 
                                fill="red", font=("Arial", 24))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 30, 
                                text=f"Jugador: {self.usuario_nombre}", fill="black", font=("Arial", 14))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 50, 
                                text=f"Edad: {self.edad}", fill="black", font=("Arial", 14))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 70, 
                                text=f"Distancia: {self.distancia}", fill="black", font=("Arial", 14))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 90, 
                                text=f"Puntos: {self.puntos}", fill="black", font=("Arial", 14))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 110, 
                                text=f"Tiempo: {tiempo_jugado:.2f} segundos", fill="black", font=("Arial", 14))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 130, 
                                text=f"Movimientos: {self.movimientos}", fill="black", font=("Arial", 14))

        tk.Button(self.root, text="Reiniciar Juego", command=self.reiniciar_juego).pack(pady=20)

    def reiniciar_juego(self):
        self.root.destroy()
        iniciar_juego(self.usuario_id, self.usuario_nombre, self.edad, self.resultados)

# Registro de usuario
def registrar_usuario():
    registro = tk.Tk()
    registro.title("Registro de Usuario")

    tk.Label(registro, text="Nombre:").pack(pady=5)
    nombre_entry = tk.Entry(registro)
    nombre_entry.pack(pady=5)

    tk.Label(registro, text="Edad:").pack(pady=5)
    edad_entry = tk.Entry(registro)
    edad_entry.pack(pady=5)

    tk.Label(registro, text="Correo:").pack(pady=5)
    correo_entry = tk.Entry(registro)
    correo_entry.pack(pady=5)

    tk.Label(registro, text="Contraseña:").pack(pady=5)
    password_entry = tk.Entry(registro, show="*")
    password_entry.pack(pady=5)

    tk.Label(registro, text="Repetir Contraseña:").pack(pady=5)
    repeat_password_entry = tk.Entry(registro, show="*")
    repeat_password_entry.pack(pady=5)

    def registrar():
        nombre = nombre_entry.get()
        edad = edad_entry.get()
        correo = correo_entry.get()
        contraseña = password_entry.get()
        repetir_contraseña = repeat_password_entry.get()

        if nombre and edad.isdigit() and correo and contraseña and repetir_contraseña:
            if contraseña == repetir_contraseña:
                conn = connect_db()
                cursor = conn.cursor()

                try:
                    cursor.execute("INSERT INTO usuarios (nombre, edad, correo, contraseña) VALUES (%s, %s, %s, %s)", 
                                   (nombre, edad, correo, contraseña))
                    conn.commit()
                    print(f"Usuario {nombre} registrado con éxito.")
                    registro.destroy()
                    iniciar_sesion()
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                print("Las contraseñas no coinciden.")
        else:
            print("Por favor, complete todos los campos correctamente.")

    tk.Button(registro, text="Registrar", command=registrar).pack(pady=20)
    registro.mainloop()

# Inicio de sesión
def iniciar_sesion():
    sesion = tk.Tk()
    sesion.title("Iniciar Sesión")

    tk.Label(sesion, text="Correo:").pack(pady=5)
    correo_entry = tk.Entry(sesion)
    correo_entry.pack(pady=5)

    tk.Label(sesion, text="Contraseña:").pack(pady=5)
    password_entry = tk.Entry(sesion, show="*")
    password_entry.pack(pady=5)

    def iniciar():
        correo = correo_entry.get()
        contraseña = password_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, edad FROM usuarios WHERE correo = %s AND contraseña = %s", (correo, contraseña))
        usuario = cursor.fetchone()

        if usuario:
            print(f"Bienvenido {usuario[1]}!")
            sesion.destroy()
            mostrar_menu_inicio(usuario[0], usuario[1], usuario[2])
        else:
            print("Correo o contraseña incorrectos.")
        
        cursor.close()
        conn.close()

    tk.Button(sesion, text="Iniciar Sesión", command=iniciar).pack(pady=10)
    tk.Button(sesion, text="Registrar Usuario", command=lambda: [sesion.destroy(), registrar_usuario()]).pack(pady=10)

    sesion.mainloop()

# Menú de inicio del juego
def mostrar_menu_inicio(usuario_id, nombre, edad):
    menu = tk.Tk()
    menu.title("Menú del Juego")

    tk.Label(menu, text=f"Bienvenido {nombre}").pack(pady=10)
    tk.Button(menu, text="Iniciar Juego", command=lambda: iniciar_juego(usuario_id, nombre, edad, {})).pack(pady=10)

    menu.mainloop()

def iniciar_juego(usuario_id, nombre, edad, resultados):
    root = tk.Tk()
    root.title(f"Juego de Autos - Jugador: {nombre}")
    juego = JuegoAutos(root, usuario_id, nombre, edad, resultados)
    root.mainloop()

# Iniciar con la pantalla de inicio de sesión
iniciar_sesion()

