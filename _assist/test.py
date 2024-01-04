import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.icons import Icon
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip


app = ttk.Window(size=(500, 500), themename='flatly')

img = ttk.PhotoImage(master=app, file='../data/assets/question.png')


lbl = ttk.Label(app, image=img)
lbl.pack()

btn = ttk.Button(app, image=img)
btn.pack()

lst = ['value1', 'value2']

cb = ttk.Combobox(app, values=lst)
cb.pack()


lst.pop(0)
# chbtn = ttk.Checkbutton(
#     master=app,
#     text='test',
# )
# chbtn.place(x=10, y=10)


# btn = ttk.Button(app, text='test', command=lambda: chbtn.event_generate('<<Invoke>>'))
# btn.place(x=10, y=30)


app.mainloop()