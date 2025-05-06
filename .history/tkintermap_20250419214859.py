import tkinter as tk
import tkintermapview 

root_tk = tk.Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
# set current widget position by address
#map_widget.set_position(48.860381, 2.338594, text= 'Chupando el Pichulon', marker=True) 
#map_widget.set_marker 
map_widget.set_zoom(16)
# set current widget position by address
marker_1 = map_widget.set_address("colosseo, rome, italy", marker=True)

print(marker_1.position, marker_1.text)  # get position and text

marker_1.set_text("Colosseo in Rome")  # set new text
# marker_1.set_position(48.860381, 2.338594)  # change position
# marker_1.delete()
map_widget.set_zoom(16)
map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root_tk.mainloop()