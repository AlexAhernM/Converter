
import customtkinter
from customtkinter import filedialog, BooleanVar
from tkinter import messagebox
from tkintermapview import TkinterMapView
from transforma import parseo, encontrar_placemark, convierte, procesar_placemark, get_zoom_level
from genera import crear_dxf

class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values ):
        super().__init__(master)
        self.values = values
        self.get_altitude = customtkinter.BooleanVar()
        self.checkboxes = []
        self.get_altitude = BooleanVar

        for i, value in enumerate(self.values):
            inputdata = customtkinter.CTkCheckBox(self, text=value)
            inputdata.grid(row=i+1, column=0, padx=20, pady=(10, 10), sticky="w")
            inputdata.configure(border_width = 1, border_color = 'white')
            self.checkboxes.append(inputdata)
    
    def get(self):
        checked_checkboxes = []
        for inputdata in self.checkboxes:
            if inputdata.get() == 1:
                checked_checkboxes.append(inputdata.cget("text"))
        return checked_checkboxes
        
        

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Geo Convert Program by Ambylog")
        self.after(0, lambda:app.state('zoomed'))
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=8)
        self.grid_columnconfigure(0, weight=0) # La primera columna ocupará 3 partes del ancho
        self.grid_columnconfigure(1, weight=3) # La segunda columna ocupará 1 parte del ancho

        self.selectfile_frame = customtkinter.CTkFrame(self)
        self.selectfile_frame.grid(row=0, column = 0, padx=10, pady=10, sticky='w')
        
        self.checkbox_frame = CheckboxFrame(self, values=['DXF (CAD)', 'Shapefile', 'xlxs (Excel)'])
        self.checkbox_frame.grid(row=0, column=1, padx=(700,10), pady =10, sticky='nsw')
        
        self.preview_frame = customtkinter.CTkFrame(self)
        self.preview_frame.grid(row = 1, column = 0, padx=10, pady=10, columnspan ='2', sticky = 'nsew')
        
        self.selectdata_boton = customtkinter.CTkButton(self.selectfile_frame, text='Select File', command=lambda: select_file(self))
        self.selectdata_boton.grid(row=0, column=0, padx=10, pady=10, sticky = 'e')
        
        self.selectdata_entry = customtkinter.CTkEntry(self.selectfile_frame, width=290, height=25, corner_radius=6 )
        self.selectdata_entry.grid(row =0, column =1, padx=10, pady=10 )
        
        
        self.checkbox_frame2 = CheckboxFrame(self.selectfile_frame, values={'Get Altitude'})
        self.checkbox_frame2.grid(row =1, column = 1, padx=10, pady=10)
        self.checkbox_frame2.configure(fg_color ='transparent')
        

        self.boton_lookmap = customtkinter.CTkButton(self.selectfile_frame, text="Preview", command= lambda: button_preview(self), width=190, height=30)
        self.boton_lookmap.grid(row=3, column=1, padx=10, pady=10)
        
def select_file(self):
    ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])
    self.selectdata_entry.delete(0, customtkinter.END)
    self.selectdata_entry.insert(customtkinter.END, ruta_archivo_kml)
    self.boton_lookmap.configure(state='normal')
    return ruta_archivo_kml

def update_preview(self, lat_centro, lon_centro, zoom_start, root, obtener_elevacion_valor):
    for widget in self.preview_frame.winfo_children():            
        widget.destroy()

    mapa_tkinter = TkinterMapView(self.preview_frame)
    mapa_tkinter.set_position(lat_centro, lon_centro)
    mapa_tkinter.set_zoom(zoom_start)

    placemarks = encontrar_placemark(root)
    for placemark in placemarks:
        _, _, coords_dec, _, layer_name = procesar_placemark(placemark, obtener_elevacion_valor, [], [], [])
        if len(coords_dec) == 1:  # Point
            marker = mapa_tkinter.set_marker(coords_dec[0][0], coords_dec[0][1], text=layer_name,
                                                font=("Times New Roman", 8, "bold"), text_color="blue")
            mapa_tkinter.set_marker(coords_dec[0][0], coords_dec[0][1])
                
        else:    
            puntos = [(point[0], point[1]) for point in coords_dec]
            mapa_tkinter.set_path(puntos, color="red", width=1)
            
    mapa_tkinter.pack(fill="both", expand=True)
      

def button_preview(self):
    ruta_archivo_kml = self.selectdata_entry.get()
    print (ruta_archivo_kml)
    if ruta_archivo_kml:
        print(self.checkbox_frame.get_altitude)    
        root, obtener_elevacion_valor = parseo(ruta_archivo_kml, self.checkbox_frame.get_altitude.get())
        encontrar_placemark(root)
        doc, coords, coords_dec, layers, lat_centro, lon_centro, radio = convierte(root, obtener_elevacion_valor)
        zoom_start = get_zoom_level(radio)
        update_preview(lat_centro, lon_centro, zoom_start, root, obtener_elevacion_valor)        
        #confirmar_localizacion (doc, ruta_archivo_kml, coords, layers, coords_dec)
        #boton_transformar_archivo.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Por favor, seleccione un archivo KML")
            
    return doc, ruta_archivo_kml, coords, layers, coords_dec, get_altitude
        


app = App()
app.mainloop()