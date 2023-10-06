from tkinter import *
from tkinter import ttk


root = Tk()
root.geometry("250x200")

logo = PhotoImage(file='btn.png', width=100)

Button(text='test', image=logo, width=400, relief='flat').place(x=0, y=0)

root.mainloop()


