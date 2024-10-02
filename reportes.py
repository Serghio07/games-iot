import tkinter as tk
from tkinter import messagebox
import csv
import mysql.connector

# Función para conectar a la base de datos
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='juego'
    )

# Función para generar reporte en CSV para un usuario específico
def generar_reporte_csv(usuario_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Consulta SQL para obtener todos los resultados de las partidas jugadas por el usuario
    cursor.execute("""
        SELECT id, id_usuario, nombre_usuario, edad, distancia, puntos, tiempo, movimientos, fecha
        FROM resultados_partida
        WHERE id_usuario = %s
    """, (usuario_id,))

    resultados = cursor.fetchall()

    if not resultados:
        messagebox.showinfo("Error", f"No se encontraron partidas para el usuario con ID {usuario_id}")
        return

    # Definir el nombre del archivo CSV a generar
    nombre_archivo = f'reporte_usuario_{usuario_id}.csv'

    # Abrir o crear el archivo CSV para escribir los datos
    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)

        # Escribir los encabezados de las columnas en el archivo CSV
        escritor_csv.writerow(['ID Partida', 'ID Usuario', 'Nombre Usuario', 'Edad', 'Distancia', 'Puntos', 'Tiempo', 'Movimientos', 'Fecha'])

        # Escribir los datos de cada partida en el archivo CSV
        for fila in resultados:
            escritor_csv.writerow(fila)

    conn.close()

    # Mensaje de confirmación
    messagebox.showinfo("Éxito", f"Reporte generado: {nombre_archivo}")

# Función para manejar el evento de generación de reporte
def generar_reporte():
    try:
        usuario_id = int(entry_id_usuario.get())
        generar_reporte_csv(usuario_id)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido para el ID del usuario.")

# Crear la ventana principal de Tkinter
ventana = tk.Tk()
ventana.title("Generar Reporte CSV por Usuario")

# Etiqueta y campo para ingresar el ID del usuario
label_id_usuario = tk.Label(ventana, text="ID del Usuario:")
label_id_usuario.pack(pady=10)

entry_id_usuario = tk.Entry(ventana)
entry_id_usuario.pack(pady=5)

# Botón para generar el reporte CSV
boton_generar = tk.Button(ventana, text="Generar Reporte", command=generar_reporte)
boton_generar.pack(pady=20)

# Ejecutar la ventana
ventana.mainloop()
