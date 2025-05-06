
import customtkinter
from customtkinter import CTk


app = CTk()
app.after(0, lambda:app.state('zoomed'))

# Frame 1
frame1 = customtkinter.CTkFrame(app, fg_color="dodger blue")
frame1.place(relx=0, rely=0, relwidth=1, relheight=0.25)

# Frame 2
frame2 = customtkinter.CTkFrame(app, fg_color="green")
frame2.place(relx=0, rely=0.25, relwidth=0.5, relheight=0.75)

# Frame 3
frame3 = customtkinter.CTkFrame(app, fg_color="blue")
frame3.place(relx=0.5, rely=0.25, relwidth=0.5, relheight=0.75)

entrada_archivo_kml = customtkinter.CTkEntry(frame1, width=50)
entrada_archivo_kml.place(relx=0.16, rely=0.15, relwidth=0.25, relheight=0.12)

# Crear el botón para seleccionar el archivo
boton_seleccionar_archivo_kml = customtkinter.CTkButton(frame1, text="Seleccionar archivo KLM", font=('Times New Roman',12))
boton_seleccionar_archivo_kml.place(relx=0.01, rely=0.15, relwidth=0.13, relheight=0.15)

# Crear checkbutton elevacion
obtener_elevacion = customtkinter.BooleanVar() # Crear variable de estado de checkbox
checkbox_obtener_elevacion = customtkinter.CTkButton(frame1, text="Obtener elevación")
checkbox_obtener_elevacion.place(relx=0.13, rely=0.50, relwidth=0.12, relheight=0.1)


app.mainloop()