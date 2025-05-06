import tkinter as tk

root = tk.Tk()
root.state("zoomed")

# Configurar las filas y columnas
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Frame 1
frame1 = tk.Frame(root, bg="red")
frame1.grid(row=1, column=1, rowspan=1, sticky="nsew")

# Frame 2
frame2 = tk.Frame(root, bg="green")
frame2.grid(row=1, column=0, sticky="nsew")

# Frame 3
frame3 = tk.Frame(root, bg="blue")
frame3.grid(row=1, column=1, sticky="nsew")

root.mainloop()