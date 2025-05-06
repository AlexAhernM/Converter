
import customtkinter

class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values ):
        super().__init__(master)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            inputdata = customtkinter.CTkCheckBox(self, text=value)
            inputdata.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
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

        self.title("my app")
        self.after(0, lambda:app.state('zoomed'))
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=0) # La primera columna ocupará 3 partes del ancho
        self.grid_columnconfigure(1, weight=3) # La segunda columna ocupará 1 parte del ancho

        self.inputdata_frame = customtkinter.CTkFrame(self)
        self.inputdata_frame.grid(row=0, column = 0, padx=10, pady=10, sticky='w')
        
        self.checkbox_frame = customtkinter.CTkFrame(self)
        self.checkbox_frame.grid(row=0, column=1, padx=10,pady =10, sticky='w')
        
        self.preview_frame = customtkinter.CTkFrame(self)
        self.preview_frame.grid(row = 1, column = 0, padx=10, pady=10, columnspan ='2', sticky = 'nsew')
        
        self.inputdata = CheckboxFrame(self, values=['DXF (CAD)', 'Shapefile', 'xlxs (Excel)'])
        
        
        
        self.labelinput = customtkinter.CTkLabel(self.inputdata_frame, text='Seleccione archivo')
        self.labelinput.grid(row=0, column=0, padx=10, pady=10, sticky = 'e')

        self.button = customtkinter.CTkButton(self.inputdata_frame, text="Visualizar", command=self.button_callback, width=190, height=30)
        self.button.grid(row=3, column=1, padx=10, pady=10)
        #self.button.columnconfigure(0, weight=1)

    def button_callback(self):
        print("button pressed")

app = App()
app.mainloop()