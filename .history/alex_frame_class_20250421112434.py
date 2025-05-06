import customtkinter

class MyCheckboxFrame(customtkinter.CTkFrame):
    
    def __init__(self, master, values):
        super().__init__(master, fg_color='gray69', corner_radius=16)
        self.values = values
        self.checkboxes = []

        for i, valores in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, **valores)
            checkbox.grid(row=i, column=0, padx=10, pady=(22, 0), sticky="w")
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
        self.geometry("400x270")
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        

        self.checkbox_frame1 = MyCheckboxFrame(self, values=[{'text':'DXF (CAD)'   , 'text_color':'white'},
                                                            {'text':'Shapefile'   , 'text_color':'black'},
                                                            {"text":"xlxs (Excel)", 'text_color': 'Yellow'}, 
                                                            {'text':'csav -txt'   , 'text_color':'RoyalBlue1'}
                                                            ])
        self.checkbox_frame2 = MyCheckboxFrame(self, values=[{'text':'KML'}, {'text':'Excel'}])
        
        self.checkbox_frame1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")
        self.checkbox_frame2.grid(row=0, column=1, padx=10, pady=(10, 0), sticky= 'nsw')
        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback, fg_color='pink', corner_radius=6, text_color='black')
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        print("checkbox_frame1:", self.checkbox_frame1.get())
        print("checkbox_frame2:", self.checkbox_frame2.get())
        
app = App()
app.mainloop()
