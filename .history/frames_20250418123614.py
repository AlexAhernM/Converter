import tkinter as tk

root = tk.Tk()
root.state("zoomed")

# Frame 1 (20% superior)
frame1 = tk.Frame(root, bg="red")
frame1.place(relx=0, rely=0, relwidth=1, relheight=0.2)

# Frame 2 (40% inferior izquierdo)
frame2 = tk.Frame(root, bg="green")
frame2.place(relx=0, rely=0.6, relwidth=0.5, relheight=1)

# Frame 3 (40% inferior derecho)
frame3 = tk.Frame(root, bg="blue")
frame3.place(relx=0.5, rely=0.6, relwidth=0.5, relheight=1)

root.mainloop()