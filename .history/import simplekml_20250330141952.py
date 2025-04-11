import simplekml
import requests
import tkinter as tk
from tkinter import filedialog, ttk


def seleccionar_archivo_kml():
    ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])
    entrada_archivo_kml.delete(0, tk.END)
    entrada_archivo_kml.insert(tk.END, ruta_archivo_kml)  
    
    return ruta_archivo_kml


def obtener_elevacion(latitud, longitud):
    """
    Obtiene la elevación de un punto dado su longitud y latitud.

    Args:
        latitud (float): La latitud del punto.
        longitud (float): La longitud del punto.

    Returns:
        float: La elevación del punto en metros.
    """
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={latitud},{longitud}"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        elevacion = datos["results"][0]["elevation"]
        return elevacion
    else:
        return None

def obtener_altitud_desde_kml(ruta_archivo_kml):
    """
    Obtiene la altitud de cada punto en un archivo KML.

    Args:
        ruta_archivo_kml (str): La ruta del archivo KML.

    Returns:
        dict: Un diccionario con la longitud, latitud y altitud de cada punto.
    """
    
    ruta_archivo_kml = entrada_archivo_kml.get()
    
    kml = simplekml.Kml()
    kml.open(ruta_archivo_kml)

    puntos = {}

    for folder in kml.features():
        for placemark in folder.features():
            for geom in placemark.geometry.geoms:
                if geom.type == "LineString":
                    for coord in geom.coords:
                        latitud = coord[1]
                        longitud = coord[0]
                        altitud = obtener_elevacion(latitud, longitud)
                        puntos[(latitud, longitud)] = altitud

    return puntos

# Ejemplo de uso
ruta_archivo_kml = "archivo.kml"
puntos = obtener_altitud_desde_kml(ruta_archivo_kml)

for punto, altitud in puntos.items():
    print(f"Latitud: {punto[0]}, Longitud: {punto[1]}, Altitud: {altitud} metros")
    
    
# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Transformar archivo KML a UTM")


# Crear las etiquetas y entradas para la ruta del archivo KML
etiqueta_archivo_kml = tk.Label(ventana_principal, text="Ruta del archivo KML:")
entrada_archivo_kml = tk.Entry(ventana_principal, width=50)
boton_seleccionar_archivo_kml = tk.Button(ventana_principal, text="Seleccionar archivo", command=seleccionar_archivo_kml)



# Crear el botón para transformar el archivo
boton_transformar_archivo = tk.Button(ventana_principal, text="Transformar archivo",
                                      command=lambda: obtener_altitud_desde_kml(entrada_archivo_kml))

# Colocar los elementos en la ventana principal
etiqueta_archivo_kml.grid(row=0, column=0, padx=5, pady=5)

entrada_archivo_kml.grid(row=0, column=1, padx=5, pady=5)
boton_seleccionar_archivo_kml.grid(row=0, column=2, padx=5, pady=5)
boton_transformar_archivo.grid(row=2, column=1, padx=5, pady=5)

ventana_principal.mainloop()