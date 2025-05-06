import customtkinter


class MyCheckboxFrame(customtkinter.CTkFrame):
    
    def __init__(self, master, titulo,  values, font=('Times New Roman', 14)):
        super().__init__(master, fg_color='gray69', corner_radius=16)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.titulo = titulo
        self.checkboxes = []

        self.titulo = customtkinter.CTkLabel(self, text=self.titulo, fg_color="gray29", text_color='white', corner_radius=6)
        self.titulo.grid(row=0, column=0, padx=10, pady=(10,0),  sticky="ew")
        
        self.button  = customtkinter.CTkButton(self)
        self.button.grid(row=5, column=0, padx=10, pady=10, sticky ='ew')
        
        for i, valores in enumerate(self.values):
            if 'font' not in valores:
                valores['font'] = font
            checkbox = customtkinter.CTkCheckBox(self, **valores)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(15, 0), sticky="ew")
            self.checkboxes.append(checkbox)
        
       

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.after(0, lambda:app.state('zoomed'))
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        

        self.checkbox_frame1 = MyCheckboxFrame(self, 'Formatos', values=[{'text':'DXF (CAD)'   , 'text_color':'white'},
                                                            {'text':'Shapefile'   , 'text_color':'black' },
                                                            {"text":"xlxs (Excel)", 'text_color': 'Yellow'}, 
                                                            {'text':'csav -txt'   , 'text_color':'RoyalBlue1'}
                                                            ])
        
        
        self.checkbox_frame2 = MyCheckboxFrame(self, 'Opciones', values=[{'text':'KML to..', 'text_color':'gray29'},
                                                             {'text':'Lat/Lon to KML','text_color':'RoyalBlue2'}])
        
        self.checkbox_frame2.configure(fg_color='transparent')
        
        self.checkbox_frame1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.checkbox_frame2.grid(row=2, column=0, padx=10, pady=(10, 0), sticky= 'nsew')
        self.button_frame1 = MyCheckboxFrame(self, text="my button", command=self.button_callback, fg_color='pink', corner_radius=6, text_color='black')
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        print("checkbox_frame1:", self.checkbox_frame1.get())
        print("checkbox_frame2:", self.checkbox_frame2.get())
        
app = App()
app.mainloop()
