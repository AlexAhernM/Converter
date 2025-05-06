import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import filedialog, ttk
import time
from tkintermapview import TkinterMapView
from transforma import parseo, encontrar_placemark, convierte, procesar_placemark, get_zoom_level
from genera import crear_dxf
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
    boton_transformar_archivo.config(state=tk.NORMAL)
    return ruta_archivo_kml
       
def mostrar_advertencia():
    
    if obtener_elevacion.get():
        etiqueta_advertencia.config(text="Advertencia: Debe estar conectado a internet,  para proceso on-iine de obtención de elevación")
    else:
        etiqueta_advertencia.config(text="Proceso normal")      
        

# Crear la ventana principal


ventana_principal = tk.Tk()
ventana.destroy
ventana_principal.state('zoomed')
ventana_principal.title("Transformar archivo KML a UTM")
# Crear las etiquetas y entradas para la ruta del archivo KML
etiqueta_archivo_kml = tk.Label(ventana_principal, text="Ruta del archivo KML:")
entrada_archivo_kml = tk.Entry(ventana_principal, width=50)
boton_seleccionar_archivo_kml = tk.Button(ventana_principal, text="Seleccionar archivo", command=seleccionar_archivo_kml)


# Crear variable de estado de checkbox
obtener_elevacion = tk.BooleanVar()

# Mostrar la imagen del mapa en la ventana

def actualizar_imagen_mapa(lat_centro, lon_centro, zoom_start, root, obtener_elevacion_valor,):
    for widget in frame_mapa.winfo_children():
        widget.destroy()

    mapa_tkinter = TkinterMapView(frame_mapa)
    mapa_tkinter.set_position(lat_centro, lon_centro)
    mapa_tkinter.set_zoom(zoom_start)

    placemarks = encontrar_placemark(root)
    for placemark in placemarks:
        _, _, coords_dec, _, layer_name = procesar_placemark(placemark, obtener_elevacion_valor, [], [], [])
        if len(coords_dec) == 1:  # Point
            mapa_tkinter.set_marker(coords_dec[0][0], coords_dec[0][1], text=layer_name)
        else:  # LineString o Polygon
            puntos = [(point[0], point[1]) for point in coords_dec]
            mapa_tkinter.set_path(puntos)

    #mapa_tkinter.grid(row=0, column=0, columnspan=3, sticky="nsew")
    mapa_tkinter.pack(fill="both", expand=True)

      
frame_mapa = tk.Frame(ventana_principal)
frame_mapa.grid(row=5, column=0, columnspan=3)
  
def confirmar_localizacion(doc, ruta_archivo_kml, coords, layers, coords_dec):
    def respuesta_confirmacion(respuesta):
        if respuesta == "incorrecta":
            boton_transformar_archivo.config(state=tk.DISABLED)
            # Vuelve a seleccionar otro archivo KML
            seleccionar_archivo_kml()
        elif respuesta == "correcta":
            # Genera la conversión
            generar_conversion(doc, ruta_archivo_kml, coords, layers, coords_dec)
    
    ventana_confirmacion = tk.Toplevel(ventana_principal)
    ventana_confirmacion.title("Confirmar Localización")
    
    etiqueta_confirmacion = tk.Label(ventana_confirmacion, text="¿La localización es correcta?")
    etiqueta_confirmacion.pack()
    
    boton_correcta = tk.Button(ventana_confirmacion, text="Looks good", command=lambda: respuesta_confirmacion("correcta"))
    boton_correcta.pack(side=tk.LEFT)
    
    boton_incorrecta = tk.Button(ventana_confirmacion, text="Localización incorrecta", command=lambda: respuesta_confirmacion("incorrecta"))
    boton_incorrecta.pack(side=tk.LEFT)


# funcion que ejecuta el programa
def procesar_archivo():
    ruta_archivo_kml = entrada_archivo_kml.get()
    print (ruta_archivo_kml)
    if ruta_archivo_kml:
          
        root, obtener_elevacion_valor = parseo(ruta_archivo_kml, obtener_elevacion)
        encontrar_placemark(root)
        doc, coords, coords_dec, layers, lat_centro, lon_centro, radio = convierte(root, obtener_elevacion_valor)
        zoom_start = get_zoom_level(radio)
        actualizar_imagen_mapa(lat_centro, lon_centro, zoom_start, root, obtener_elevacion_valor)        
        confirmar_localizacion (doc, ruta_archivo_kml, coords, layers, coords_dec)
        boton_transformar_archivo.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Por favor, seleccione un archivo KML")
    return doc, ruta_archivo_kml, coords, layers, coords_dec

def generar_conversion(doc, ruta_archivo_kml, coords, layers, coords_dec):
    ruta_archivo_kml = entrada_archivo_kml.get()
    # Crea los checkbox para seleccionar los formatos de salida
    ventana_formatos = tk.Toplevel(ventana_principal)
    ventana_formatos.title("Seleccionar formatos de salida")
    
    formato_dxf = tk.BooleanVar()
    formato_shp = tk.BooleanVar()
    formato_xlsx = tk.BooleanVar()
    formato_csv = tk.BooleanVar()
    
    checkbox_dxf = tk.Checkbutton(ventana_formatos, text="DXF (CAD)", variable=formato_dxf)
    checkbox_dxf.pack()
    
    checkbox_shp = tk.Checkbutton(ventana_formatos, text="SHP (Shapefile)", variable=formato_shp)
    checkbox_shp.pack()
    
    checkbox_xlsx = tk.Checkbutton(ventana_formatos, text="XLXS (Excel)", variable=formato_xlsx)
    checkbox_xlsx.pack()
    
    checkbox_csv = tk.Checkbutton(ventana_formatos, text="CSV", variable=formato_csv)
    checkbox_csv.pack()
    
    def generar_archivos(doc, ruta_archivo_kml, coords, layers, coords_dec):
        # Genera los archivos según los formatos seleccionados
        if formato_dxf.get():
            crear_dxf(doc, ruta_archivo_kml, coords, layers, coords_dec)
        # Agrega el código para generar los demás formatos
    
    boton_generar = tk.Button(ventana_formatos, text="Generar archivos", 
                          command=lambda: generar_archivos(doc, ruta_archivo_kml, coords, layers, coords_dec))
    boton_generar.pack()

    
    
        
# Crear el botón para transformar el archivo
boton_transformar_archivo = tk.Button(ventana_principal, text="Transformar archivo", command=procesar_archivo, state=tk.DISABLED)
    
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


