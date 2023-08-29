import tkinter as tk


root = tk.Tk()
root.geometry('100x100')

txt = tk.Label(master=root, text='text')
txt.pack(anchor='center', expand=1)


root.mainloop()