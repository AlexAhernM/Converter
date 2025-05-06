import customtkinter

app = customtkinter.CTk()

app.title("my app")
app.geometry("400x280")
app.grid_columnconfigure(0, weight=1)

def button_callback(app):
        print("button pressed")

app.grid_rowconfigure((0, 1), weight=1)

checkbox_frame = customtkinter.CTkFrame(app, fg_color='gray69', corner_radius=16)
checkbox_frame.grid(row=0, column=0, padx=10, pady = 10, sticky = 'nsw')

app.checkbox_1 = customtkinter.CTkCheckBox(checkbox_frame, text="DXF (CAD)", text_color='white')
app.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

app.checkbox_2 = customtkinter.CTkCheckBox(app, text="Shapefile", text_color='RoyalBlue1')
app.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

app.checkbox_3 = customtkinter.CTkCheckBox(app, text="xlxs - Excel", text_color='green3')
app.checkbox_3.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        
app.button = customtkinter.CTkButton(app, text="my button", command= button_callback)
app.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

app.mainloop()