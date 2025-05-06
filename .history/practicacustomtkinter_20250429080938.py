
import customtkinter
from customtkinter import filedialog, BooleanVar
import tkinter as tk
from tkinter import messagebox
from tkintermapview import TkinterMapView
from transforma import parseo, encontrar_placemark, convierte, procesar_placemark, get_zoom_level
from genera import generate_files_intermediate

class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values, enabled = True ):
        super().__init__(master)
        self.values = values
        self.checkboxes = []
        

        for i, value in enumerate(self.values):
            inputdata = customtkinter.CTkCheckBox(self, text=value)
            inputdata.grid(row=i+1, column=0, padx=10, pady= 10, sticky="sw")
            inputdata.configure(border_width = 1, border_color = 'white')
            if not enabled:
                inputdata.configure(state="disabled")
            self.checkboxes.append(inputdata)
            
    
    def get(self):
        checked_checkboxes = []
        for inputdata in self.checkboxes:
            if inputdata.get() == 1:
                checked_checkboxes.append(inputdata.cget("text"))
        return checked_checkboxes
    
    def enable_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.configure(state="normal")
    
    def disable_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.deselect()
            checkbox.configure(state="disabled")
        

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Geo Convert Program by Ambylog")
        self.after(0, lambda:app.state('zoomed'))
        self.grid_rowconfigure(2, weight=1)
        
        self.grid_columnconfigure(0, weight=1) # La primera columna ocupará 1/3 partes del ancho
        self.grid_columnconfigure(1, weight=3) # La segunda columna ocupará 2/3 parte del ancho
        
        # FRAME : ROW 0 - SELECT FILE
        self.selectfile_frame = customtkinter.CTkFrame(self)
        self.selectfile_frame.grid(row=0, column = 0, padx=10, pady=10, sticky='nsw')
        
        self.selectdata_boton = customtkinter.CTkButton(self.selectfile_frame, text='Select File', command=lambda: select_file(self))
        self.selectdata_boton.grid(row=0, column=0, padx=10, pady=(10,10), sticky = 'e')
        
        self.selectdata_entry = customtkinter.CTkEntry(self.selectfile_frame, width=290, height=25, corner_radius=6 )
        self.selectdata_entry.grid(row =0, column =1, padx=10, pady=10 )
        
        self.checkbox_altitude = CheckboxFrame(self.selectfile_frame, values={'Get Altitude'})
        self.checkbox_altitude.grid(row =1, column = 1, padx=10, pady=5)
        self.checkbox_altitude.configure(fg_color ='transparent')
    
        self.boton_lookmap = customtkinter.CTkButton(self.selectfile_frame, text="Preview", 
                                                     command= lambda: button_preview(self), 
                                                     width=190, height=30)
        self.boton_lookmap.configure(state= tk.DISABLED)
        self.boton_lookmap.grid(row=2, column=1, padx=10, pady=10)
        
        # FRAME: ROW 0 - SAVE LABELS 
        self.frame_save_label = customtkinter.CTkFrame(self)
        self.frame_save_label.grid (row=0, column=1, padx=50, pady=10, sticky= 'nsw', columnspan= 1)
        
        # FRAME: ROW 0 - SELECT FORMAT (Chexboxes)
        self.checkbox_type = CheckboxFrame(self ,values=['DXF (CAD)', 'Shapefile', 'xlxs (Excel)'], enabled=False)
        self.checkbox_type.grid(row=0, column=2, padx=(550,10), pady =10, sticky='nsw')
    
        
        # FRAME: ROW 1 - APPROVAL
        self.approval_frame = customtkinter.CTkFrame(self)
        self.approval_frame.grid(row=1, column =0, padx=10,pady = 0, sticky= 'ew', columnspan=3)
        
        # FRAME: ROW 2 - MAP PREVIEW
        self.preview_frame = customtkinter.CTkFrame(self)
        self.preview_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=3, sticky='nsew')
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        self.destroy()       
        
def select_file(self):
    ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])
    self.selectdata_entry.delete(0, customtkinter.END)
    self.selectdata_entry.insert(customtkinter.END, ruta_archivo_kml)
    self.boton_lookmap.configure(state='normal')
    self.checkbox_type.disable_checkboxes()
    for widget in self.preview_frame.winfo_children():            
        widget.destroy()
    for widget in self.approval_frame.winfo_children():
        widget.destroy()
        
    return ruta_archivo_kml

