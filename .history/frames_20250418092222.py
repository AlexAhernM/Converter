import tkinter as tk

root = tk.Tk()

# Crear 3 frames
frame1 = tk.Frame(root, bg="red")
frame2 = tk.Frame(root, bg="green")
frame3 = tk.Frame(root, bg="blue")

# Agregar widgets a cada frame
label1 = tk.Label(frame1, text="Frame 1")
label1.pack()

label2 = tk.Label(frame2, text="Frame 2")
label2.pack()

label3 = tk.Label(frame3, text="Frame 3")
label3.pack()

# Agregar los frames a la ventana
frame1.pack(side=tk.TOP)
frame2.pack(side=tk.TOP)
frame3.pack(side=tk.TOP)

root.mainloop()