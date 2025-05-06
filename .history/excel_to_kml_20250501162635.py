import pandas as pd
from pyproj import Transformer
import simplekml
import customtkinter as ctk
from customtkinter import filedialog
    

# Crear la GUI

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x900")
        self.title("coordinate converter")

        self.tipo_var = ctk.StringVar()
        self.tipo_var.set("Puntos")
        
        self.tipo_coords_var = ctk.StringVar()
        self.tipo_coords_var.set("decimales")

        self.tipo_frame = ctk.CTkFrame(self)
        self.tipo_frame.grid(row=0, column=2, padx=10, pady=10, sticky ='w')
        

        self.kml_label = ctk.CTkLabel(self.tipo_frame, text="Tipo de KML:")
        self.kml_label.grid(row=0, column=0, padx=10, pady=10, sticky ='w')


        self.kml_puntos= ctk.CTkRadioButton(self.tipo_frame, text="Puntos", variable=self.tipo_var, value="Puntos")
        self.kml_puntos.grid(row=0, column=2, padx=10, pady=10, sticky ='w')

        self.kml_poliln= ctk.CTkRadioButton(self.tipo_frame, text="Polilínea", variable=self.tipo_var, value="Polilínea")
        self.kml_poliln.grid(row=0, column=3, padx=10, pady=10, sticky ='w')

        self.zona_label = ctk.CTkLabel(self.tipo_frame, text="Zona:")
        self.zona_label.grid(row=0, column = 4,padx=10, pady=10, sticky ='w' )
        self.zona_listbox = ctk.CTkComboBox(self.tipo_frame, values=[str(i) for i in range(1, 61)])
        self.zona_listbox.set("Zona")
        self.zona_listbox.bind("<<ComboboxSelected>>", lambda event: self.hemisferio_listbox.configure(state="normal"))
        self.zona_listbox.configure(state="disabled")
        self.zona_listbox.grid(row=1, column = 4,padx=10, pady=10, sticky ='w') 

        self.hemisferio_label = ctk.CTkLabel(self.tipo_frame, text="Hemisferio:")
        self.hemisferio_label.grid(row=0, column = 5,padx=10, pady=10, sticky ='w' )
        self.hemisferio_listbox = ctk.CTkComboBox(self.tipo_frame, values=["Norte", "Sur"])
        self.hemisferio_listbox.set("Hemisferio")
        self.hemisferio_listbox.bind("<<ComboboxSelected>>", lambda event: self.zona_listbox.configure(state="normal"))
        self.hemisferio_listbox.configure(state="disabled")
        self.hemisferio_listbox.grid(row=1, column = 5,padx=10, pady=10, sticky ='w' )

        self.select_boton = ctk.CTkButton(self.tipo_frame, text='Select File', command= select_file)
        self.select_boton.grid(row=0, column=0, padx=10, pady=10, sticky ='w')

        self.kml_entry = ctk.CTkEntry(self)
        self.kml_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.kml_dec_radio  = ctk.CTkRadioButton(self, text="Coordenadas decimales", variable=self.tipo_coordenadas_var, value="decimales", command=seleccionar_tipo_coordenadas)
        self.kml_dec_radio.grid(row=1, column = 0, padx=10, pady=10, sticky='w')

        self.kml_utm_radio = ctk.CTkRadioButton(self, text="Coordenadas UTM", variable=self.tipo_coordenadas_var, value="utm", command=seleccionar_tipo_coordenadas)
        self.kml_utm_radio.grid(row=1, column = 1, padx=10, pady=10, sticky='w')
        

        self.crear_button = ctk.CTkButton(self, text="Crear archivo KML", command=crear_kml)
        self.crear_button.grid(row=2, column=0, padx=10, pady=10, sticky ='ew', columnspan = 2)
        
        
def select_file(self):
    ruta_archivo_excel = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivo XLSX", "*.xlsx")])
    self.kml_entry.delete(0, ctk.END)
    self.kml_entry.insert(ctk.END, ruta_archivo_excel)
    
    return ruta_archivo_excel

def seleccionar_tipo_coordenadas(self):
    
    df = pd.read_excel(self.kml_entry.get())
    
    if self.tipo_coordenadas_var.get() == "decimales":    
        df['lon'] = df.iloc[:, 0]  # Columna A
        df['lat'] = df.iloc[:, 1]  # Columna B
    else:
        zona= self.zona_listobox.get(self.zona_listbox.curselection())
        hemisferio = self.hemisferio_listbox.get(self.hemisferio_listbox.curselection())
        if hemisferio =='Northern':
            utm_crs = f"EPSG:326{int(zona):02d}"
        else:
            utm_crs = f"EPSG:327{int(zona):02d}"
        transformer = Transformer.from_crs("EPSG:4326", utm_crs, always_xy=True)
        df['lon'], df['lat'] = transformer.transform(df.iloc[:, 0], df.iloc[:, 1])
        
# Función para crear el archivo KML
def crear_kml(self):
    ruta_archivo_excel = self.kml_entry.get()
    print (ruta_archivo_excel)
    df = pd.read_excel(ruta_archivo_excel)
            
    if self.tipo_var.get() == "Puntos":
        kml = simplekml.Kml()
        for index, row in df.iterrows():
            kml.newpoint(name=str(index), coords=[(row['lon'], row['lat'])])
    elif self.tipo_var.get() == "Polilínea":
        kml = simplekml.Kml()
        coords = [(row['lon'], row['lat']) for index, row in df.iterrows()]
        kml.newlinestring(name="Polilínea", coords=coords)
    kml.save('coordenadas.kml')        
        
        

if __name__ == "__main__":
    app = App()
    app.mainloop()