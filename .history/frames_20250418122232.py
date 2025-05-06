import tkinter as tk

ventana_principal = tk.Tk()
ventana_principal.state("zoomed")


frame1 = tk.Frame(ventana_principal, bg="red")
frame1.pack(fill='x', expand= True)

#frame_inferior = tk.Frame(ventana_principal)
#frame_inferior.pack(fill="both", expand=True)

frame2 = tk.Frame(ventana_principal, bg="blue")
frame2.pack(side="left", fill="x", expand=True)

frame3 = tk.Frame(ventana_principal, bg="green")
frame3.pack(side="right", fill="x", expand=True)

ventana_principal.mainloop()