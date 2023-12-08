from .._source import *


class ProcessingInterface:
    """Конструктор для фрейма отображающего статус обработки различных задач. Используется как контекстный менеджер"""  

    __slots__ = 'header', '__header_lbl', 'operation', 'filebar'
    
    def __init__(self, frame: ttk.Labelframe):
        # Текстовая пременная и лейбл модуля
        self.header = ttk.StringVar(frame, value='__Module_Name__')
        self.__header_lbl = ttk.Label(frame, textvariable=self.header)

        # Интерфейс операций
        self.operation = OperationLabel(frame)

        # Интерфейс фалов
        self.filebar = FileBar(frame)

    def __enter__(self) -> None:
        """При входе в менеджер, размещаем виджеты"""
        self.__header_lbl.pack(anchor=ttkc.W, expand=1)
        self.operation.pack(anchor=ttkc.W, expand=1)
        self.filebar.pack(anchor=ttkc.W, expand=1, fill=ttkc.BOTH)

    def __exit__(self, *args) -> None:
        """При выходе - сбрасываем текстовые переменные и скрываем их виджеты"""
        self.__header_lbl.pack_forget()
        self.operation.pack_forget()
        self.operation.reset()
        self.filebar.pack_forget()
        self.filebar.reset()


class OperationLabel(ttk.Label):
    """Интерфейс для упрощения обработки операций и их названий"""

    def __init__(self, master: ttk.LabelFrame, /, **kwargs) -> None:
        super().__init__(master, text='__Operation_Name__', **kwargs)
        self.__value = -1
        self.maximum = 0

    def set(self, value: str) -> None:
        """Установка значения в текстовую переменную"""
        self.__value += 1
        self.configure(text=f'{self.__value} / {self.maximum} -- {value}')
    
    def reset(self) -> None:
        """Сбрасывает значения виджетов до начальных"""
        self.__value = -1
        self.maximum = 0


class FileBar(ttk.Frame):
    """Интерфейс для управления виджетами файлов"""

    def __init__(self, master: ttk.LabelFrame, /, **kwargs) -> None:
        super().__init__(master, **kwargs)

        # Лейбл отображения имени файла
        self.__lbl = ttk.Label(self, text='__long_file_name__')
        self.__lbl.pack(anchor=ttkc.W, expand=1)

        # Переменные для прогрессбара и лейблов
        self.__value = 1
        self.__delta = 1.0
        self.__maximum = 100

        # Прогрессбар
        self.__pb = ttk.Progressbar(self)
        self.__pb.pack(
            anchor=ttkc.W, 
            expand=1, 
            fill=ttkc.X, 
            side=ttkc.LEFT,
            padx=(0, 10)
            )
        # Лейбл отображения процента
        self.__lbl1 = ttk.Label(self, text='100.0%', width=6, justify='left')
        self.__lbl1.pack(side=ttkc.RIGHT, anchor=ttkc.E)
    
    @property
    def maximum(self) -> int:
        """Возвращает предельное значение интерфейса"""
        return self.__maximum

    @maximum.setter
    def maximum(self, value: int) -> None:
        """Устанавливает предельное значение"""
        self.__maximum = value
        self.__delta = 100 / value
        self.__pb['value'] -= self.__delta

    def set(self, value: str) -> None:
        """Устанавливает value в лейблы и продвигает прогрессбар"""
        self.__pb['value'] += self.__delta
        self.__value += 1
        self.__lbl.configure(text=f'{self.__value} / {self.__maximum} -- {value}')
        self.__lbl1.configure(text=str(round(self.__pb['value'], 1)) + '%')
    
    def reset(self) -> None:
        """Сбрасывает значения виджетов до начальных"""
        self.__pb['value'] = 0
        self.__value = 1
        self.__delta = 1.0
        self.__maximum = 100
