import tkinter as tk
import subprocess
import os

# Función para ejecutar el módulo utmtc.py
def ejecutar_utmtc():
    try:
        # Ejecutar el script utmtc.py desde la ruta './funciones/utmtc.py'
        subprocess.run(['python', './funciones/utmtc.py'], check=True)
        print("Módulo utmtc.py ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar utmtc.py: {e}")
    except FileNotFoundError:
        print("No se encontró el archivo utmtc.py.")
        
# Función para ejecutar el módulo icbycvehis.py
def ejecutar_icbycvehis():
    try:
        # Ejecutar el script icbycvehis.py desde la ruta './funciones/icbycvehis.py'
        subprocess.run(['python', './funciones/icbycvehis.py'], check=True)
        print("Módulo icbycvehis.py ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar icbycvehis.py: {e}")
    except FileNotFoundError:
        print("No se encontró el archivo icbycvehis.py.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mantenedores")

# Configurar el tamaño de la ventana
ventana.geometry("300x200")

# Crear un label de bienvenida
label_bienvenida = tk.Label(ventana, text="Menu de Mantenedores", font=("Arial", 14))
label_bienvenida.pack(pady=20)

# Crear un botón para ejecutar utmtc.py
boton_utmtc = tk.Button(ventana, text="UTM y TC", command=ejecutar_utmtc, width=25, height=2)
boton_utmtc.pack(pady=10)

# Crear un botón para ejecutar icbycvehis.py
boton_icbycvehis = tk.Button(ventana, text="Componentes Base y Variable", command=ejecutar_icbycvehis, width=25, height=2)
boton_icbycvehis.pack(pady=10)

# Ejecutar la interfaz gráfica
ventana.mainloop()
