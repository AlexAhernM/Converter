
import customtkinter

def button_callback():
    print("button pressed")

app = customtkinter.CTk()
app.title("my app")
app.geometry("800x150")
app.grid_columnconfigure(0, weight=1)

button1 = customtkinter.CTkButton(app, text="my button", command=button_callback, sticky= 'ew')
button1.grid(row=0, column=0, padx=20, pady=20)




app.mainloop()
