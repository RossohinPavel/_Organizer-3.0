from ..source import *


class PlanerFrame(ttk.LabelFrame):
    def __init__(self, master: Any, /, **kwargs):
        super().__init__(master, text='Планировщик', **kwargs)