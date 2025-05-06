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
frame3.place(relx=0.5, rely=0.25, relwidth=0.5, relheight=0.75)


# Frame 4
frame4 = tk.Frame(root, bg="yellow")
frame4.place(relx=0.4, rely=0.15 , relwidth=0.15, relheight=0.20)


root.mainloop()