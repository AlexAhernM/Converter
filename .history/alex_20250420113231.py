
import customtkinter

def button_callback():
    print("pasa la lengua por esta alfombrita")
    
    
def button_callback1():
    print("chupa este cogotito")

app = customtkinter.CTk()
app.title("my app")
app.geometry("800x150")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)

button1 = customtkinter.CTkButton(app, text="my button", command=button_callback)
button1.grid(row=0, column=0, padx=20, pady=20, sticky= 'ew')




app.mainloop()
