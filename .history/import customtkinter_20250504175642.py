import customtkinter

def button_callback():
    print("button pressed")

app = customtkinter.CTk()
app.title("my app")
app.geometry("400x150")
app.grid_columnconfigure(0, weight=1)


button = customtkinter.CTkButton(app, text="my button", command=button_callback, sticky= "w")
button.grid(row=00, column=0, padx=(10),  pady=(10))

app.mainloop()