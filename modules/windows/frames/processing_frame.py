from .common import src as src
from modules.app_manager import AppManagerW


class ProcessingFrame(AppManagerW):
    """Конструктор для фрейма отображающего статус обработки различных задач. Используется как контекстный менеджер"""
    def __init__(self, frame):
        self._frame = frame
        self.header = src.tk.StringVar(master=frame)
        self.status = src.tk.StringVar(master=frame)
        self.qty = src.tk.StringVar(master=frame)
        self.pb = src.ttk.Progressbar(master=frame, orient='horizontal', length=243)
        self._widgets = [src.ttk.Label(master=self._frame, textvariable=self.header, width=40),
                         src.ttk.Label(master=self._frame, textvariable=self.status, width=40),
                         src.ttk.Label(master=self._frame, textvariable=self.qty, width=40), self.pb]

    def __enter__(self):
        place = 4
        for widget in self._widgets:
            widget.place(x=2, y=place)
            place += 24

    def __exit__(self, *args):
        self.header.set('__Имя модуля/номер заказа__')
        self.status.set('__Статус/имя тиража__')
        self.qty.set('__Количество__')
        self.pb['maximum'] = 0
        self.pb['value'] = 0
        for widget in self._widgets:
            widget.place_forget()
