
import customtkinter
from customtkinter import filedialog

class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values ):
        super().__init__(master)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            inputdata = customtkinter.CTkCheckBox(self, text=value)
            inputdata.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
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
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=0) # La primera columna ocupará 3 partes del ancho
        self.grid_columnconfigure(1, weight=3) # La segunda columna ocupará 1 parte del ancho

        self.inputdata_frame = customtkinter.CTkFrame(self)
        self.inputdata_frame.grid(row=0, column = 0, padx=10, pady=10, sticky='w')
        
        self.checkbox_frame = CheckboxFrame(self, values=['DXF (CAD)', 'Shapefile', 'xlxs (Excel)'])
        self.checkbox_frame.grid(row=0, column=1, padx=10,pady =10, sticky='w')
        
        self.preview_frame = customtkinter.CTkFrame(self)
        self.preview_frame.grid(row = 1, column = 0, padx=10, pady=10, columnspan ='2', sticky = 'nsew')
        
        self.selectdata_boton = customtkinter.CTkButton(self.inputdata_frame, text='Seleccione archivo', command=self.select_file)
        self.selectdata_boton.grid(row=0, column=0, padx=10, pady=10, sticky = 'e')
        
        self.selectdata_entry = customtkinter.CTkEntry(self.inputdata_frame, width=290, height=25, corner_radius=6 )
        self.selectdata_entry.grid(row =0, column =1, padx=10, pady=10 )

        self.button = customtkinter.CTkButton(self.inputdata_frame, text="Visualizar", command=self.button_callback, width=190, height=30)
        self.button.grid(row=3, column=1, padx=10, pady=10)
        #self.button.columnconfigure(0, weight=1)

    def button_callback(self):
        print("Opciones Seleccionadas", self.checkbox_frame.get())
        
        
    def select_file(self):
        ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])
        self.selectdata_entry.delete(0, customtkinter.END)
        self.selectdata_entry.insert(customtkinter.END, ruta_archivo_kml)
        self.button.configure(state='normal')
        return ruta_archivo_kml

app = App()
app.mainloop()