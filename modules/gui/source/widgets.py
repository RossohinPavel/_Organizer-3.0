from .main import *
from re import match as re_match
from typing import Literal, Callable, Type


class HeaderLabel(ttk.Frame):
    """Фрейм - заголовок, с надписью и подчеркиванием."""

    def __init__(
        self, 
        master: Any, 
        text: str = '', 
        anchor: Literal['w', 'n', 'e'] = 'w',
        padx: int = 15
        ):
        super().__init__(master)

        # Разделитель
        ttk.Separator(self, orient='horizontal').place(relwidth=1.0, rely=0.39)

        # Лейбл с текстом
        self.lbl = ttk.Label(self, text=text, padding=(0, -5, 0, -2))
        match anchor:
            case 'n': justify = 0
            case 'e': justify = (0, padx)
            case 'w' | _ : justify = (padx, 0)
        self.lbl.pack(anchor=anchor, padx=justify)


class ONVEntry(ttk.Entry):
    """Класс для отрисовки фреймов проверки заказа и осуществления логики первичной валидации номера"""
    def __init__(self, master: Any, _func: Callable[[str], None], **kwargs):
        self._func = _func
        super().__init__(master, validate='key', **kwargs)
        self.__insert_def_val()
        self.bind('<KeyPress>', self.__enter_event)
        self.config(validatecommand=(self.register(self.__validate), "%P"))

    def __enter_event(self, event):
        """Событие для очитски виджета от от текста, который там находится по умолчанию"""
        if self.get().startswith('#') and event.char.isdigit():
            self.delete(0, 'end')

    def __validate(self, value: str) -> bool:
        """Валидация введеных значений, вызов функции при полной валидации и очистка _entry"""
        res = re_match(r'\d{0,6}$', value) is not None
        if res and len(value) == 6:
            self._func(value)
            self.__insert_def_val()
        return res

    def __insert_def_val(self) -> None:
        """Очитска _entry и вставка значения по умолчанию"""
        self.delete(0, 'end')
        self.insert(0, '#Введите номер заказа')
        self.icursor(0)


class SettingLine(ttk.Frame):
    """Конструктор для отображения кнопки с иконкой шестеренки и лейбла настроек."""

    def __init__(
        self,
        master: Any, 
        _func: Type[Callable[[], None]],
        _prefix: str = '',
        _postfix: str = ''
        ):
        super().__init__(master)

        # Кнопка вызова настроек
        btn = ttk.Button(
            self, 
            style='stg.Outline.TButton',
            text='⚙️',  
            command=_func
        )
        btn.pack(anchor=ttkc.W, side=ttkc.LEFT, padx=(0, 1))

        if _func is None:
            btn.configure(command=lambda: print(btn.winfo_geometry()))

        # Лейбл для отображения текста приставки, поясняющей суть настройки
        if _prefix:
            ttk.Label(self, text=_prefix).pack(anchor=ttkc.W, side=ttkc.LEFT)
        
        # Лейбл для отображения информации, полученной в результате вызова функции настройки
        self._var = ttk.StringVar(self)
        ttk.Label(self, textvariable=self._var).pack(anchor=ttkc.W, side=ttkc.LEFT)

        # Лейбл для отображения текста суффикса, поясняющей суть настройки
        if _postfix:
            ttk.Label(self, text=_postfix).pack(anchor=ttkc.W, side=ttkc.LEFT)
