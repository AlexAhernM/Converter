import tkinter as tk


root = tk.Tk()
root.state("zoomed")

# Frame 1
frame1 = tk.Frame(root, bg="red")
frame1.place(relx=0, rely=0, relwidth=0.5, relheight=1)

# Frame 2
frame2 = tk.Frame(root, bg="green")
frame2.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)

# Frame 3
frame3 = tk.Frame(root, bg="blue")
frame3.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)

root.mainloop()