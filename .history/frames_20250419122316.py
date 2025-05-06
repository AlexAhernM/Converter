import tkinter as tk

root = tk.Tk()
root.state("zoomed")

# Frame 1
frame1 = tk.Frame(root, bg="dodger blue")
frame1.place(relx=0, rely=0, relwidth=1, relheight=0.25)

# Frame 2
frame2 = tk.Frame(root, bg="green")
frame2.place(relx=0, rely=0.25, relwidth=0.5, relheight=0.75)

# Frame 3
frame3 = tk.Frame(root, bg="blue")
frame3.place(relx=0.5, rely=0.25, relwidth=0.5, relheight=0.75)


etiqueta_archivo_kml = tk.Label(frame1, text="Ruta del archivo KML:", font=("Arial", 12), bg="dodger blue", fg="white")
etiqueta_archivo_kml.place(relx=0.01, rely=0.15, relwidth=0.13, relheight=0.1)

entrada_archivo_kml = tk.Entry(frame1, width=50)
entrada_archivo_kml.place(relx=0.13, rely=0.14, relwidth=0.25, relheight=0.12)

# Crear el botón para seleccionar el archivo
boton_seleccionar_archivo_kml = tk.Button(frame1, text="Seleccionar archivo")
boton_seleccionar_archivo_kml.place(relx=0.4, rely=0.15, relwidth=0.13, relheight=0.1)

# Crear checkbutton elevacion
obtener_elevacion = tk.BooleanVar() # Crear variable de estado de checkbox
checkbox_obtener_elevacion = tk.Checkbutton(frame1, text="Obtener elevación")
checkbox_obtener_elevacion.place(relx=0.20, rely=0.35, relwidth=0.12, relheight=0.1)



root.mainloop()