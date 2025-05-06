import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import filedialog, ttk
import time
import tkintermapview 

root_tk = tk.Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root_tk.mainloop()