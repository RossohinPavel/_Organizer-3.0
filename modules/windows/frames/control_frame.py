from ..source import *
from ..settings import SettingsWindow as StgWin
from ..library import LibraryWindow as LibWin


class ControlFrame(LabeledFrame):
    """Фрейм для отрисовки кнопок управления приложением"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Управление приложением', **kwargs)
        root_master = self.master.master.master
        frame = ttk.Frame(master=self.container)
        frame.pack(anchor='center', expand=1)
        MyButton(master=frame, text="Клиенты", command=None, width=16).pack(pady=(0, 3))
        MyButton(master=frame, text="Библиотека", command=lambda: LibWin(root_master), width=16).pack(pady=(0, 3))
        MyButton(master=frame, text="Информация", command=None, width=16).pack(pady=(0, 3))
        MyButton(master=frame, text="Настройки", command=lambda: StgWin(root_master), width=16).pack()
