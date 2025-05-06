import customtkinter

class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color='gray69', corner_radius=16)
        
        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="DXF (CAD)")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="w")
        
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="Shapefile")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="w")
        
        self.checkbox_3 = customtkinter.CTkCheckBox(self, text='xlxs - Excel', text_color='yellow')
        self.checkbox_3.grid(row=2, column=0, padx=10, pady=(20,0), sticky= 'w')
        
        self.checkbox_4 = customtkinter.CTkCheckBox(self, text='csv ', text_color='RoyalBlue1')
        self.checkbox_4.grid(row=3, column=0, padx=10, pady=(20,0), sticky= 'w')
        
    def get(self):
        checked_checkboxes = []
        if self.checkbox_1.get() == 1:
            checked_checkboxes.append(self.checkbox_1.cget("text"))
        if self.checkbox_2.get() == 1:
            checked_checkboxes.append(self.checkbox_2.cget("text"))
        if self.checkbox_3.get() == 1:
            checked_checkboxes.append(self.checkbox_3.cget("text"))
        if self.checkbox_4.get() == 1:
            checked_checkboxes.append(self.checkbox_4.cget("text"))
        return checked_checkboxes

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x270")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox_frame = MyCheckboxFrame(self)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="nsw")

        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback, fg_color='pink', corner_radius=6, text_color='black')
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        print("checked checkboxes:", self.checkbox_frame.get())
        
app = App()
app.mainloop()
