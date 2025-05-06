import tkinter as tk

root = tk.Tk()
root.state("zoomed")

# Frame 1
frame1 = tk.Frame(root, bg="red")
frame1.place(relx=0, rely=0, relwidth=1, relheight=0.25)

# Frame 2
frame2 = tk.Frame(root, bg="green")
frame2.place(relx=0, rely=0.25, relwidth=0.5, relheight=0.75)

# Frame 3
frame3 = tk.Frame(root, bg="blue")
frame3.place(relx=0.5, rely=0.25, relwidth=0.5, relheight=0.65)


# Frame 4
frame4 = tk.Frame(root, bg="yellow")
frame4.place(relx=0.65 - 0.05, rely=0.25 + 0.375 - 0.05, relwidth=0.1, relheight=0.1)


root.mainloop()