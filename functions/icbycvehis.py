from flask import Blueprint, render_template, request, redirect, url_for, flash
import pandas as pd
import os
from datetime import datetime, timedelta

# Crear un Blueprint
icbycvehis_bp = Blueprint('icbycvehis', __name__, template_folder='../templates')

# Configuración de rutas de archivos
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'data', 'componentes_base_variable.csv')
HISTORICO_CSV_FILE = os.path.join(BASE_DIR, 'data', 'historico_componentes.csv')

# Lista de combustibles
COMBUSTIBLES = [
    "Gasolina Automotriz de 93 octanos (en UTM/m3)",
    "Gasolina Automotriz de 97 octanos (en UTM/m3)",
    "Petroleo Diesel (en UTM/m3)",
    "Gas Licuado del Petroleo de Consumo Vehicular (en UTM/m3)",
    "Gas Natural Comprimido de Consumo Vehicular (en UTM/1000m3)"
]

# Funciones auxiliares (sin cambios)
def cargar_datos():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, index_col=0)
        if 'Fecha de Actualizacion' not in df.columns:
            df['Fecha de Actualizacion'] = ''
        if 'Vigencia Desde' not in df.columns:
            df['Vigencia Desde'] = ''
        return df
    else:
        return pd.DataFrame(columns=["Componente Base", "Componente Variable", "Impuesto Especifico", "Fecha de Actualizacion", "Vigencia Desde"])

def guardar_datos(df, vigencia_fecha):
    fecha_actualizacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    df["Fecha de Actualizacion"] = fecha_actualizacion
    df["Vigencia Desde"] = vigencia_fecha
    df["Componente Base"] = df["Componente Base"].round(4)
    df["Componente Variable"] = df["Componente Variable"].round(4)
    df["Impuesto Especifico"] = df["Impuesto Especifico"].round(4)
    df.to_csv(CSV_FILE, float_format="%.4f")

    for combustible in COMBUSTIBLES:
        if combustible in df.index:
            base = df.at[combustible, "Componente Base"]
            variable = df.at[combustible, "Componente Variable"]
            impuesto = df.at[combustible, "Impuesto Especifico"]
            vigencia_desde = df.at[combustible, "Vigencia Desde"]

            historial = {
                "Fecha de Modificación": fecha_actualizacion,
                "Componente Base": base,
                "Componente Variable": variable,
                "Impuesto Especifico": impuesto,
                "Vigencia Desde": vigencia_desde
            }

            historial_df = pd.DataFrame([historial])

            if os.path.exists(HISTORICO_CSV_FILE):
                historial_df.to_csv(HISTORICO_CSV_FILE, mode='a', header=False, index=False)
            else:
                historial_df.to_csv(HISTORICO_CSV_FILE, mode='w', header=True, index=False)

def calcular_vigencia_hasta(fecha_vigencia):
    vigencia_date = datetime.strptime(fecha_vigencia, "%d/%m/%Y")
    days_until_wednesday = (2 - vigencia_date.weekday()) % 7
    fecha_fin = vigencia_date + timedelta(days=days_until_wednesday)
    return fecha_fin.strftime("%d/%m/%Y")

# Rutas del Blueprint
@icbycvehis_bp.route('/', methods=['GET', 'POST'])
def index():
    df = cargar_datos()
    vigencia_fecha = df['Vigencia Desde'].iloc[0] if not df.empty and 'Vigencia Desde' in df.columns else ''
    fecha_vigencia_hasta = calcular_vigencia_hasta(vigencia_fecha) if vigencia_fecha else "No disponible"

    if request.method == 'POST':
        vigencia_fecha = request.form.get('vigencia_fecha')
        for combustible in COMBUSTIBLES:
            base = float(request.form.get(f'base_{combustible}', 0))
            variable = float(request.form.get(f'variable_{combustible}', 0))
            impuesto = base + variable

            if combustible not in df.index:
                df.loc[combustible] = [0, 0, 0, '', '']

            df.at[combustible, "Componente Base"] = base
            df.at[combustible, "Componente Variable"] = variable
            df.at[combustible, "Impuesto Especifico"] = impuesto

        guardar_datos(df, vigencia_fecha)
        flash('Datos guardados con éxito!', 'success')
        return redirect(url_for('icbycvehis.index'))

    return render_template('icbycvehis.html', combustibles=COMBUSTIBLES, data=df, vigencia_fecha=vigencia_fecha, fecha_vigencia_hasta=fecha_vigencia_hasta)
