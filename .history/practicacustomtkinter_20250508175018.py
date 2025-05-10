
import customtkinter
from customtkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from tkintermapview import TkinterMapView
from transforma import parseo, encontrar_placemark, convierte, procesar_placemark, get_zoom_level
from genera import generate_files_intermediate
import os
import re
import requests
from PIL import Image, ImageTk
from io import BytesIO



class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values, enabled=True, width=650, height = 180):
        super().__init__(master, width=width, height= height)
        #self.grid_propagate(False)
        self.values = values
        self.checkboxes = []
        

        for i, value in enumerate(self.values):
            inputdata = customtkinter.CTkCheckBox(self, text=value)
            inputdata.grid(row=i, column=0, padx=10, pady= (10, 5), sticky="nw")
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
    imagen_tk = None
    def __init__(self):
        super().__init__()
        self.title("Geo Convert Program by Ambylog")
        self.after(0, lambda:app.state('zoomed'))
        self.grid_columnconfigure(0, weight=1)
        
        
        
        # ROW 0 - SELECT FRAME
        self.selectfile_frame = customtkinter.CTkFrame(self, width=650, height=180, corner_radius=6)
        self.selectfile_frame.grid(row=0, column = 0, padx=10, pady=10, sticky='w')
        self.selectfile_frame.grid_propagate(False)
        
        self.selectdata_boton = customtkinter.CTkButton(self.selectfile_frame, text='Select File', command=lambda: select_file(self))
        self.selectdata_boton.grid(row=0, column=0, padx=10, pady=(25,10), sticky = 'w')
        
        self.selectdata_entry = customtkinter.CTkEntry(self.selectfile_frame, width=290, height=25, corner_radius=6 )
        self.selectdata_entry.grid(row =0, column =1, padx=10, pady=(20,10 ), sticky ='w')
        
        self.checkbox_altitude = CheckboxFrame(self.selectfile_frame, values={'Get Altitude'})
        self.checkbox_altitude.grid(row =1, column = 2, padx=10, pady=1)
        self.checkbox_altitude.configure(fg_color ='transparent')
    
        self.boton_lookmap = customtkinter.CTkButton(self.selectfile_frame, text="Preview", 
                                                     command= lambda: button_preview(self), 
                                                     width=160, height=20)
        self.boton_lookmap.configure(state= tk.DISABLED)
        self.boton_lookmap.grid(row=2, column=1, padx=10, pady=(10,0))
        
        
        # FRAME: ROW 0 - SELECT AND RESULT FORMAT (Chexboxes, Bottons and Labels)
        self.checkbox_type = CheckboxFrame(self ,values=['DXF (CAD)', 'Shapefile', 'xlxs (Excel)'], enabled=False)
        self.checkbox_type.grid(row=0, column=2, padx= 10, pady =5, sticky='we')
        
        self.boton_generate_files = customtkinter.CTkButton(self.checkbox_type, text='generate files')
        self.boton_generate_files.grid(row=4, column=0, padx=10, pady=10, sticky='ew')
        self.boton_generate_files.configure(state= 'disabled')
        
        
        # FRAME: ROW 1 - APPROVAL
        self.approval_frame = customtkinter.CTkFrame(self, height=40)
        self.approval_frame.grid(row=1 ,column =0, padx=10,pady =5,sticky='we', columnspan=3)
        #self.approval_frame.grid_propagate(False)
        
        # FRAME: ROW 2 - MAP PREVIEW
        # Creación del frame de vista previa
        self.preview_frame = customtkinter.CTkFrame(self, height=500, width=500)
        self.preview_frame.grid(row=2, column=0, padx=10, pady=5, columnspan=3, sticky='nsew')
        
        
        # Inicializar atributos del label y la imagen
        self.preview_label = None
        self.preview_image = None
        
         # Cargar y mostrar la imagen en el frame de vista previa
        show_image_in_preview(self)

        #self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
def show_image_in_preview(self):
        
    url_image = "https://raw.githubusercontent.com/AlexAhernM/Converter/master/earth.png"
        
    # Descargar la imagen desde la URL
    response = requests.get(url_image)
    if response.status_code == 200:
        # Cargar la imagen en PIL
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
    else:
        print(f"Error al descargar la imagen: {response.status_code}")
        return
        
    # Convertir la imagen para CTkLabel
    self.preview_image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(1600, 700))  # Ajusta el tamaño aquí
    
    # Crear y mostrar el CTkLabel (si no existe)
    if not self.preview_label:
        self.preview_label = customtkinter.CTkLabel(self.preview_frame, text="", image=self.preview_image)
        self.preview_label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    
