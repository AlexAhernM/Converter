import tkinter as tk

root = tk.Tk()
root.state("zoomed")

# Frame 1 (20% superior)
frame1 = tk.Frame(root, bg="red")
frame1.place(relx=0, rely=0, relwidth=1, relheight=0.2)

# Frame 2 (40% inferior izquierdo)
frame2 = tk.Frame(root, bg="green")
frame2.place(relx=0, rely=0.2, relwidth=0.2, relheight=0.8)

# Frame 3 (40% inferior derecho)
frame3 = tk.Frame(root, bg="blue")
frame3.place(relx=0.8, rely=0.2, relwidth=0.8, relheight=0.8)

root.mainloop()
