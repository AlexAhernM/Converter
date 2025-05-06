import customtkinter

class MyCheckboxFrame(customtkinter.CTkFrame):
    
    def __init__(self, master, values):
        super().__init__(master, fg_color='gray69', corner_radius=16)
        self.values = values
        self.checkboxes = []

        for i, valores in enumerate(self.values):
            pichula = customtkinter.CTkCheckBox(self, **valores)
            pichula.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(pichula)

    def get(self):
        checked_checkboxes = []
        for pichula in self.checkboxes:
            if pichula.get() == 1:
                checked_checkboxes.append(pichula.cget("text"))
        return checked_checkboxes

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x270")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        

        self.checkbox_frame = MyCheckboxFrame(self, values=[{'text':'DXF (CAD)'   , 'text_color':'white'},
                                                            {'text':'Shapefile'   , 'text_color':'black'},
                                                            {"text":"xlxs (Excel)", 'text_color': 'Yellow'}, 
                                                            {'text':'csav -txt'   , 'text_color':'RoyalBlue1'}
                                                            ])
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback, fg_color='pink', corner_radius=6, text_color='black')
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        print("checked checkboxes:", self.checkbox_frame.get())
        
app = App()
app.mainloop()
