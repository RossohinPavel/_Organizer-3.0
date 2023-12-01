from .._source import *


class ProcessingFrame:
    """Конструктор для фрейма отображающего статус обработки различных задач. Используется как контекстный менеджер"""  
    def __init__(self, frame: tb.Labelframe):
        self.header = tb.StringVar(master=frame)
        self._header_label = tb.Label(master=frame, textvariable=self.header, anchor='w', width=22)
        self.operation = tb.Meter(frame, metersize=160, interactive=True, textfont='-size 18 -weight bold', subtext='long_file_name', bootstyle='info')
        self.file = tb.Meter(frame, metersize=160, interactive=True, textfont='-size 18 -weight bold', subtext='long_file_name')
        self.__exit__()

    def __enter__(self) -> None:
        """При входе в менеджер, размещаем виджеты"""
        self._header_label.pack(pady=(0, 2))
        self.operation.pack()
        self.file.pack()

    def __exit__(self, *args) -> None:
        """При выходе - сбрасываем текстовые переменные и скрываем их виджеты"""
        self.header.set('__Имодуль__')
        self._header_label.pack_forget()
        self.operation.pack_forget()
        self.file.pack_forget()
