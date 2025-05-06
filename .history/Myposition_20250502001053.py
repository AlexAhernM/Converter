import tkinter as tk
from tkintermapview import TkinterMapView
import geocoder

def obtener_posicion():
  g = geocoder.ip('me')
  lat, lng = g.latlng
  return lat, lng

def mostrar_mapa(root):
  map_widget = TkinterMapView(root, width=800, height=500)
  map_widget.pack(fill="both", expand=True)
  lat, lng = obtener_posicion()
  map_widget.set_position(lat, lng)
  map_widget.set_zoom(15)
  map_widget.set_marker(lat, lng, text="Mi posición actual")

root = tk.Tk()
mostrar_mapa(root)
root.mainloop()