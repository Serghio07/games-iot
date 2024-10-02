from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Función para conectarse a la base de datos
def connect_db():
    return mysql.connector.connect(
        host='localhost',    # Cambia esto si tu base de datos está en otro servidor
        user='root',
        password='',
        database='juego'
    )

# Ruta principal del dashboard
@app.route("/")
def dashboard():
    conn = connect_db()
    cursor = conn.cursor()

    # Consulta SQL para obtener estadísticas de rendimiento por jugador
    cursor.execute("""
        SELECT nombre_usuario, AVG(puntos) AS promedio_puntos, AVG(tiempo) AS promedio_tiempo, 
               MAX(distancia) AS maxima_distancia, COUNT(*) AS total_partidas 
        FROM resultados_partida 
        GROUP BY nombre_usuario
    """)
    stats = cursor.fetchall()

    conn.close()

    # Pasar las estadísticas obtenidas a la plantilla HTML
    return render_template('timeReal.html', stats=stats)

# Iniciar el servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
