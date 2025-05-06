import pandas as pd
from pyproj import Transformer
import simplekml
import customtkinter as ctk
from customtkinter import filedialog, CTkLis
import tkinter as tk
from tkinter import ttk


def select_file():
    ruta_archivo_excel = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivo XLSX", "*.xlsx")])
    kml_entry.delete(0, ctk.END)
    kml_entry.insert(ctk.END, ruta_archivo_excel)
    
    return ruta_archivo_excel

# Función para crear el archivo KML
def crear_kml():
    ruta_archivo_excel = kml_entry.get()
    print (ruta_archivo_excel)
    df = pd.read_excel(ruta_archivo_excel)

    if tipo_coordenadas_var.get() == "decimales":
        
        df['lon'] = df.iloc[:, 0]  # Columna A
        df['lat'] = df.iloc[:, 1]  # Columna B
    else:
        zona= zona_listobox.get(zona_listbox.curselection())
        hemisferio = hemisferio_listbox.get(hemisferio_listbox.curselection())
        if hemisferio =='Northern':
            utm_crs = f"EPSG:326{int(zona):02d}"
            
    if tipo_var.get() == "Puntos":
        kml = simplekml.Kml()
        for index, row in df.iterrows():
            kml.newpoint(name=str(index), coords=[(row['lon'], row['lat'])])
    elif tipo_var.get() == "Polilínea":
        kml = simplekml.Kml()
        coords = [(row['lon'], row['lat']) for index, row in df.iterrows()]
        kml.newlinestring(name="Polilínea", coords=coords)
    kml.save('coordenadas.kml')
    
    

# Crear la GUI

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        
        self.geometry("900x900")
        self.title("coordinate converter")


        self.tipo_coords_var = ctk.StringVar()
        self.tipo_coords_var.set("decimales")


        self.tipo_var = ctk.StringVar()
        self.tipo_var.set("Puntos")

        self.tipo_frame = ctk.CTkFrame(app)

        self.tipo_coordenadas_var = ctk.StringVar()
        self.tipo_coordenadas_var.set("decimales")


        self.kml_puntos= ctk.CTkRadioButton(self.tipo_frame, text="Puntos", variable=tipo_var, value="Puntos")
        self.kml_puntos.grid(row=0, column=2, padx=10, pady=10, sticky ='w')

        self.kml_poliln= ctk.CTkRadioButton(self.tipo_frame, text="Polilínea", variable=tipo_var, value="Polilínea")
        self.kml_poliln.grid(row=0, column=3, padx=10, pady=10, sticky ='w')

        self.zona_label = ctk.CTkLabel(app, text="Zona:")
        self.zona_label.grid(row=0, column = 4,padx=10, pady=10, sticky ='w' )
        self.zona_listbox = ctk.CTkComboBox(app)
        self.zona_listbox.insert(ctk.END, *range(1, 61))
        self.zona_listbox.configure(state="disabled")
        self.zona_listbox.pack(row=1, column = 4,padx=10, pady=10, sticky ='w') 

        hemisferio_label = ctk.CTkLabel(app, text="Hemisferio:")
        hemisferio_label.grid(row=0, column = 5,padx=10, pady=10, sticky ='w' )
        hemisferio_listbox = ctk.CTkListox(app)
        hemisferio_listbox.insert(tk.END, "Norte", "Sur")
        hemisferio_listbox.configure(state="disabled")
        hemisferio_listbox.pack()



        select_boton = ctk.CTkButton(app, text='Select File', command= select_file)
        select_boton.grid(row=0, column=0, padx=10, pady=10, sticky ='w')

        kml_entry = ctk.CTkEntry(app)
        kml_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        kml_dec_radio  = ctk.CTkRadioButton(app, text="Coordenadas decimales", variable=tipo_coordenadas_var, value="decimales", command=seleccionar_tipo_coordenadas)
        kml_dec_radio.grid(row=1, column = 0, padx=10, pady=10, sticky='w')

        kml_utm_radio = ctk.CTkRadioButton(app, text="Coordenadas UTM", variable=tipo_coordenadas_var, value="utm", command=seleccionar_tipo_coordenadas)
        kml_utm_radio.grid(row=1, column = 1, padx=10, pady=10, sticky='w')



        crear_button = ctk.CTkButton(app, text="Crear archivo KML", command=crear_kml)
        crear_button.grid(row=2, column=0, padx=10, pady=10, sticky ='ew', columnspan = 2)

if __name__ == "__main__":
    app = App()
    app.mainloop()