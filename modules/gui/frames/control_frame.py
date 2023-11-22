from .._source import *
from ..windows import *


class ControlFrame(tb.Frame):
    def __init__(self, master: Any):
        super().__init__(master, padding=5)
        self.show_greetings_lbl()
        self.show_buttons()

    def show_greetings_lbl(self):
        container = tb.Frame(self)
        tb.Label(master=container, text='Спасибо').pack()
        container.pack(side='left', expand=1, fill='both')
        tb.Frame(self, height=240).pack(side='left')    # Выравниватель)))
    
    def print_geometry(self):
        print(self.master.master.winfo_geometry())

    def show_buttons(self):
        container = tb.Frame(self)
        tb.Button(container, text='Клиенты', width=13).pack(pady=(0, 5), anchor='n')
        tb.Button(container, text='Библиотека', width=13).pack(pady=(0, 5))
        tb.Button(container, text='Информация', width=13).pack(pady=(0, 5))
        tb.Button(container, text='Настройки', width=13).pack(pady=(0, 5))
        tb.Button(container, text='PrintGeometry', width=13, command=self.print_geometry).pack()
        container.pack(side='right', fill='y')
