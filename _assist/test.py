import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip


app = ttk.Window(size=(500, 500), themename='flatly')


f = ScrolledFrame(app, autohide=True)
f.pack()


# chbtn = ttk.Checkbutton(
#     master=app,
#     text='test',
# )
# chbtn.place(x=10, y=10)


btn = ttk.Button(app, text='test', command=lambda: chbtn.event_generate('<<Invoke>>'))
btn.place(x=10, y=30)


app.mainloop()