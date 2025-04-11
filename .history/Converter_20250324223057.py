import tkinter as tk
from tkinter import filedialog, ttk
import time
import ezdxf.colors
import utm
import ezdxf
from fastkml import kml
import os
import pandas as pd
import xml.etree.ElementTree as ET
import os
import psutil
import uuid
from transforma import transformar_archivo_kml


def carga_programa():
    # Simula la carga del programa
    for i in range(100):
        barra_progreso['value'] = i
        etiqueta_progreso['text'] = f"Cargando... {i}%"
        ventana.update_idletasks()
        time.sleep(0.1)  # Simula la carga
       # Cierra la ventana de carga
    ventana.destroy()

ventana = tk.Tk()
ventana.geometry("800x100")
ventana.title("Cargando programa")
# Crea la etiqueta de progreso
etiqueta_progreso = tk.Label(ventana, text="Cargando.", font=("Arial", 12))
etiqueta_progreso.pack(pady=20)

# Crea la barra de progreso
barra_progreso = ttk.Progressbar(ventana, orient="horizontal",length=600, mode="determinate")
barra_progreso.pack(pady=20)

# Llama a la función de carga del programa
carga_programa()

# Inicia el bucle principal de la ventana
ventana.mainloop()

def seleccionar_archivo_kml():
    ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])
    entrada_archivo_kml.delete(0, tk.END)
    entrada_archivo_kml.insert(tk.END, ruta_archivo_kml)
    return ruta_archivo_kml, entrada_archivo_kml


# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Transformar archivo KML a UTM")


# Crear las etiquetas y entradas para la ruta del archivo KML
etiqueta_archivo_kml = tk.Label(ventana_principal, text="Ruta del archivo KML:")
entrada_archivo_kml = tk.Entry(ventana_principal, width=50)
boton_seleccionar_archivo_kml = tk.Button(ventana_principal, text="Seleccionar archivo", command=seleccionar_archivo_kml)


# Crear el botón para transformar el archivo
boton_transformar_archivo = tk.Button(ventana_principal, text="Transformar archivo", command=lambda: transformar_archivo_kml)

# Colocar los elementos en la ventana principal
etiqueta_archivo_kml.grid(row=0, column=0, padx=5, pady=5)
entrada_archivo_kml.grid(row=0, column=1, padx=5, pady=5)
boton_seleccionar_archivo_kml.grid(row=0, column=2, padx=5, pady=5)
boton_transformar_archivo.grid(row=2, column=1, padx=5, pady=5)

ventana_principal.mainloop()