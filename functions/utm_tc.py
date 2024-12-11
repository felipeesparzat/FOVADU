from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))

# Crear directorio si no existe
if not os.path.exists('./data'):
    os.makedirs('./data')

# Lista de meses y años para los desplegables
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
años = [str(año) for año in range(2024, 2026)]  # Años de 2024 a 2025


# Función para cargar los datos del mes y año seleccionados
def cargar_datos_mes_año(mes, año):
    archivo_existe = os.path.exists('./data/utm_tc.csv')
    if archivo_existe:
        with open('./data/utm_tc.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            registros = list(reader)
            for fila in registros:
                if fila[0] == mes and fila[1] == año:
                    return {"utm": fila[2], "tipo_cambio": fila[3]}
    return {"utm": "", "tipo_cambio": ""}


# Función para guardar los datos en el archivo CSV
def guardar_datos(mes, año, utm, tipo_cambio):
    try:
        utm_valor = float(utm)
        tipo_cambio_valor = float(tipo_cambio)

        registros = []
        archivo_existe = os.path.exists('./data/utm_tc.csv')
        if archivo_existe:
            with open('./data/utm_tc.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                registros = list(reader)

        encontrado = False
        for i, fila in enumerate(registros):
            if fila[0] == mes and fila[1] == año:
                registros[i] = [mes, año, utm_valor, tipo_cambio_valor]
                encontrado = True
                break

        if not encontrado:
            registros.append([mes, año, utm_valor, tipo_cambio_valor])

        with open('./data/utm_tc.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(registros)

        return {"success": True, "message": "Datos guardados correctamente."}

    except ValueError:
        return {"success": False, "message": "Por favor, ingrese valores válidos."}


@app.route('/')
def index():
    mes_actual = datetime.now().month - 1
    año_actual = datetime.now().year
    return render_template('utm_tc.html', meses=meses, años=años, mes_actual=mes_actual, año_actual=año_actual)


@app.route('/cargar', methods=['POST'])
def cargar():
    data = request.json
    mes = data.get('mes')
    año = data.get('año')
    return jsonify(cargar_datos_mes_año(mes, año))


@app.route('/guardar', methods=['POST'])
def guardar():
    data = request.json
    mes = data.get('mes')
    año = data.get('año')
    utm = data.get('utm', "0")
    tipo_cambio = data.get('tipo_cambio', "0")
    resultado = guardar_datos(mes, año, utm, tipo_cambio)
    return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)
