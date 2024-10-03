import tkinter as tk
from tkinter import messagebox
import csv
import mysql.connector
from datetime import datetime  # Importar la librería para obtener fecha y hora

# Función para conectar a la base de datos
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='juego'
    )

# Función para generar reporte en CSV para un usuario específico
def generar_reporte_csv_usuario(usuario_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Consulta SQL para obtener todos los resultados de las partidas jugadas por el usuario
    cursor.execute("""
        SELECT id, id_usuario, nombre_usuario, edad, distancia, puntos, tiempo, movimientos, autos_esquivados, intentos
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

        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Escribir los encabezados de las columnas en el archivo CSV
        escritor_csv.writerow(['ID Partida', 'ID Usuario', 'Nombre Usuario', 'Edad', 'Distancia', 'Puntos', 'Tiempo', 'Movimientos', 'Autos Esquivados', 'Intentos', 'Fecha y Hora Generación'])

        # Escribir los datos de cada partida en el archivo CSV
        for fila in resultados:
            escritor_csv.writerow(list(fila) + [fecha_hora_actual])  # Añadir la fecha y hora actual al final de cada fila

    conn.close()

    # Mensaje de confirmación
    messagebox.showinfo("Éxito", f"Reporte generado: {nombre_archivo}")

# Función para generar reporte en CSV para todos los usuarios
def generar_reporte_csv_todos():
    conn = connect_db()
    cursor = conn.cursor()

    # Consulta SQL para obtener todos los resultados de las partidas jugadas
    cursor.execute("""
        SELECT id, id_usuario, nombre_usuario, edad, distancia, puntos, tiempo, movimientos, autos_esquivados, intentos
        FROM resultados_partida
    """)

    resultados = cursor.fetchall()

    if not resultados:
        messagebox.showinfo("Error", "No se encontraron partidas.")
        return

    # Definir el nombre del archivo CSV a generar
    nombre_archivo = 'reporte_todos_usuarios.csv'

    # Abrir o crear el archivo CSV para escribir los datos
    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)

        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Escribir los encabezados de las columnas en el archivo CSV
        escritor_csv.writerow(['ID Partida', 'ID Usuario', 'Nombre Usuario', 'Edad', 'Distancia', 'Puntos', 'Tiempo', 'Movimientos', 'Autos Esquivados', 'Intentos', 'Fecha y Hora Generación'])

        # Escribir los datos de cada partida en el archivo CSV
        for fila in resultados:
            escritor_csv.writerow(list(fila) + [fecha_hora_actual])  # Añadir la fecha y hora actual al final de cada fila

    conn.close()

    # Mensaje de confirmación
    messagebox.showinfo("Éxito", f"Reporte generado: {nombre_archivo}")

# Función para manejar el evento de generación de reporte por usuario
def generar_reporte_por_usuario():
    try:
        usuario_id = int(entry_id_usuario.get())
        generar_reporte_csv_usuario(usuario_id)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido para el ID del usuario.")

# Función para manejar el evento de generación de reporte para todos los usuarios
def generar_reporte_todos():
    generar_reporte_csv_todos()

# Función para cargar y mostrar la lista de usuarios
def cargar_lista_usuarios():
    conn = connect_db()
    cursor = conn.cursor()

    # Consulta para obtener todos los usuarios
    cursor.execute("SELECT id, nombre FROM usuarios")
    usuarios = cursor.fetchall()

    if not usuarios:
        messagebox.showinfo("Error", "No se encontraron usuarios.")
        return

    # Limpiar la lista antes de cargar
    lista_usuarios.delete(0, tk.END)

    # Agregar cada usuario a la lista
    for usuario in usuarios:
        lista_usuarios.insert(tk.END, f"ID: {usuario[0]}, Nombre: {usuario[1]}")

    conn.close()

# Función para manejar el evento de selección de un usuario en la lista
def seleccionar_usuario(event):
    seleccion = lista_usuarios.curselection()
    if seleccion:
        usuario_seleccionado = lista_usuarios.get(seleccion[0])
        # Extraer el ID del usuario seleccionado
        usuario_id = usuario_seleccionado.split(',')[0].split(':')[1].strip()
        entry_id_usuario.delete(0, tk.END)
        entry_id_usuario.insert(0, usuario_id)

# Crear la ventana principal de Tkinter
ventana = tk.Tk()
ventana.title("Generar Reporte CSV por Usuario o Todos")

# Etiqueta y campo para ingresar el ID del usuario
label_id_usuario = tk.Label(ventana, text="ID del Usuario:")
label_id_usuario.pack(pady=10)

entry_id_usuario = tk.Entry(ventana)
entry_id_usuario.pack(pady=5)

# Listbox para mostrar la lista de usuarios
label_lista_usuarios = tk.Label(ventana, text="Selecciona un usuario de la lista:")
label_lista_usuarios.pack(pady=10)

lista_usuarios = tk.Listbox(ventana, height=10, width=50)
lista_usuarios.pack(pady=5)
lista_usuarios.bind('<<ListboxSelect>>', seleccionar_usuario)

# Botón para cargar la lista de usuarios
boton_cargar_lista = tk.Button(ventana, text="Cargar Lista de Usuarios", command=cargar_lista_usuarios)
boton_cargar_lista.pack(pady=5)

# Botón para generar el reporte CSV por usuario
boton_generar_usuario = tk.Button(ventana, text="Generar por Usuario", command=generar_reporte_por_usuario)
boton_generar_usuario.pack(pady=5)

# Botón para generar el reporte CSV para todos los usuarios
boton_generar_todos = tk.Button(ventana, text="Generar Todos", command=generar_reporte_todos)
boton_generar_todos.pack(pady=20)

# Ejecutar la ventana
ventana.mainloop()
