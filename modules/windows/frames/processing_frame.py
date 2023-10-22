from ..source import *
from modules.app_manager import AppManager


class ProcessingFrame(LabeledFrame):
    storage = AppManager.storage
    __new__ = AppManager.write_to_storage('pf')
    
    """Конструктор для фрейма отображающего статус обработки различных задач. Используется как контекстный менеджер"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = tk.IntVar(master=self, value=0)
        ttk.Label(master=self, textvariable=self.queue).place(x=130, y=-9)
        ttk.Frame(master=self.container, width=300).pack()
        self.header = tk.StringVar(master=self)
        self.status = tk.StringVar(master=self)
        self.pb = ttk.Progressbar(master=self.container, orient='horizontal', length=298)
        self._widgets = [ttk.Label(master=self.container, textvariable=self.header, width=49),
                         ttk.Label(master=self.container, textvariable=self.status, width=49),
                         self.pb]

    def __enter__(self):
        """При входе в менеджер, размещаем виджеты"""
        place = 4
        for widget in self._widgets:
            widget.place(x=1, y=place)
            place += 24

    def __exit__(self, *args):
        """При выходе - сбрасываем текстовые переменные и скрываем их виджеты"""
        self.header.set('__Имя модуля/номер заказа__')
        self.status.set('__Статус/имя тиража__')
        self.pb['maximum'] = 0
        self.pb['value'] = 0
        for widget in self._widgets:
            widget.place_forget()
