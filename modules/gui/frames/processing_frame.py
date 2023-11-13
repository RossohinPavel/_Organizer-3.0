from typing import Self
from .._source import *


class FileBar:
    """Интерфейс для управления лейблом и прогрессбаром"""
    __slots__ = ('_lbl', '_pb')

    def __init__(self, master: tk.Misc | None) -> None:
        self._lbl = ttk.Label(master, width=49)
        self._pb = ttk.Progressbar(master, orient='horizontal')
    
    def reset(self) -> None:
        """Сбрасывает состояние Label и Progressbar до стартовых значений"""
        self._lbl.config(text='__Имя файла__')
        self._pb['value'] = 0
        self._pb['maximum'] = 0

    def pack(self, *args, **kwargs) -> None:
        """Размещение по алгоритму метода pack виджетов ttk.Label и ttk.Progressbar"""
        self._lbl.pack(*args, **kwargs)
        self._pb.pack(*args, **kwargs)
    
    def pack_forget(self) -> None:
        """Затирание виджетов"""
        self._lbl.pack_forget()
        self._pb.pack_forget()
    
    @property
    def maximum(self) -> float:
        """Получение значения maximum Progressbar'а"""
        return self._pb['maximum']
    
    @maximum.setter
    def maximum(self, value: int | float) -> None:
        """Установка значения maximum Progressbar'а"""
        self._pb['maximum'] = value
    
    def set(self, string: str = '') -> None:
        """Установка строкового значения в виджет текста"""
        self._lbl.config(text=f'{self._pb['value'] + 1}/{self._pb['maximum']} -- {string}')
    
    def __iadd__(self, num: int | float) -> None:
        """Увеличиваем значение Progressbar'а через составное присваивание"""
        self._pb['value'] += num


class ProcessingFrame(LabeledFrame):
    """Конструктор для фрейма отображающего статус обработки различных задач. Используется как контекстный менеджер"""
    __instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Отрисовка лейбла очереди
        self.queue = tk.IntVar(master=self, value=0)
        ttk.Label(master=self, textvariable=self.queue).place(x=130, y=-9)
        self.header = tk.StringVar(master=self.container)
        self.operation = tk.StringVar(master=self.container)
        self.filebar = FileBar(master=self.container)
        self._widgets = [ttk.Label(master=self.container, textvariable=self.header, width=49),
                         ttk.Label(master=self.container, textvariable=self.operation, width=49),
                         self.filebar]

    def __enter__(self) -> None:
        """При входе в менеджер, размещаем виджеты"""
        for widget in self._widgets: 
            widget.pack(expand=1, fill='x')

    def __exit__(self, *args) -> None:
        """При выходе - сбрасываем текстовые переменные и скрываем их виджеты"""
        self.header.set('__Исполняемый модуль / Название Задачи__')
        self.operation.set('__Название операции__')
        self.filebar.reset()
        for widget in self._widgets:
            widget.pack_forget()
