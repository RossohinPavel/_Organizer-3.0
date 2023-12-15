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
    """Фрейм генерации стикера"""

    def __init__(self, master: Any, /, **kwargs):
        super().__init__(master, text='Генератор наклеек')
        # Верхнаяя чать. Поле ввода и кнопка
        container = ttk.Frame(self, padding=(5, 3, 5, 5))
        container.pack(fill=ttkc.X)

        onvf = ONVFrame(container, func=self.main)
        onvf.pack(
            padx=(0, 3), 
            fill=ttkc.X,
            side=ttkc.LEFT,
            expand=1
            )
        btn = ttk.Button(
            master=container, 
            text='Скопировать инфо', 
            command=self.to_clipboard,
            style='info-outline'
            )
        btn.pack(
            padx=(2, 0), 
            fill=ttkc.X,
            side=ttkc.RIGHT,
            expand=1
            )
        # Разделитель
        ttk.Frame(master=self, borderwidth=1, relief='solid').pack(fill='x')

        # Переменные и лейблы под них
        self.header_var = ttk.StringVar(master=self)
        ttk.Label(master=self, textvariable=self.header_var).pack(anchor='nw', fill='x')

        self.info_var = ttk.StringVar(master=self)
        ttk.Label(master=self, textvariable=self.info_var).pack(anchor='nw', fill='both')
        
    def main(self, order_name: str) -> None:
        """После валидации введенного номера, обновляет лейбл"""
        proxy = StickerGenProxy(order_name)
        if proxy is None:
            self.header_var.set(f'Не могу найти заказ {order_name}')
            self.info_var.set('')
            return
        self.header_var.set(f'{proxy.order.name} - {proxy.order.customer_name}')
        self.info_var.set(proxy.create_sticker())
        self.to_clipboard()

    def to_clipboard(self):
        """Копирования информации в буфер обмена"""
        self.clipboard_clear()
        self.clipboard_append(self.info_var.get())
