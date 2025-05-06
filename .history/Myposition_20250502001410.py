import tkinter as tk
from tkintermapview import TkinterMapView

def mostrar_mapa(root, lat, lng):
  map_widget = TkinterMapView(root, width=800, height=500)
  map_widget.pack(fill="both", expand=True)
  map_widget.set_position(lat, lng)
  map_widget.set_zoom(15)
  map_widget.set_marker(lat, lng, text="Mi posición actual")

def obtener_posicion():
  lat = float(lat_entry.get())
  lng = float(lng_entry.get())
  return lat, lng

root = tk.Tk()

lat_label = tk.Label(root, text="Latitud:")
lat_label.pack()
lat_entry = tk.Entry(root)
lat_entry.pack()

lng_label = tk.Label(root, text="Longitud:")
lng_label.pack()
lng_entry = tk.Entry(root)
lng_entry.pack()

def mostrar():
  lat, lng = obtener_posicion()
  mostrar_mapa(root, lat, lng)

mostrar_button = tk.Button(root, text="Mostrar", command=mostrar)
mostrar_button.pack()

root.mainloop()