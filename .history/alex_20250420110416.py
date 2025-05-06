
import customtkinter

def button_callback():
    print("button pressed")

app = customtkinter.CTk()
app.title("my app")
app.geometry("800x150")

button1 = customtkinter.CTkButton(app, text="my button", command=button_callback)
button1.grid(row=0, column=1, padx=20, pady=20)

button2 = customtkinter.CTkButton(app, text="my button", command=button_callback)
button2.grid(row=0, column=2, padx=20, pady=20)

app.mainloop()
