from .common import *


class StickGenFrame(LabeledFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Генератор наклеек', **kwargs)
        self.container.pack(expand=1)
        ONVFrame(master=self.container, func=lambda x: print(f'number {x}'), width=50, height=50).pack(pady=(3, 0), fill='both')
        src.ttk.Frame(master=self.container, borderwidth=1, relief='solid').pack(fill='x')
        src.ttk.Label(master=self.container, text='text').pack(anchor='nw', fill='both')
        src.MyButton(master=self.container, text='Скопировать инфо').pack(anchor='s', expand=1)