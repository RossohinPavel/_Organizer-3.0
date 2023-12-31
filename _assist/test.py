import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

app = ttk.Window(size=(500, 500))

frame = ttk.Frame(app, width=300, height=300, style='success')
frame.pack()

# btn = ttk.Button(frame, text='test')
# btn.pack(after=frame)


app.mainloop()