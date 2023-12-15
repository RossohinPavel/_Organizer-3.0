from .._source import *
from re import match as re_match


class ONVFrame(ttk.Entry):
    """Класс для отрисовки фреймов проверки заказа и осуществления логики первичной валидации номера"""
    def __init__(self, master: Any, /, **kwargs):
        self._func = kwargs.pop('func')
        super().__init__(master, validate='key', **kwargs)
        self.focus_set()
        self.__insert_def_val()
        self.bind('<KeyPress>', self.__enter_event)
        self.config(validatecommand=(self.register(self.__validate), "%P"))

    def __enter_event(self, event):
        if self.get().startswith('#') and event.char.isdigit():
            self.delete(0, 'end')

    def __validate(self, value: str) -> bool:
        """Валидация введеных значений, вызов функции при полной валидации и очистка _entry"""
        res = re_match(r'\d{0,6}$', value) is not None
        if res and len(value) == 6:
            if self._func:
                self._func(value)
            self.__insert_def_val()
        return res

    def __insert_def_val(self, text='#Введите номер заказа', cursor=0) -> None:
        """Очитска _entry и вставка значения по умолчанию"""
        self.delete(0, 'end')
        self.insert(0, text)
        self.icursor(cursor)
