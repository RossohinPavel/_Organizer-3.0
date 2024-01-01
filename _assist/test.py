import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

app = ttk.Window(size=(500, 500))


img = ttk.PhotoImage(master=app, file='../data/assets/badge.png')

lbl = ttk.Label(app, image=img, text=1, compound='center', foreground='white')
lbl.place(x=20, y=20)

# lbl1 = ttk.Label(app, text=1)
# lbl1.place(x=20, y=20)

# btn = ttk.Button(frame, text='test')
# btn.pack(after=frame)


app.mainloop()