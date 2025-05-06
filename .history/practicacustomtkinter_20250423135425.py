
import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.after(0, lambda:app.state('zoomed'))
        self.grid_columnconfigure((1) , weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=9)

        self.inputdata_frame = customtkinter.CTkFrame(self)
        self.inputdata_frame.grid(row=0, column = 0, padx=10, pady=10, sticky='w')
        
        self.checkbox_frame = customtkinter.CTkFrame(self, width=850)
        self.checkbox_frame.grid(row=0, column=1, padx=10, pady=10, sticky ='e')
        
        self.preview_frame = customtkinter.CTkFrame(self)
        self.preview_frame.grid(row = 1, column = 0, padx=10, pady=10, columnspan ='3', sticky = 'nsew')
        
        self.inputdata = customtkinter.CTkEntry(self.inputdata_frame,placeholder_text="CTkEntry",
                               width=390,
                               height=25,
                               border_width=2,
                               corner_radius=6) 
        self.inputdata.grid(row =0, column=1, padx=10, pady=10)
        
        
        self.labelinput = customtkinter.CTkLabel(self.inputdata_frame, text='Seleccione archivo')
        self.labelinput.grid(row=0, column=0, padx=10, pady=10, sticky = 'e')
        
        self.checkbox_1 = customtkinter.CTkCheckBox(self.checkbox_frame, text="DXF (CAD)")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self.checkbox_frame, text="Shapefile")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10,0), sticky="w")
        self.checkbox_3 = customtkinter.CTkCheckBox(self.checkbox_frame, text="xlxs (Excel)")
        self.checkbox_3.grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")

        self.button = customtkinter.CTkButton(self.inputdata_frame, text="Visualizar", command=self.button_callback, width=190, height=30)
        self.button.grid(row=3, column=1, padx=10, pady=10)
        #self.button.columnconfigure(0, weight=1)

    def button_callback(self):
        print("button pressed")

app = App()
app.mainloop()