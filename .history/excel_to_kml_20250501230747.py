import pandas as pd
from pyproj import Transformer
import simplekml
import os
import customtkinter as ctk
from customtkinter import filedialog
    

# Crear la GUI

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x900")
        self.title("coordinate converter")

        self.tipo_geo = ctk.StringVar()
        self.tipo_geo.set("Puntos")
        self.tipo_geo.set("Polilínea")
        
        self.tipo_coords = ctk.StringVar()
        self.tipo_coords.set("decimales")
        self.tipo_coords.set("utm")

        self.frame_utm = ctk.CTkFrame(self)
        self.frame_utm.grid(row=0, column=2, padx=10, pady=10, sticky ='w')
        

        self.kml_puntos= ctk.CTkRadioButton(self, text="Puntos", variable=self.tipo_geo, value="Puntos")
        self.kml_puntos.grid(row=0, column=0, padx=10, pady=10, sticky ='w')

        self.kml_poliln= ctk.CTkRadioButton(self, text="Polilínea", variable=self.tipo_geo, value="Polilínea")
        self.kml_poliln.grid(row=0, column=1, padx=10, pady=10, sticky ='w')

        self.zona_label = ctk.CTkLabel(self.frame_utm, text="Zona:")
        self.zona_label.grid(row=0, column = 4,padx=10, pady=10, sticky ='w' )
        self.zona_listbox = ctk.CTkComboBox(self.frame_utm, values=[str(i) for i in range(1, 61)])
        self.zona_listbox.set("Zona")
        self.zona_listbox.bind("<<ComboboxSelected>>", lambda event: self.hemisferio_listbox.configure(state="normal"))
        self.zona_listbox.configure(state="disabled")
        self.zona_listbox.grid(row=1, column = 4,padx=10, pady=10, sticky ='w') 

        self.hemisferio_label = ctk.CTkLabel(self.frame_utm, text="Hemisferio:")
        self.hemisferio_label.grid(row=0, column = 5,padx=10, pady=10, sticky ='w' )
        self.hemisferio_listbox = ctk.CTkComboBox(self.frame_utm, values=["Northern", "Southern"])
        self.hemisferio_listbox.set("Hemisferio")
        self.hemisferio_listbox.bind("<<ComboboxSelected>>", lambda event: self.zona_listbox.configure(state="normal"))
        self.hemisferio_listbox.configure(state="disabled")
        self.hemisferio_listbox.grid(row=1, column = 5,padx=10, pady=10, sticky ='w' )

        self.select_boton = ctk.CTkButton(self, text='Select File', command=lambda: select_file(self))
        self.select_boton.grid(row=1, column=0, padx=10, pady=10, sticky ='w')
        
        
        self.kml_entry = ctk.CTkEntry(self)
        self.kml_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.kml_dec_radio  = ctk.CTkRadioButton(self, text="Coordenadas decimales", variable=self.tipo_coords, value="decimales")
        self.kml_dec_radio.grid(row=1, column = 0, padx=10, pady=10, sticky='w')

        self.kml_utm_radio = ctk.CTkRadioButton(self.frame_utm, text="Coordenadas UTM", variable=self.tipo_coords, value="utm")
        self.kml_utm_radio.grid(row=1, column = 1, padx=10, pady=10, sticky='w')
        

        self.crear_button = ctk.CTkButton(self, text="Crear archivo KML", command= lambda: crear_kml(self))
        self.crear_button.grid(row=2, column=0, padx=10, pady=10, sticky ='ew', columnspan = 2)
        
        
def select_file(self):
    ruta_archivo_excel = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivo XLSX", "*.xlsx")])
    self.kml_entry.delete(0, ctk.END)
    self.kml_entry.insert(ctk.END, ruta_archivo_excel)
    
    return ruta_archivo_excel

def leer_y_transformar_coordenadas(self):
    ruta_archivo_excel = self.kml_entry.get()
    df = pd.read_excel(ruta_archivo_excel)
    
    if self.tipo_coords.get() == "decimales":    
        df['lat'] = df.iloc[:, 0]  # Columna A
        df['lon'] = df.iloc[:, 1]  # Columna B
    else:
        zona= self.zona_listbox.get()
        hemisferio = self.hemisferio_listbox.get()
        if hemisferio =='Northern':
            utm_crs = f"EPSG:326{int(zona):02d}"
        else:
            utm_crs = f"EPSG:327{int(zona):02d}"
        transformer = Transformer.from_crs(utm_crs, "EPSG:4326", always_xy=True)
        df['lon'], df['lat'] = transformer.transform(df.iloc[:, 1], df.iloc[:, 0])
    
    return df

def crear_kml(self):
    df = leer_y_transformar_coordenadas(self)
    
    if self.tipo_geo.get() == "Puntos":
        kml = simplekml.Kml()
        for index, row in df.iterrows():
            kml.newpoint(name=str(index), coords=[(row['lon'], row['lat'])])
    elif self.tipo_geo.get() == "Polilínea":
        kml = simplekml.Kml()
        coords = [(row['lon'], row['lat']) for index, row in df.iterrows()]
        kml.newlinestring(name="Polilínea", coords=coords)
   
    ruta_archivo_excel = self.kml = self.kml_entry.get()
    nombre_archivo_excel = os.path.basename(ruta_archivo_excel)
    nombre_archivo_kml = nombre_archivo_excel.replace('.xlsx', '.kml')
    
    # Obtener la ruta de la carpeta de descargas
    ruta_descargas = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    # Verificar si el archivo ya existe y agregar índice si es necesario
    indice = 0
    ruta_archivo_kml_full = os.path.join(ruta_descargas, nombre_archivo_kml)
    while os.path.exists(ruta_archivo_kml_full):
        indice += 1
        nombre_base, extension = os.path.splitext(nombre_archivo_kml)
        nombre_archivo_kml = f"{nombre_base} ({indice}){extension}"
        ruta_archivo_kml_full = os.path.join(ruta_descargas, nombre_archivo_kml)
    
    kml.save(ruta_archivo_kml_full)
    print(f"Creado y guardado con éxito en: {ruta_archivo_kml_full}")
    
    
    
if __name__ == "__main__":
    app = App()
    app.mainloop()