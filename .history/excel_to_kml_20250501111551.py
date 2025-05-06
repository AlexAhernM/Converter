import pandas as pd
from pyproj import Transformer
import simplekml
import customtkinter
from customtkinter import filedialog
import tkinter as tk
from tkinter import ttk


def select_file():
    ruta_archivo_excel = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivo XLSX", "*.xlsx")])
    kml_entry.delete(0, customtkinter.END)
    kml_entry.insert(customtkinter.END, ruta_archivo_excel)
    
    return ruta_archivo_excel

# Función para crear el archivo KML
def crear_kml():
    ruta_archivo_excel = kml_entry.get()
    print (ruta_archivo_excel)
    df = pd.read_excel(ruta_archivo_excel)

    # Definir el sistema de coordenadas UTM y el sistema de coordenadas geográficas
    utm_crs = "EPSG:32719"  # Reemplaza con el código EPSG correspondiente a tu zona UTM
    geo_crs = "EPSG:4326"  # WGS84

    # Crear un objeto Transformer para realizar la conversión de coordenadas
    transformer = Transformer.from_crs(utm_crs, geo_crs, always_xy=True)

    
    if tipo_coordenadas == "grados":
        df['lon'] = df.iloc[:, 0]  # Columna A
        df['lat'] = df.iloc[:, 1]  # Columna B
    else:
        transformer = Transformer.from_crs(utm_crs, geo_crs, always_xy=True)
        df['lon'], df['lat'] = transformer.transform(df.iloc[:, 0], df.iloc[:, 1])
        # Convertir las coordenadas UTM a geográficas
        df['lon'], df['lat'] = transformer.transform(df['Este'], df['Norte'])
    
    
    
      
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
app = customtkinter.CTk()
app.geometry("600x500")
app.title("CTk Excel_to_KLM")

tipo_var = customtkinter.StringVar()
tipo_var.set("Puntos")

tipo_frame = customtkinter.CTkFrame(app)


kml_puntos= customtkinter.CTkRadioButton(tipo_frame, text="Puntos", variable=tipo_var, value="Puntos")
kml_puntos.pack(side=tk.LEFT)

kml_poliln= customtkinter.CTkRadioButton(tipo_frame, text="Polilínea", variable=tipo_var, value="Polilínea")
kml_poliln.pack(side=tk.LEFT)

select_boton = customtkinter.CTkButton(app, text='Select File', command= select_file)
select_boton.grid(row=0, column=0, padx=10, pady=10, sticky ='w')

kml_entry = customtkinter.CTkEntry(app)
kml_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

crear_button = customtkinter.CTkButton(app, text="Crear archivo KML", command=crear_kml)
crear_button.grid(row=1, column=0, padx=10, pady=10, sticky ='ew', columnspan = 2)

app.mainloop()