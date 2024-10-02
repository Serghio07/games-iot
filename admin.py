import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Conexión a la base de datos
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='juego'
    )

# Crear ventana principal
root = tk.Tk()
root.title("CRUD de Usuarios")
root.geometry("500x400")

# Función para crear un nuevo usuario
def crear_usuario():
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    correo = entry_correo.get()
    contraseña = entry_contraseña.get()

    if nombre and edad.isdigit() and correo and contraseña:
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, edad, correo, contraseña) VALUES (%s, %s, %s, %s)", 
                           (nombre, edad, correo, contraseña))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario creado con éxito.")
            limpiar_campos()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al crear usuario: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios y la edad debe ser un número.")

# Función para leer la información de un usuario por ID
def leer_usuario():
    usuario_id = entry_id.get()
    if usuario_id.isdigit():
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
            usuario = cursor.fetchone()
            if usuario:
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, usuario[1])
                entry_edad.delete(0, tk.END)
                entry_edad.insert(0, usuario[2])
                entry_correo.delete(0, tk.END)
                entry_correo.insert(0, usuario[3])
                entry_contraseña.delete(0, tk.END)
                entry_contraseña.insert(0, usuario[4])
            else:
                messagebox.showwarning("Advertencia", "Usuario no encontrado.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al leer usuario: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Advertencia", "El ID debe ser un número.")

# Función para actualizar un usuario
def actualizar_usuario():
    usuario_id = entry_id.get()
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    correo = entry_correo.get()
    contraseña = entry_contraseña.get()

    if usuario_id.isdigit() and nombre and edad.isdigit() and correo and contraseña:
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE usuarios SET nombre = %s, edad = %s, correo = %s, contraseña = %s WHERE id = %s", 
                           (nombre, edad, correo, contraseña, usuario_id))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Usuario actualizado con éxito.")
                limpiar_campos()
            else:
                messagebox.showwarning("Advertencia", "Usuario no encontrado.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar usuario: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios y deben ser válidos.")

# Función para eliminar un usuario
def eliminar_usuario():
    usuario_id = entry_id.get()
    if usuario_id.isdigit():
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Usuario eliminado con éxito.")
                limpiar_campos()
            else:
                messagebox.showwarning("Advertencia", "Usuario no encontrado.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar usuario: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Advertencia", "El ID debe ser un número.")

# Función para listar todos los usuarios
def listar_usuarios():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        if usuarios:
            listado = ""
            for usuario in usuarios:
                listado += f"ID: {usuario[0]}, Nombre: {usuario[1]}, Edad: {usuario[2]}, Correo: {usuario[3]}\n"
            messagebox.showinfo("Usuarios", listado)
        else:
            messagebox.showinfo("Usuarios", "No hay usuarios registrados.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al listar usuarios: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para limpiar los campos de entrada
def limpiar_campos():
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)

# Crear la interfaz de usuario con Tkinter
tk.Label(root, text="ID de Usuario").grid(row=0, column=0, padx=10, pady=5)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Nombre").grid(row=1, column=0, padx=10, pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Edad").grid(row=2, column=0, padx=10, pady=5)
entry_edad = tk.Entry(root)
entry_edad.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Correo").grid(row=3, column=0, padx=10, pady=5)
entry_correo = tk.Entry(root)
entry_correo.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Contraseña").grid(row=4, column=0, padx=10, pady=5)
entry_contraseña = tk.Entry(root, show="*")
entry_contraseña.grid(row=4, column=1, padx=10, pady=5)

# Botones CRUD
tk.Button(root, text="Crear Usuario", command=crear_usuario).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="Leer Usuario", command=leer_usuario).grid(row=5, column=1, padx=10, pady=10)
tk.Button(root, text="Actualizar Usuario", command=actualizar_usuario).grid(row=6, column=0, padx=10, pady=10)
tk.Button(root, text="Eliminar Usuario", command=eliminar_usuario).grid(row=6, column=1, padx=10, pady=10)
tk.Button(root, text="Listar Usuarios", command=listar_usuarios).grid(row=7, column=0, columnspan=2, pady=10)

# Iniciar la interfaz gráfica
root.mainloop()
