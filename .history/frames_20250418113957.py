import tkinter as tk

root = tk.Tk()
root.state("zoomed")

# Frame 1
frame1 = tk.Frame(root, bg="red")
frame1.pack(side=tk.LEFT, fill=tk.Y, expand=True)

# Frame 2
frame2 = tk.Frame(root, bg="green")
frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Frame 3
frame3 = tk.Frame(root, bg="blue")
frame3.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

root.mainloop()