def update_preview(self, lat_centro, lon_centro, zoom_start, root, altitud_value):
    for widget in self.preview_frame.winfo_children():            
        widget.destroy()
    
    self.mapa_tkinter = TkinterMapView(self.preview_frame)
    self.mapa_tkinter.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')   
    self.mapa_tkinter.set_position(lat_centro, lon_centro)
    self.mapa_tkinter.set_zoom(zoom_start)

    placemarks = encontrar_placemark(root)
    for placemark in placemarks:
        _, _, coords_dec, _, layer_name = procesar_placemark(placemark, altitud_value, [], [], [])
        if len(coords_dec) == 1:  # Point
            marker = self.mapa_tkinter.set_marker(coords_dec[0][0], coords_dec[0][1], text=layer_name,
                                                font=("Times New Roman", 8, "bold"), text_color="blue")
            self.mapa_tkinter.set_marker(coords_dec[0][0], coords_dec[0][1])
                
        else:    
            puntos = [(point[0], point[1]) for point in coords_dec]
            self.mapa_tkinter.set_path(puntos, color="red", width=1)
    
    self.label_mappreview = customtkinter.CTkLabel(self.approval_frame, text='Vision Preliminar Area Geografica a Procesar', 
                                                       fg_color='gray69', text_color='Blue' , width = 290, height=25, corner_radius=6)
    self.label_mappreview.grid(row=0, column =0, padx= (400), pady= (5))        
    self.mapa_tkinter.pack(fill="both", expand=True)
    

def button_preview(self):
    ruta_archivo_kml = self.selectdata_entry.get()
    print(ruta_archivo_kml)
    if ruta_archivo_kml: 
        self.preview_frame.configure(cursor="wait")  # Cambia el cursor a un reloj de arena
        self.preview_frame.update_idletasks()  # Fuerza a Tkinter a actualizar la GUI
        try:
            root, altitud_value = parseo(ruta_archivo_kml, self.checkbox_altitude.get())

            doc, coords, coords_dec, layers, lat_centro, lon_centro, radio = convierte(root, altitud_value)
            zoom_start = get_zoom_level(radio)
            update_preview(self, lat_centro, lon_centro, zoom_start, root, altitud_value)
            self.boton_lookmap.configure(state= 'disabled')
        finally:
            self.preview_frame.configure(cursor="arrow")  # Restaura el cursor original        
            confirmar_localizacion (self, doc, ruta_archivo_kml, coords, layers, coords_dec)
        
    else:
        messagebox.showerror("Error", "Por favor, seleccione un archivo KML")
            
    return doc, ruta_archivo_kml, coords, layers, coords_dec, altitud_value
        
def confirmar_localizacion(self, doc, ruta_archivo_kml, coords, layers, coords_dec):
    def respuesta_confirmacion(respuesta):
        if respuesta == "incorrecta":
            self.boton_lookmap.configure(state='disabled')
            # Vuelve a seleccionar otro archivo KML
            select_file(self)
        elif respuesta == "correcta":
            self.checkbox_type.enable_checkboxes()
            generate_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec) or ("", "", "")
                 
    boton_looks_good = customtkinter.CTkButton(self.approval_frame, text="Looks good", command=lambda: respuesta_confirmacion("correcta"),
                                                  fg_color='gray69', text_color='Blue' ,  corner_radius=6)
                                 
    boton_looks_good.grid(row =0, column=1, padx =10, pady =10, sticky ="e")
    
    boton_no_good = customtkinter.CTkButton(self.approval_frame, text="wrong location", command=lambda: respuesta_confirmacion("incorrecta"),
                              fg_color='gray69', text_color='Blue' ,  corner_radius=6)
    boton_no_good.grid (row=0, column=2, padx=10, pady=10, sticky='w')



  
def generate_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec):
    def on_click():
        messages = generate_files_intermediate(self, doc, ruta_archivo_kml, coords, layers, coords_dec)
        show_messages(self, messages)

    self.boton_generate_files = customtkinter.CTkButton(self.checkbox_type, text='generate files', state='normal',
                                                        command=on_click)
    self.boton_generate_files.grid(row=5, column=0, padx=10, pady=10, sticky='ew')
    
def show_messages(self, messages):
    msg_dxf, msg_shp, msg_xlx = messages
    if msg_dxf:
        self.save_dxf = customtkinter.CTkLabel(self.frame_save_label, text=msg_dxf)
        self.save_dxf.grid(row=0, column=0, padx=10, pady=10, sticky='we')

    if msg_shp:
        self.save_shp = customtkinter.CTkLabel(self.frame_save_label, text=msg_shp)
        if msg_dxf:
            self.save_shp.grid(row=1, column=0, padx=10, pady=10, sticky='we')
        else:
            self.save_shp.grid(row=0, column=0, padx=10, pady=10, sticky='we')

    if msg_xlx:
        self.save_xlx = customtkinter.CTkLabel(self.frame_save_label, text=msg_xlx)
        if msg_dxf and msg_shp:
            self.save_xlx.grid(row=2, column=0, padx=10, pady=10, sticky='we')
        elif msg_dxf or msg_shp:
            self.save_xlx.grid(row=1, column=0, padx=10, pady=10, sticky='we')
        else:
            self.save_xlx.grid(row=0, column=0, padx=10, pady=10, sticky='we')
    


   
    

    
app = App()
app.mainloop()