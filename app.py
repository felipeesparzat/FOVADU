from flask import Flask, render_template, redirect, url_for
from functions.icbycvehis import icbycvehis_bp

app = Flask(__name__,template_folder='./templates')
app.secret_key = 'your_secret_key'

app.register_blueprint(icbycvehis_bp, url_prefix='/icbycvehis')

# Página de inicio
@app.route('/')
def home():
    return render_template('index.html')  # Asegúrate de tener un index.html en /templates

# Ruta para el módulo UTM/TC
@app.route('/utm_tc')
def utm_tc():
    import functions.utm_tc as utm_tc_module
    return utm_tc_module.index()  # Asegúrate de que utm_tc.py tenga una función index()

# Ruta para el módulo Componente Combustible
@app.route('/icbycvehis')
def icbycvehis():
    import functions.icbycvehis as icbycvehis_module
    return icbycvehis_module.index()  # Asegúrate de que icbycvehis.py tenga una función index()

if __name__ == '__main__':
    app.run(debug=True)
