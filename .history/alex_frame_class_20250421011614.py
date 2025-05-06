import customtkinter

class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(app, master):
        super().__init__(master, fg_color='gray69', corner_radius=16)
        
        app.checkbox_1 = customtkinter.CTkCheckBox(app, text="DXF (CAD)")
        app.checkbox_1.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="w")
        
        app.checkbox_2 = customtkinter.CTkCheckBox(app, text="Shapefile")
        app.checkbox_2.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="w")
        
        app.checkbox_3 = customtkinter.CTkCheckBox(app, text='xlxs - Excel', text_color='yellow')
        app.checkbox_3.grid(row=2, column=0, padx=10, pady=(20,0), sticky= 'w')
        
        app.checkbox_4 = customtkinter.CTkCheckBox(app, text='csv ', text_color='RoyalBlue1')
        app.checkbox_4.grid(row=3, column=0, padx=10, pady=(20,0), sticky= 'w')
        
    def get(app):
        checked_checkboxes = []
        if app.checkbox_1.get() == 1:
            checked_checkboxes.append(app.checkbox_1.cget("text"))
        if app.checkbox_2.get() == 1:
            checked_checkboxes.append(app.checkbox_2.cget("text"))
        if app.checkbox_3.get() == 1:
            checked_checkboxes.append(app.checkbox_3.cget("text"))
        if app.checkbox_4.get() == 1:
            checked_checkboxes.append(app.checkbox_4.cget("text"))
        return checked_checkboxes

class App(customtkinter.CTk):
    def __init__(app):
        super().__init__()

        app.title("my app")
        app.geometry("400x270")
        app.grid_columnconfigure(0, weight=1)
        app.grid_rowconfigure(0, weight=1)

        app.checkbox_frame = MyCheckboxFrame(app)
        app.checkbox_frame.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="nsw")

        app.button = customtkinter.CTkButton(app, text="my button", command=app.button_callback, fg_color='pink', corner_radius=6, text_color='black')
        app.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(app):
        print("checked checkboxes:", app.checkbox_frame.get())
            
        
app = App()
app.mainloop()