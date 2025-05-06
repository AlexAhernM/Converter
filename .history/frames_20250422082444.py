import customtkinter
from customtkinter import CTk

app = CTk()
app.after(0, lambda:app.state('zoomed'))

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=4)

# Frame 1
frame1 = customtkinter.CTkFrame(app, fg_color="dodger blue")
frame1.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Frame 2
frame2 = customtkinter.CTkFrame(app, fg_color="green")
frame2.grid(row=1, column=0, sticky="nsew")

# Frame 3
frame3 = customtkinter.CTkFrame(app, fg_color="blue")
frame3.grid(row=1, column=1, sticky="nsew")

frame1.grid_columnconfigure(0, weight=1)
frame1.grid_columnconfigure(1, weight=1)
frame1.grid_rowconfigure(0, weight=1)

entrada_archivo_kml = customtkinter.CTkEntry(frame1, width=50)
entrada_archivo_kml.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Crear el botón para seleccionar el archivo
boton_seleccionar_archivo_kml = customtkinter.CTkButton(frame1, text="Seleccionar archivo KLM", font=('Times New Roman',12))
boton_seleccionar_archivo_kml.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Crear checkbutton elevacion
obtener_elevacion = customtkinter.BooleanVar() # Crear variable de estado de checkbox
checkbox_obtener_elevacion = customtkinter.CTkCheckBox(frame1, text="Obtener elevación", variable=obtener_elevacion)
checkbox_obtener_elevacion.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

app.mainloop()
