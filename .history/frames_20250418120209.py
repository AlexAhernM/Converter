import tkinter as tk

root = tk.Tk()
root.state("zoomed")


frame1 = tk.Frame(root, bg="red")
frame1.place(relx=0, rely=0, relwidth=0.2, relheight=0.2)

frame2 = tk.Frame(root, bg="blue")
frame2.place(relx=0, rely=0.5, relwidth=0.8, relheight=0.8)

frame3 = tk.Frame(root, bg="green")
frame3.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8)

root.mainloop()