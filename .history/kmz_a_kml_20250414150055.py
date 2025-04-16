import tkinter as tk
from tkinter import filedialog
import zipfile
import xml.etree.ElementTree as ET

def seleccionar_archivo():
    archivo_kmz = filedialog.askopenfilename(title="Seleccione un archivo KMZ", filetypes=[("Archivos KMZ", "*.kmz")])
    if archivo_kmz:
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, archivo_kmz)

def procesar_archivo():
    archivo_kmz = entry_archivo.get()
    if archivo_kmz:
        try:
            with zipfile.ZipFile(archivo_kmz, 'r') as kmz:
                kml_data = kmz.read('doc.kml')
            root = ET.fromstring(kml_data)
            has_elevation = False
            for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
                geometry = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates')
                if geometry is not None:
                    coords = geometry.text.strip().split()
                    for coord in coords:
                        values = coord.split(',')
                        if len(values) == 3:  # longitude, latitude, altitude
                            has_elevation = True
                            break
                    if has_elevation:
                        break
            resultado.set(f"El archivo KML {'tiene' if has_elevation else 'no tiene'} atributos de elevación")
            with open('archivo.kml', 'wb') as kml_file:
                kml_file.write(kml_data)
        except Exception as e:
            resultado.set(f"Error: {str(e)}")
    else:
        resultado.set("Por favor, seleccione un archivo KMZ")

root = tk.Tk()
root.title("Convertidor KMZ a KML")

label_archivo = tk.Label(root, text="Archivo KMZ:")
label_archivo.grid(row=0, column=0, padx=5, pady=5)

entry_archivo = tk.Entry(root, width=50)
entry_archivo.grid(row=0, column=1, padx=5, pady=5)

boton_seleccionar = tk.Button(root, text="Seleccionar", command=seleccionar_archivo)
boton_seleccionar.grid(row=0, column=2, padx=5, pady=5)

boton_procesar = tk.Button(root, text="Procesar", command=procesar_archivo)
boton_procesar.grid(row=1, column=1, padx=5, pady=5)

resultado = tk.StringVar()
label_resultado = tk.Label(root, textvariable=resultado)
label_resultado.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()