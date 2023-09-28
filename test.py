import tkinter as tk
import tkinter.ttk as ttk
import re


class LabeledFrame(ttk.Frame):
    def __init__(self, *args, text='', **kwargs):
        super().__init__(*args, padding=(5, 8, 5, 5), **kwargs)
        self.container = ttk.Frame(master=self, width=50, height=50, borderwidth=1, padding=(2, 4, 2, 2), relief='solid')
        self.container.pack(fill='both')
        ttk.Label(master=self, text=text).place(x=3, y=-10)


root = tk.Tk()
root.geometry('200x200')

frame = LabeledFrame(master=root, text='test')
frame.pack(fill='both')

ttk.Label(master=frame.container, text='text_inside').pack(anchor='nw')

root.mainloop()