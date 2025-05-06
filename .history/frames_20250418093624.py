import tkinter as tk

root = tk.Tk()
root.geometry("800x600")  # Tamaño de la ventana

# Frame 1 (mitad izquierda)
frame1 = tk.Frame(root, bg="red")
frame1.place(x=0, y=0, width=400, height=600)  # Tamaño y posición

# Frame 2 (mitad superior de la mitad derecha)
frame2 = tk.Frame(root, bg="green")
frame2.place(x=400, y=0, width=400, height=300)  # Tamaño y posición

# Frame 3 (mitad inferior de la mitad derecha)
frame3 = tk.Frame(root, bg="blue")
frame3.place(x=400, y=300, width=400, height=300)  # Tamaño y posición

root.mainloop()