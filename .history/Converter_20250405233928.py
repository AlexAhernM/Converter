import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, ttk
import time
from transforma import parseo
import threading

#from folium.plugins import KML
#from folium import KMLOverlay
from PIL import Image, ImageTk

def carga_programa():
    for i in range(100):
        # En lugar de actualizar la GUI directamente, utilizamos el método after
        ventana.after(0, actualizar_progreso, i)
        time.sleep(0.1)
    ventana.after(0, cerrar_ventana)
    
def cerrar_ventana():
    ventana.destroy()
          
def actualizar_progreso(i):
    barra_progreso['value'] = i
    etiqueta_progreso['text'] = f"Loading... {i}%"

       
ventana = tk.Tk()
ventana.title ("Gis Converter Program ...Progress")

barra_progreso = ttk.Progressbar(ventana, orient="horizontal", length=600, mode="determinate")
barra_progreso.pack(pady=20)
etiqueta_progreso = tk.Label(ventana, text="Loading....", font=("Arial", 12))
etiqueta_progreso.pack(pady=20)

hilo_carga = threading.Thread(target=carga_programa)
hilo_carga.start()
ventana.mainloop()

def seleccionar_archivo_kml():
    ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])
    entrada_archivo_kml.delete(0, tk.END)
    entrada_archivo_kml.insert(tk.END, ruta_archivo_kml) 
    return ruta_archivo_kml
       
def mostrar_advertencia():
    print("La función mostrar_advertencia se ha llamado")
    print("Valor de obtener_elevacion:", obtener_elevacion.get())
    
    if obtener_elevacion.get():
        etiqueta_advertencia.config(text="Advertencia: El proceso de transformación puede ser más demorado debido a la obtención de elevación.")
    else:
        etiqueta_advertencia.config(text="ahora chupa este cogotito")      
        
def mostrar_mensaje():
    print("Valor de me voy de paseO:", voy_a_la_luna.get())
    if voy_a_la_luna.get():
        etiqueta_mensaje.config(text="Voy a la luna")
    else:
        etiqueta_mensaje.config(text="Te quedas en casa")

# Crear la ventana principal

ventana_principal = tk.Tk()
ventana.destroy
ventana_principal.title("Transformar archivo KML a UTM")

# Crear las etiquetas y entradas para la ruta del archivo KML
etiqueta_archivo_kml = tk.Label(ventana_principal, text="Ruta del archivo KML:")
entrada_archivo_kml = tk.Entry(ventana_principal, width=50)
boton_seleccionar_archivo_kml = tk.Button(ventana_principal, text="Seleccionar archivo", command=seleccionar_archivo_kml)


# Crear el botón para transformar el archivo
boton_transformar_archivo = tk.Button(ventana_principal, text="Transformar archivo",
                                      command=lambda: parseo(entrada_archivo_kml, obtener_elevacion))

# Colocar los elementos en la ventana principal
etiqueta_archivo_kml.grid(row=0, column=0, padx=5, pady=5)

entrada_archivo_kml.grid(row=0, column=1, padx=5, pady=5)
boton_seleccionar_archivo_kml.grid(row=0, column=2, padx=5, pady=5)
boton_transformar_archivo.grid(row=2, column=1, padx=5, pady=5)

# Crear variable de estado de checkbox
obtener_elevacion = tk.BooleanVar()
voy_a_la_luna = tk.BooleanVar()

# Crear checkbuttom elevacion
checkbox_obtener_elevacion = tk.Checkbutton(ventana_principal, text="Obtener elevación", variable=obtener_elevacion,command=mostrar_advertencia)
checkbox_obtener_elevacion.grid(row=4, column=1, padx=5, pady=5)

# Colocar etiqueta elevacion  en la ventana principal
etiqueta_advertencia = tk.Label(ventana_principal, text="sin elevacion", wraplength=400)
etiqueta_advertencia.grid(row=4, column=2, columnspan=3, padx=5, pady=5)


# Crear checkbuttom paseo
checkbutton_voy_a_la_luna = tk.Checkbutton(ventana_principal, text="Voy a la luna", variable=voy_a_la_luna, command=mostrar_mensaje)
checkbutton_voy_a_la_luna.grid (row=1, column=1, padx=10, pady=10)


#colovar etiqueta paseo en la ventana principal
etiqueta_mensaje = tk.Label(ventana_principal, text="Te quedas en casa")
etiqueta_mensaje.grid (row=1, column=2, padx=5, pady=5)





# Mostrar la imagen del mapa en la ventana
imagen_mapa = Image.open("mapa.png")
imagen_mapa_tk = ImageTk.PhotoImage(imagen_mapa)
label_imagen_mapa = tk.Label(ventana_principal, image=imagen_mapa_tk)
label_imagen_mapa.image = imagen_mapa_tk
label_imagen_mapa.grid(row=5, column=0, columnspan=3)


ventana_principal.mainloop()


