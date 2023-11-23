from .._source import *
from ..windows import *


class ControlFrame(tb.Frame):
    def __init__(self, master: Any):
        super().__init__(master, padding=(5, 5, 4, 5))
        self.show_greetings_lbl()
        self.show_buttons()

    def show_greetings_lbl(self):
        container = tb.Frame(self)
        container.pack(fill='both', expand=1)
        tb.Label(container, text='Спасибо').pack(expand=1, side='left')
        tb.Frame(container, width=1, height=410).pack(side='right')
    
    def print_geometry(self):
        print(self.master.master.winfo_geometry())

    def show_buttons(self):
        container = tb.Frame(self)
        container.pack(fill='x')
        tb.Button(container, text='Библиотека', width=13).pack(side='left')
        tb.Button(container, text='Настройки', width=13).pack(side='right', padx=(0, 1))
        tb.Button(container, text='P_G', width=5, command=self.print_geometry).pack(side='right', padx=5)