def destroy_preview_label(self):
    # Método para destruir el CTkLabel y liberar recursos
    if self.preview_label:
        self.preview_label.destroy()
        self.preview_label = None
        self.preview_image = None  # Liberar la referencia de la imagen

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
        
    try:
        self.save_dxf.destroy()
    except AttributeError:
        pass
       
    try:
        self.save_shp.destroy()
    except AttributeError:
        pass   
       
    try:
        self.save_xlx.destroy()
    except AttributeError:
        pass      
          
       
    return ruta_archivo_kml

def update_preview(self, lat_centro, lon_centro, zoom_start, root, altitud_value):
    for widget in self.preview_frame.winfo_children():            
        widget.destroy()
    
    self.destroy_preview_label()  # Destruir el CTkLabel de la imagen
    
    
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
        
        root, altitud_value = parseo(ruta_archivo_kml, self.checkbox_altitude.get())
        doc, coords, coords_dec, layers, lat_centro, lon_centro, radio = convierte(root, altitud_value)
        zoom_start = get_zoom_level(radio)
        update_preview(self, lat_centro, lon_centro, zoom_start, root, altitud_value)
        self.boton_lookmap.configure(state= 'disabled')
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
                 
    self.boton_looks_good = customtkinter.CTkButton(self.approval_frame, text="Looks good", command=lambda: respuesta_confirmacion("correcta"),
                                                  fg_color='gray69', text_color='Blue' ,  corner_radius=6)
                                 
    self.boton_looks_good.grid(row =0, column=1, padx =10, pady =10, sticky ="e")
    
    
    self.boton_no_good = customtkinter.CTkButton(self.approval_frame, text="select another file", command=lambda: respuesta_confirmacion("incorrecta"),
                              fg_color='gray69', text_color='Blue' ,  corner_radius=6)
    self.boton_no_good.grid (row=0, column=2, padx=10, pady=10, sticky='w')
    
  
def generate_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec):
    def on_click():
        messages = generate_files_intermediate(self, doc, ruta_archivo_kml, coords, layers, coords_dec)
        show_messages(self, messages)
        
    self.boton_generate_files.configure(state= 'normal', command=on_click)
                                                            

def show_messages(self, messages):
    msg_dxf, msg_shp, msg_xlx = messages
    
    ruta_dxf_match = re.search(r'C:\\.*\.dxf', msg_dxf)
    if ruta_dxf_match:
        ruta_dxf = ruta_dxf_match.group()
    else:
        ruta_dxf = None

    ruta_shp_match = re.search(r'C:\\.*\.shp', msg_shp)
    if ruta_shp_match:
        ruta_shp = ruta_shp_match.group()
    else:
        ruta_shp = None
    
    ruta_xlx_match = re.search(r'C:\\.*\.xlsx', msg_xlx)
    print('se paso super bien  ', msg_xlx)
    if ruta_xlx_match:
        ruta_xlx = ruta_xlx_match.group()
        print('hasta aca super bien  ',  msg_xlx)
    else:
        ruta_xlx = None
    
    if msg_dxf:
        self.save_dxf = customtkinter.CTkButton(self.checkbox_type, text=msg_dxf, text_color='firebrick1', fg_color="transparent", hover_color=self.checkbox_type.cget("fg_color"), border_width=0)
        
        if ruta_dxf:
            self.save_dxf.configure(command=lambda ruta=ruta_dxf: abrir_archivo(ruta))
            self.save_dxf.grid(row=0, column=1, padx=5, pady=(10,5), sticky='w')

    if msg_shp:
        self.save_shp = customtkinter.CTkButton(self.checkbox_type, text=msg_shp, text_color='blue', fg_color="transparent", hover_color=self.checkbox_type.cget("fg_color"), border_width=0)
        
        if ruta_shp:
            self.save_shp.configure(command=lambda ruta=ruta_shp: abrir_archivo(ruta))
            self.save_shp.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    if msg_xlx:
        self.save_xlx = customtkinter.CTkButton(self.checkbox_type, text=msg_xlx, text_color='PaleGreen4', fg_color="transparent", hover_color=self.checkbox_type.cget("fg_color"), border_width=0)
        
        if ruta_xlx:
            self.save_xlx.configure(command=lambda ruta=ruta_xlx: abrir_archivo(ruta))
            self.save_xlx.grid(row=2, column=1, padx=5, pady=5, sticky='w')

def abrir_archivo(ruta):
    try:
        os.startfile(ruta)
    except OSError as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo {ruta}. Asegúrate de que haya una aplicación asociada con este tipo de archivo.")
        
    


   
    

    
app = App()
app.mainloop()