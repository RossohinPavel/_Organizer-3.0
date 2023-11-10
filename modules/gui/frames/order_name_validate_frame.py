from .._source import *
from re import match as re_match


class ONVFrame(ttk.Frame):
    """Класс для отрисовки фреймов проверки заказа и осуществления логики первичной валидации номера"""
    def __init__(self, *args, func=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._func = func
        self._entry = ttk.Entry(master=self, width=22, validate='key')
        self._entry.pack(anchor='n', pady=(0, 3))
        self._entry.focus_set()
        self.__insert_def_val()
        self._entry.bind('<KeyPress>', self.__enter_event)
        self._entry.config(validatecommand=(self.register(self.__validate), "%P"))

    def __enter_event(self, event):
        if self._entry.get().startswith('#') and event.char.isdigit():
            self._entry.delete(0, 'end')

    def __validate(self, value: str) -> bool:
        """Валидация введеных значений, вызов функции при полной валидации и очистка _entry"""
        res = re_match(r'\d{0,6}$', value) is not None
        if res and len(value) == 6:
            if self._func:
                self._func(value)
            self.__insert_def_val()
        return res

    def __insert_def_val(self, text='#Введите номер заказа', cursor=0):
        """Очитска _entry и вставка значения по умолчанию"""
        self._entry.delete(0, 'end')
        self._entry.insert(0, text)
        self._entry.icursor(cursor)
