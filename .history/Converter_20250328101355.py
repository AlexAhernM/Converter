import tkinter as tk
from tkinter import filedialog, ttk
import time
import pyproj
from pyproj import Transformer
from fastkml import kml
import threading
from transforma import transformar_archivo_kml


def seleccionar_archivo_kml():
    ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])
    entrada_archivo_kml.delete(0, tk.END)
    entrada_archivo_kml.insert(tk.END, ruta_archivo_kml)  
    with open('archivo.kml', 'r') as f:
        kml_data = kml.KML()
        kml_data.from_string(f.read())
        
    # Obtener la zona y hemisferio del archivo KML
    zone, hemisphere = None, None
    for feature in kml_data.features():

        if feature.geometry is not None:
            zone, hemisphere = feature.geometry.coords[0][0], feature.geometry.coords[0][1]
            

    # Definir el sistema de coordenadas de origen (WGS 1984) y destino (UTM)
    src_crs = 'EPSG:4326'  # WGS 1984
    dst_crs = f'EPSG:327{zone}{hemisphere}'  # UTM

    # Crear un transformador de coordenadas
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    print (ruta_archivo_kml, entrada_archivo_kml)
    return ruta_archivo_kml, transformer
    
def carga_programa():
    for i in range(100):
        # En lugar de actualizar la GUI directamente, utilizamos el método after
        ventana.after(0, actualizar_progreso, i)
        time.sleep(0.1)
    ventana.destroy()
    
def actualizar_progreso(i):
    barra_progreso['value'] = i
    etiqueta_progreso['text'] = f"Loading... {i}%"

ventana = tk.Tk()
ventana.title ("Gis Converter Program ...Progress")
barra_progreso = ttk.Progressbar(ventana, orient="horizontal", length=600, mode="determinate")
barra_progreso.pack(pady=20)
etiqueta_progreso = tk.Label(ventana, text="Loading....", font=("Arial", 12))
etiqueta_progreso.pack(pady=20)

hilo_carga = threading.Thread(target=carga_programa)
hilo_carga.start()

ventana.mainloop()



# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Transformar archivo KML a UTM")


# Crear las etiquetas y entradas para la ruta del archivo KML
etiqueta_archivo_kml = tk.Label(ventana_principal, text="Ruta del archivo KML:")
entrada_archivo_kml = tk.Entry(ventana_principal, width=50)
boton_seleccionar_archivo_kml = tk.Button(ventana_principal, text="Seleccionar archivo", command=seleccionar_archivo_kml)



# Crear el botón para transformar el archivo
boton_transformar_archivo = tk.Button(ventana_principal, text="Transformar archivo",
command=lambda: transformar_archivo_kml(entrada_archivo_kml))

# Colocar los elementos en la ventana principal
etiqueta_archivo_kml.grid(row=0, column=0, padx=5, pady=5)

entrada_archivo_kml.grid(row=0, column=1, padx=5, pady=5)
boton_seleccionar_archivo_kml.grid(row=0, column=2, padx=5, pady=5)
boton_transformar_archivo.grid(row=2, column=1, padx=5, pady=5)

ventana_principal.mainloop()