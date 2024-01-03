import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip


app = ttk.Window(size=(500, 500), themename='flatly')





chbtn = ttk.Checkbutton(
    master=app,
    text='test',
)
chbtn.place(x=10, y=10)


btn = ttk.Button(app, text='test', command=lambda: chbtn.event_generate('<<Invoke>>'))
btn.place(x=10, y=30)


app.mainloop()