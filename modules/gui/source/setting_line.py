from .main import *
from ...mytyping import Callable, Type


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
