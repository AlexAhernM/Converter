
import customtkinter

def button_callback():
    print("button pressed")

app = customtkinter.CTk()
app.title("my app")
app.geometry("800x150")
app.grid_columnconfigure(2, weight=1)

button1 = customtkinter.CTkButton(app, text="my button", command=button_callback)
button1.grid(row=0, column=0, padx=5, pady=10, sticky= 'ew')

button2 = customtkinter.CTkButton(app, text="my button", command=button_callback)
button2.grid(row=0, column=1, padx=50, pady=50, sticky= 'ew')


app.mainloop()
