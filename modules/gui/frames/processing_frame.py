from typing import Self
from .._source import *


class FileBar:
    """Интерфейс для управления лейблом и прогрессбаром"""
    __slots__ = ('_lbl', '_pb')

    def __init__(self, master: ctk.CTkFrame) -> None:
        self._lbl = ctk.CTkLabel(master, width=25)
        self._pb = ctk.CTkProgressBar(master, height=15, border_width=1)
    
    def reset(self) -> None:
        """Сбрасывает состояние Label и Progressbar до стартовых значений"""
        self._lbl.configure(text='__Имя файла__')
        self._pb['value'] = 0
        self._pb['maximum'] = 0

    def pack(self) -> None:
        """Размещение по алгоритму метода pack виджетов ttk.Label и ttk.Progressbar"""
        self._lbl.pack(anchor='nw', padx=5)
        self._pb.pack(anchor='nw', padx=5, pady=5, fill='x', expand=1)
    
    def pack_forget(self) -> None:
        """Затирание виджетов"""
        self._lbl.pack_forget()
        self._pb.pack_forget()
    
#     @property
#     def maximum(self) -> float:
#         """Получение значения maximum Progressbar'а"""
#         return self._pb['maximum']
    
#     @maximum.setter
#     def maximum(self, value: int | float) -> None:
#         """Установка значения maximum Progressbar'а"""
#         self._pb['maximum'] = value
    
#     def set(self, string: str = '') -> None:
#         """Установка строкового значения в виджет текста"""
#         self._lbl.config(text=f'{int(self._pb['value']) + 1}/{self._pb['maximum']} -- {string}')
    
#     def __iadd__(self, num: int | float) -> Self:
#         """Увеличиваем значение Progressbar'а через составное присваивание"""
#         self._pb['value'] += num
#         return self


class ProcessingFrame:
    """Конструктор для фрейма отображающего статус обработки различных задач. Используется как контекстный менеджер"""  
    def __init__(self, frame: ctk.CTkFrame):
        # Отрисовка лейбла очереди
        self.header = ctk.StringVar(master=frame)
        self._header_label = ctk.CTkLabel(master=frame, textvariable=self.header, width=25)
        self.operation = ctk.StringVar(master=frame)
        self._operation_label = ctk.CTkLabel(master=frame, textvariable=self.header, width=25)
        self.filebar = FileBar(master=frame)
        self.__exit__()

    def __enter__(self) -> None:
        """При входе в менеджер, размещаем виджеты"""
        self._header_label.pack(padx=5, anchor='nw')
        self._operation_label.pack(padx=5, anchor='nw')
        self.filebar.pack()

    def __exit__(self, *args) -> None:
        """При выходе - сбрасываем текстовые переменные и скрываем их виджеты"""
        self.header.set('__Исполняемый модуль / Название Задачи__')
        self.operation.set('__Название операции__')
        self.filebar.reset()
        self._header_label.pack_forget()
        self._operation_label.pack_forget()
        self.filebar.pack_forget()
