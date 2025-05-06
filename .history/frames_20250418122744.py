import tkinter as tk

ventana_principal = tk.Tk()
ventana_principal.state("zoomed")

frame1 = tk.Frame(ventana_principal, bg="red")
frame1.grid(row=0, column=0, columnspan=2, sticky="ew")

frame2 = tk.Frame(ventana_principal, bg="blue")
frame2.grid(row=1, column=0, sticky="nsew")

frame3 = tk.Frame(ventana_principal, bg="green")
frame3.grid(row=1, column=1, sticky="nsew")

ventana_principal.grid_rowconfigure(0, weight=0)
ventana_principal.grid_rowconfigure(1, weight=1)
ventana_principal.grid_columnconfigure(0, weight=1)
ventana_principal.grid_columnconfigure(1, weight=1)


ventana_principal.mainloop()