import tkinter as tk
import tkinter.ttk as ttk


root = tk.Tk()

pb = ttk.Progressbar(master=root)
pb.pack()

pb += 1

root.mainloop()