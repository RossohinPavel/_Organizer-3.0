from typing import Self
from .._source import *


# class FileBar:
#     """Интерфейс для управления лейблом и прогрессбаром"""
#     __slots__ = ('_lbl', '_pb')

#     def __init__(self, master: tk.Misc | None) -> None:
#         self._lbl = ttk.Label(master, width=49)
#         self._pb = ttk.Progressbar(master, orient='horizontal')
    
#     def reset(self) -> None:
#         """Сбрасывает состояние Label и Progressbar до стартовых значений"""
#         self._lbl.config(text='__Имя файла__')
#         self._pb['value'] = 0
#         self._pb['maximum'] = 0

#     def pack(self, *args, **kwargs) -> None:
#         """Размещение по алгоритму метода pack виджетов ttk.Label и ttk.Progressbar"""
#         self._lbl.pack(*args, **kwargs)
#         self._pb.pack(*args, **kwargs)
    
#     def pack_forget(self) -> None:
#         """Затирание виджетов"""
#         self._lbl.pack_forget()
#         self._pb.pack_forget()
    
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


class ProcessingFrame(ctk.CTkFrame):
    """Конструктор для фрейма отображающего статус обработки различных задач. Используется как контекстный менеджер"""  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Отрисовка лейбла очереди
        self.header = ctk.StringVar(master=self)
        self._header_label = ctk.CTkLabel(master=self.container, textvariable=self.header, width=49)
        self.operation = tk.StringVar(master=self.container)
        self._operation_label = ttk.Label(master=self.container, textvariable=self.operation, width=49)
        self.filebar = FileBar(master=self.container)

    def __enter__(self) -> None:
        """При входе в менеджер, размещаем виджеты"""
        self._header_label.pack(expand=1, fill='x')
        self._operation_label.pack(expand=1, fill='x')
        self.filebar.pack(expand=1, fill='x')

    def __exit__(self, *args) -> None:
        """При выходе - сбрасываем текстовые переменные и скрываем их виджеты"""
        self.header.set('__Исполняемый модуль / Название Задачи__')
        self.operation.set('__Название операции__')
        self.filebar.reset()
        self._header_label.pack_forget()
        self._operation_label.pack_forget()
        self.filebar.pack_forget()
