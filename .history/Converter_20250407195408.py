import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, ttk
import time
import os
from tkhtmlview import HTMLLabel
from transforma import Mapa
from transforma import parseo
import threading


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
        etiqueta_advertencia.config(text="Advertencia: Debe estar conectado a internet,  para proceso on-iine de obtención de elevación")
    else:
        etiqueta_advertencia.config(text="Proceso normal")      
        

# Crear la ventana principal

ventana_principal = tk.Tk()
ventana.destroy
ventana_principal.title("Transformar archivo KML a UTM")

# Crear las etiquetas y entradas para la ruta del archivo KML
etiqueta_archivo_kml = tk.Label(ventana_principal, text="Ruta del archivo KML:")
entrada_archivo_kml = tk.Entry(ventana_principal, width=50)
boton_seleccionar_archivo_kml = tk.Button(ventana_principal, text="Seleccionar archivo", command=seleccionar_archivo_kml)


# Crear variable de estado de checkbox
obtener_elevacion = tk.BooleanVar()

# Mostrar la imagen del mapa en la ventana


def actualizar_imagen_mapa():
    # Eliminar la imagen estática anterior
    for widget in frame_mapa.winfo_children():
        widget.destroy()

    # Crear el recuadro para mostrar el mapa
    html_mapa = HTMLLabel(frame_mapa, html='<iframe src="file:///D:/OneDrive/tuto_vscode/Conversion/mapa.html" width="100%" height="100%"></iframe>')
    html_mapa.pack(fill=tk.BOTH, expand=True)
       
    
    
frame_mapa = tk.Frame(ventana_principal)
frame_mapa.grid(row=5, column=0, columnspan=3)


# Crear el botón para transformar el archivo
boton_transformar_archivo = tk.Button(ventana_principal, text="Transformar archivo",
                                      command=lambda: [parseo(entrada_archivo_kml, obtener_elevacion), actualizar_imagen_mapa()])

# Colocar los elementos en la ventana principal
etiqueta_archivo_kml.grid(row=0, column=0, padx=5, pady=5)

entrada_archivo_kml.grid(row=0, column=1, padx=5, pady=5)
boton_seleccionar_archivo_kml.grid(row=0, column=2, padx=5, pady=5)
boton_transformar_archivo.grid(row=2, column=1, padx=5, pady=5)


# Crear checkbuttom elevacion
checkbox_obtener_elevacion = tk.Checkbutton(ventana_principal, text="Obtener elevación", variable=obtener_elevacion,command=mostrar_advertencia)
checkbox_obtener_elevacion.grid(row=4, column=1, padx=5, pady=5)

# Colocar etiqueta elevacion  en la ventana principal
etiqueta_advertencia = tk.Label(ventana_principal, wraplength=400)
etiqueta_advertencia.grid(row=4, column=2, columnspan=3, padx=5, pady=5)

ventana_principal.mainloop()


