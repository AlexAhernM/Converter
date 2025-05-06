import customtkinter

app = customtkinter.CTk()

app.title("my app")
app.geometry("400x180")
app.grid_columnconfigure(0, weight=1)

def button_callback(app):
        print("button pressed")

app.grid_rowconfigure((0, 1), weight=1)

app.checkbox_1 = customtkinter.CTkCheckBox(app, text="checkbox 1")
app.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
app.checkbox_2 = customtkinter.CTkCheckBox(app, text="checkbox 2")
app.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
app.checkbox_3 = customtkinter.CTkCheckBox(app, text="checkbox 2")
app.checkbox_3.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        
app.button = customtkinter.CTkButton(app, text="my button", command= button_callback)
app.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

app.mainloop()