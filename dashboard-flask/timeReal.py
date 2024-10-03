from flask import Flask, render_template, jsonify, request
import mysql.connector
import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="juego"
    )

def obtener_datos_estadisticas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT nombre_usuario, AVG(puntos) AS promedio_puntos, AVG(tiempo) AS promedio_tiempo, 
               MAX(distancia) AS maxima_distancia, COUNT(*) AS total_partidas,
               SUM(autos_esquivados) AS total_autos_esquivados, SUM(intentos) AS total_intentos
        FROM resultados_partida 
        GROUP BY nombre_usuario
    """)
    resultados = cursor.fetchall()

    jugadores = [fila[0] for fila in resultados]
    promedio_puntos = [fila[1] for fila in resultados]
    promedio_tiempo = [fila[2] for fila in resultados]
    maxima_distancia = [fila[3] for fila in resultados]
    total_partidas = [fila[4] for fila in resultados]
    total_autos_esquivados = [fila[5] for fila in resultados]
    total_intentos = [fila[6] for fila in resultados]

    cursor.close()
    conexion.close()

    return jugadores, promedio_puntos, promedio_tiempo, maxima_distancia, total_partidas, total_autos_esquivados, total_intentos

@app.route('/')
def index():
    return render_template('timeReal.html')

@app.route('/datos_grafico', methods=['GET'])
def datos_grafico():
    jugadores, promedio_puntos, promedio_tiempo, maxima_distancia, total_partidas, total_autos_esquivados, total_intentos = obtener_datos_estadisticas()

    # Gráfico 1: Promedio de Puntos por Jugador (línea)
    trace1 = go.Scatter(x=jugadores, y=promedio_puntos, mode='lines', name='Promedio de Puntos')

    # Gráfico 2: Promedio de Tiempo por Jugador (línea)
    trace2 = go.Scatter(x=jugadores, y=promedio_tiempo, mode='lines', name='Promedio de Tiempo')

    # Gráfico 3: Máxima Distancia por Jugador (línea)
    trace3 = go.Scatter(x=jugadores, y=maxima_distancia, mode='lines', name='Máxima Distancia')

    # Gráfico 4: Total de Partidas por Jugador (línea)
    trace4 = go.Scatter(x=jugadores, y=total_partidas, mode='lines', name='Total de Partidas')

    # Gráfico 5: Total de Autos Esquivados por Jugador (línea)
    trace5 = go.Scatter(x=jugadores, y=total_autos_esquivados, mode='lines', name='Total de Autos Esquivados')

    # Gráfico 6: Total de Intentos por Jugador (línea)
    trace6 = go.Scatter(x=jugadores, y=total_intentos, mode='lines', name='Total de Intentos')

    layout = go.Layout(
        title=f'Estadísticas de Jugadores - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        xaxis_title='Jugadores',
        yaxis_title='Estadísticas',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    fig = go.Figure(data=[trace1, trace2, trace3, trace4, trace5, trace6], layout=layout)
    graph_json = pio.to_json(fig)

    return jsonify(graph_json)

@app.route('/recibir_datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO resultados_partida (id_usuario, nombre_usuario, edad, distancia, puntos, tiempo, movimientos, autos_esquivados, intentos) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data['id_usuario'], data['nombre_usuario'], data['edad'], data['distancia'], data['puntos'], data['tiempo'], data['movimientos'], data['autos_esquivados'], data['intentos']))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
