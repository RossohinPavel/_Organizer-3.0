from ..._source import *
from ..order_name_validate_frame import ONVFrame
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


class StickerGenFrame(ttk.LabelFrame):
    def __init__(self, master: Any, /, **kwargs):
        super().__init__(master, text='Генератор наклеек')
        ONVFrame(master=self, func=self.main).pack(pady=(3, 5), fill='both')
        ttk.Frame(master=self, borderwidth=1, relief='solid').pack(fill='x')
        self.header_var = ttk.StringVar(master=self)
        ttk.Label(master=self, textvariable=self.header_var).pack(anchor='nw', fill='x')
        self.info_var = ttk.StringVar(master=self)
        ttk.Label(master=self, textvariable=self.info_var).pack(anchor='nw', fill='both')
        ttk.Button(master=self, text='Скопировать инфо', command=self.to_clipboard).pack(anchor='s', expand=1)

    def main(self, order_name):
        proxy = StickerGenProxy(order_name)
        if proxy is None:
            self.header_var.set(f'Не могу найти заказ {order_name}')
            self.info_var.set('')
            return
        self.header_var.set(f'{proxy.order.name} - {proxy.order.customer_name}')
        self.info_var.set(proxy.create_sticker())
        self.to_clipboard()

    def to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.info_var.get())
