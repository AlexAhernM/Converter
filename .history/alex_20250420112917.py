
import customtkinter

def button_callback():
    print("pasa la lengua por esta alfombrita")
    
    
def button_callback1():
    print("chupa este cogotito")

app = customtkinter.CTk()
app.title("my app")
app.geometry("800x150")
app.grid_columnconfigure(1, weight=1)
pp.grid_rowconfigure(1, weight=1)
button1 = customtkinter.CTkButton(app, text="my button", command=button_callback)
button1.grid(row=0, column=0, padx=20, pady=20, sticky= 'ew')

button2 = customtkinter.CTkButton(app, text="my button", command=button_callback1)
button2.grid(row=0, column=1, padx=20, pady=20, sticky= 'ns')


app.mainloop()
