import tkinter as tk
import random
import time

# Configuración del juego
ANCHO = 400
ALTO = 600
VELOCIDAD_OBSTACULOS_INICIAL = 5
MOVIMIENTO_AUTO = 20
TAMAÑO_AUTO = 50
TAMAÑO_OBSTACULO = 50
NUM_OBSTACULOS = 3  # Aumentamos el número de obstáculos

class JuegoAutos:
    def __init__(self, root, usuario, usuarios, indice_actual, resultados):
        self.root = root
        self.usuario = usuario
        self.usuarios = usuarios
        self.indice_actual = indice_actual
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
        # Posición inicial del auto
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
            if random.randint(1, 20) <= NUM_OBSTACULOS:  # Probabilidad de aparición de varios obstáculos
                self.crear_obstaculo()
            self.root.after(100, self.actualizar_obstaculos)

    def actualizar_pantalla(self):
        if self.jugando:
            # Aumentar la dificultad con la distancia recorrida
            self.distancia += self.velocidad_obstaculos
            if self.distancia % 100 == 0:  # Cada 100 unidades de distancia
                self.velocidad_obstaculos += 1  # Incrementar velocidad de obstáculos

            self.mostrar_datos()
            self.root.after(50, self.actualizar_pantalla)
        else:
            self.registrar_resultado()
            self.mostrar_datos_finales()

    def mostrar_datos(self):
        # Mostrar puntuación y distancia en pantalla
        self.canvas.delete("datos")
        self.canvas.create_text(10, 10, anchor="nw", text=f"Puntos: {self.puntos}", 
                                fill="black", font=("Arial", 12), tags="datos")
        self.canvas.create_text(10, 30, anchor="nw", text=f"Distancia: {self.distancia}", 
                                fill="black", font=("Arial", 12), tags="datos")
        self.canvas.create_text(10, 50, anchor="nw", text=f"Movimientos: {self.movimientos}", 
                                fill="black", font=("Arial", 12), tags="datos")

    def registrar_resultado(self):
        # Registrar los resultados del jugador actual
        tiempo_jugado = time.time() - self.tiempo_inicio
        self.resultados[self.usuario] = {
            "distancia": self.distancia,
            "puntos": self.puntos,
            "tiempo": tiempo_jugado,
            "movimientos": self.movimientos
        }

    def mostrar_datos_finales(self):
        tiempo_jugado = time.time() - self.tiempo_inicio
        self.canvas.create_text(ANCHO // 2, ALTO // 2, text="¡Fin del juego!", 
                                fill="red", font=("Arial", 24))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 30, 
                                text=f"Jugador: {self.usuario}", fill="black", font=("Arial", 14))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 50, 
                                text=f"Distancia: {self.distancia}", fill="black", font=("Arial", 14))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 70, 
                                text=f"Puntos: {self.puntos}", fill="black", font=("Arial", 14))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 90, 
                                text=f"Tiempo: {tiempo_jugado:.2f} segundos", fill="black", font=("Arial", 14))
        self.canvas.create_text(ANCHO // 2, ALTO // 2 + 110, 
                                text=f"Movimientos: {self.movimientos}", fill="black", font=("Arial", 14))

        # Pasar al siguiente jugador si hay más
        self.root.after(3000, self.cambiar_jugador)

    def cambiar_jugador(self):
        self.root.destroy()
        siguiente_indice = (self.indice_actual + 1) % len(self.usuarios)
        if siguiente_indice > 0:
            iniciar_juego(self.usuarios, siguiente_indice, self.resultados)
        else:
            mostrar_resultados_finales(self.resultados)


def ventana_inicio():
    inicio = tk.Tk()
    inicio.title("Inicio de Juego - 4 Jugadores")

    nombres = []
    for i in range(4):
        tk.Label(inicio, text=f"Ingrese el nombre del Jugador {i+1}:").pack(pady=5)
        nombre_entry = tk.Entry(inicio)
        nombre_entry.pack(pady=5)
        nombres.append(nombre_entry)

    def iniciar():
        usuarios = [entry.get() for entry in nombres if entry.get()]
        if len(usuarios) == 4:  # Verificar que los 4 nombres sean ingresados
            inicio.destroy()
            iniciar_juego(usuarios, 0, {})

    tk.Button(inicio, text="Iniciar Juego", command=iniciar).pack(pady=20)
    inicio.mainloop()


def iniciar_juego(usuarios, indice_actual, resultados):
    root = tk.Tk()
    root.title(f"Juego de Autos - Jugador: {usuarios[indice_actual]}")
    juego = JuegoAutos(root, usuarios[indice_actual], usuarios, indice_actual, resultados)
    root.mainloop()


def mostrar_resultados_finales(resultados):
    resumen = tk.Tk()
    resumen.title("Resultados Finales")

    tk.Label(resumen, text="Resultados Finales", font=("Arial", 16)).pack(pady=10)
    for usuario, data in resultados.items():
        tk.Label(resumen, text=f"Jugador: {usuario}").pack(pady=5)
        tk.Label(resumen, text=f"Distancia: {data['distancia']}").pack(pady=5)
        tk.Label(resumen, text=f"Puntos: {data['puntos']}").pack(pady=5)
        tk.Label(resumen, text=f"Tiempo: {data['tiempo']:.2f} segundos").pack(pady=5)
        tk.Label(resumen, text=f"Movimientos: {data['movimientos']}").pack(pady=5)

    tk.Button(resumen, text="Cerrar", command=resumen.destroy).pack(pady=20)
    resumen.mainloop()


# Iniciar el proceso con la ventana de creación de 4 usuarios
ventana_inicio()
