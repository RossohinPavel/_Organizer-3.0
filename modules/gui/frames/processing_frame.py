from .._source import *


class QueueDescriptor:
    """Дескриптор для очереди выполнения задач"""
    __slots__ = '_value'

    def __init__(self) -> None:
        self._value = 0
    
    def __get__(self, *_) -> int: 
        return self._value
    
    def __set__(self, obj: Any, value: int) -> None:
        self._value = value
        obj._desc_bound_method()


class ProcessingFrame(ttk.LabelFrame):
    """Конструктор для фрейма отображающего статус обработки различных задач. Используется как контекстный менеджер"""
    queue = QueueDescriptor()  
    
    def __init__(self, master: Any, /, **kwargs):
        super().__init__(master, padding=(5, 0, 5, 5), **kwargs)

        # Переменная очереди выполнения задач
        self.queue = 0

        # Лейбл для отображения названия модуля
        self.header = HeaderLabel(self)

        # Интерфейс операций
        self.operation = OperationLabel(self)

        # Файловый интерфейс
        self.filebar = FileBar(self)

    def _desc_bound_method(self):
        """Обновляет заголовок фрейма в зависимости от количества выполняемых задач"""
        self.configure(text=f'Задач в очереди: {self.queue}')

    def __enter__(self) -> None:
        """При входе в менеджер, размещаем виджеты"""
        self.header.pack(anchor=ttkc.W, expand=1)
        self.operation.pack(anchor=ttkc.W, expand=1)
        self.filebar.pack(anchor=ttkc.W, expand=1, fill=ttkc.BOTH)

    def __exit__(self, *args) -> None:
        """При выходе - сбрасываем текстовые переменные и скрываем их виджеты"""
        for widget in (self.header, self.operation, self.filebar):
            widget.reset()
            widget.pack_forget()


class HeaderLabel(ttk.Label):
    """Интерфейс для текста заголовка"""

    def step(self, value: str):
        """Установка текста лейбла"""
        self.configure(text=value)
    
    def reset(self):
        """Сбрасывает значения виджетов до начальных"""
        self.configure(text='__DEBUG__')


class OperationLabel(ttk.Label):
    """Интерфейс для упрощения обработки операций и их названий"""

    def __init__(self, master: ttk.LabelFrame, /, **kwargs) -> None:
        super().__init__(master, text='__Operation_Name__', **kwargs)
        self.__value = 0
        self.maximum = 1

    def step(self, value: str) -> None:
        """Установка значения в текстовую переменную"""
        self.__value += 1
        prefix = f'{self.__value} / {self.maximum} -- ' if self.maximum > 1 else ''
        self.configure(text=f'{prefix}{value}')
    
    def reset(self) -> None:
        """Сбрасывает значения виджетов до начальных"""
        self.__value = 0
        self.maximum = 1


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
        self.__pb = ttk.Progressbar(self, style='success-striped')
        self.__pb.pack(
            anchor=ttkc.W, 
            expand=1, 
            fill=ttkc.X, 
            side=ttkc.LEFT,
            padx=(0, 5)
            )
        # Лейбл отображения процента
        self.__lbl1 = ttk.Label(self, text='100.0%', width=6, justify='left')
        self.__lbl1.pack(side=ttkc.RIGHT, anchor=ttkc.E)

    def maximum(self, value: int, percentage: int = 100) -> None:
        """
        Устанавливает предельное значение
        value: общее количество шагов (файлов, объектов и т.д)
        percentage: Сколько в процентном соотношении от 100, займет прогрессия 
        """
        self.__maximum = value
        self.__delta = percentage / value
    
    def step(self, value: str) -> None:
        """Начало шага. Устанавливает значение в текстовую переменную"""
        self.__value += 1
        prefix = f'{self.__value} / {self.__maximum} -- ' if self.__maximum > 1 else ''
        self.__lbl.configure(text=f'{prefix}{value}')
        
    def step_end(self) -> None:
        """Конец шага. Продвигает прогрессбар"""
        self.__pb['value'] += self.__delta
        self.__lbl1.configure(text=str(round(self.__pb['value'], 1)) + '%')

    def reset(self) -> None:
        """Сбрасывает значения виджетов до начальных"""
        self.__pb['value'] = 0
        self.__value = 1
        self.__delta = 1.0
        self.__maximum = 100
