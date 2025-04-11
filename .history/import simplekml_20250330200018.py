import requests
import tkinter as tk
from tkinter import filedialog, ttk


def seleccionar_archivo_kml():
    ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])
    entrada_archivo_kml.delete(0, tk.END)
    entrada_archivo_kml.insert(tk.END, ruta_archivo_kml)  
    
    return ruta_archivo_kml


import xml.etree.ElementTree as ET
import requests

def obtener_altitud_desde_kml(entrada_archivo_kml):
    
    ruta_archivo_kml = entrada_archivo_kml.get()
    

    try:
            tree = ET.parse(ruta_archivo_kml)
            
            root = tree.getroot()

        
            elevaciones_api = []
            for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
                for line_string in placemark.findall('.//{http://www.opengis.net/kml/2.2}LineString'):
                    print("Encontrado un LineString")
                    coordenadas = line_string.find('{http://www.opengis.net/kml/2.2}coordinates')
                    if coordenadas is not None:
                        
                        valores_coordenadas = coordenadas.text.split()
                        for valor_coordenada in valores_coordenadas:
                            longitud, latitud, altitud = valor_coordenada.split(',')

                            # Obtener la altitud utilizando la API de Open-Elevation
                            url = f"https://api.open-elevation.com/api/v1/lookup?locations={latitud},{longitud}"
                            respuesta = requests.get(url)
                            
                            if respuesta.status_code == 200:
                                datos = respuesta.json()
                                altitud_api = round(datos["results"][0]["elevation"], 2)
                                elevaciones_api.append((latitud, longitud, altitud_api))
                                

    # Imprimir los resultados con la función print
            print("Resultados:")
            for punto in elevaciones_api:
                print(f"Latitud: {punto[0]}, Longitud: {punto[1]}, Altitud: {punto[2]:.2f} metros")
               
#De esta manera, se crea una nueva lista llamada elevaciones_api que almacena las elevaciones obtenidas desde la API para cada punto. Luego, se imprimen los resultados utilizando esta lista.

    except Exception as e:
        print("Error:", str(e))
    



# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Transformar archivo KML a UTM")


# Crear las etiquetas y entradas para la ruta del archivo KML
etiqueta_archivo_kml = tk.Label(ventana_principal, text="Ruta del archivo KML:")
entrada_archivo_kml = tk.Entry(ventana_principal, width=50)
boton_seleccionar_archivo_kml = tk.Button(ventana_principal, text="Seleccionar archivo", command=seleccionar_archivo_kml)


# Crear el botón para transformar el archivo
boton_transformar_archivo = tk.Button(ventana_principal, text="Obtener Altitud",
                                      command=lambda: obtener_altitud_desde_kml(entrada_archivo_kml))

# Crear la etiqueta para mostrar los resultados
etiqueta_resultados = tk.Label(ventana_principal, text="", wraplength=400)


# Colocar los elementos en la ventana principal
etiqueta_archivo_kml.grid(row=0, column=0, padx=5, pady=5)

entrada_archivo_kml.grid(row=0, column=1, padx=5, pady=5)
boton_seleccionar_archivo_kml.grid(row=0, column=2, padx=5, pady=5)
boton_transformar_archivo.grid(row=2, column=1, padx=5, pady=5)

ventana_principal.mainloop()