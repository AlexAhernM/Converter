import tkinter as tk
import tkintermapview 

root_tk = tk.Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
# set current widget position by address
map_widget.set_position(48.860381, 2.338594, marker=False)  # change position
map_widget.set_tile_server("Chupando la callampa")
map_widget.set_zoom(16)
map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root_tk.mainloop()