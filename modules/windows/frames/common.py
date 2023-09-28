import modules.windows.source as src
from re import match as re_match


class LabeledFrame(src.ttk.Frame):
    """Конструктор для фрейма с надписью"""
    def __init__(self, *args, text='', **kwargs):
        super().__init__(*args, padding=(3, 7, 3, 3), **kwargs)
        self.container = src.ttk.Frame(master=self, width=50, height=50, borderwidth=1, padding=(2, 6, 2, 2), relief='solid')
        self.container.pack(fill='both')
        src.ttk.Label(master=self, text=text).place(x=20, y=-9)


class ONVFrame(src.ttk.Frame):
    """Класс для отрисовки фреймов проверки заказа и осуществления логики первичной валидации номера"""
    def __init__(self, *args, func=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._func = func
        self._entry = src.ttk.Entry(master=self, width=22, validate='key')
        self._entry.pack(anchor='n', pady=(0, 3))
        self._entry.focus_set()
        self.__insert_def_val()
        self._entry.config(validatecommand=(self.register(self.__validate), "%P"))

    def __validate(self, value: str) -> bool:
        """Валидация введеных значений, вызов функции при полной валидации и очистка _entry"""
        if value == '':
            self.__insert_def_val()
        if len(value) > 6:
            value = value[0]
        res = re_match(r'\d{0,6}$', value) is not None
        if res:
            if len(value) == 1:
                self.__insert_def_val(value, 1)
            if len(value) == 6:
                self._func(value)
                self.__insert_def_val()
        return res

    def __insert_def_val(self, text='#Введите номер заказа', cursor=0):
        """Очитска _entry и вставка значения по умолчанию"""
        self._entry.delete(0, 'end')
        self._entry.insert(0, text)
        self._entry.icursor(cursor)
