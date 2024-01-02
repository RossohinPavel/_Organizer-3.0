from ..._source import *
from ..order_name_validate_entry import ONVEntry
from .proxy import StickerGenProxy


class InfoFrame(ttk.Frame):
    """Общий фрейм информации о заказе"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, padding=(5, 0, 5, 5))

        # Фрейм генерации наклеек
        StickerGenFrame(self).pack(expand=1, fill='both')

        # Кнопки получения информации
        ttk.Button(self, text='Заказы', width=13).pack(side='left', padx=10, pady=(5, 0))
        ttk.Button(self, text='Клиенты', width=13).pack(side='right', padx=10, pady=(5, 0))



