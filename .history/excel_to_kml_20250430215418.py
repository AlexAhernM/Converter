import pandas as pd
from pyproj import Transformer
import simplekml
import customtkinter
from customtkinter import filedialog
import tkinter as tk
from tkinter import ttk


def select_file(self):
    ruta_archivo_excel = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivo XLXS", "*.xlxs")])
    self.selectdata_entry.delete(0, customtkinter.END)
    self.selectdata_entry.insert(customtkinter.END, ruta_archivo_excel)
    
    return ruta_archivo_excel

# Leer el archivo Excel
df = pd.read_excel('ruta_archivo_excel')


# Definir el sistema de coordenadas UTM y el sistema de coordenadas geográficas
utm_crs = "EPSG:32719"  # Reemplaza con el código EPSG correspondiente a tu zona UTM
geo_crs = "EPSG:4326"  # WGS84

# Crear un objeto Transformer para realizar la conversión de coordenadas
transformer = Transformer.from_crs(utm_crs, geo_crs, always_xy=True)

# Convertir las coordenadas UTM a geográficas
df['lon'], df['lat'] = transformer.transform(df['Este'], df['Norte'])

# Función para crear el archivo KML
def crear_kml():
    tipo = tipo_var.get()
    if tipo == "Puntos":
        kml = simplekml.Kml()
        for index, row in df.iterrows():
            kml.newpoint(name=row['Nombre'], coords=[(row['lon'], row['lat'])])
    elif tipo == "Polilínea":
        kml = simplekml.Kml()
        coords = [(row['lon'], row['lat']) for index, row in df.iterrows()]
        kml.newlinestring(name="Polilínea", coords=coords)
    kml.save('coordenadas.kml')

# Crear la GUI
root = tk.Tk()
root.title("Crear archivo KML")

tipo_var = tk.StringVar()
tipo_var.set("Puntos")

tipo_frame = ttk.Frame(root)
tipo_frame.pack(padx=10, pady=10)

ttk.Radiobutton(tipo_frame, text="Puntos", variable=tipo_var, value="Puntos").pack(side=tk.LEFT)
ttk.Radiobutton(tipo_frame, text="Polilínea", variable=tipo_var, value="Polilínea").pack(side=tk.LEFT)

crear_button = ttk.Button(root, text="Crear archivo KML", command=crear_kml)
crear_button.pack(padx=10, pady=10)

root.mainloop()