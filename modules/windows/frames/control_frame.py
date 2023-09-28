from .common import *
from modules.windows.settings import SettingsWindow
from modules.windows.library import LibraryWindow


class ControlFrame(LabeledFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Управление приложением', **kwargs)
        self.container.pack(expand=1)
        root_master = self.master.master.master
        src.MyButton(master=self.container, text="Настройки", command=lambda: SettingsWindow(root_master), width=16).pack(pady=(55, 4))
        src.MyButton(master=self.container, text="Библиотека", command=lambda: LibraryWindow(root_master), width=16).pack()
        src.MyButton(master=self.container, text="Информация", command=None, width=16).pack(pady=4)
