from ...source import *


class StickerGenFrame(ttk.Frame):
    """Фрейм генерации стикера"""

    def __init__(self, master: Any, padding: int | tuple[int, ...]):
        super().__init__(master, padding=padding)   # type:  ignore
        HeaderLabel(self, text='Генератор наклеек').pack(fill=ttkc.X, pady=(0, 2))

        # Верхнаяя чать. Поле ввода и кнопка

        container = ttk.Frame(self)
        container.pack(fill=ttkc.X)

        # # onvf = ONVEntry(container, func=self.main)
        onvf = ttk.Entry(container)
        onvf.pack(fill=ttkc.X, pady=(0, 5))

        # # Разделитель
        # ttk.Separator(master=self, orient='horizontal').pack(fill=ttkc.X, pady=5)

        # # Переменные и лейблы под них
        # self.header_var = ttk.StringVar(master=self, value='223344 - Test Name')
        # ttk.Label(master=self, textvariable=self.header_var).pack(anchor=ttkc.NW, padx=10)

        t = ttk.Text(self)
        t.pack(anchor=ttkc.NW, fill=ttkc.BOTH)

        t.insert('1.0', 'test\ntest')

        # self.info_var = ttk.StringVar(master=self, value='1\n2\n3\n4\n5\n6\n7\n8\n9\n10')
        # ttk.Label(master=self, textvariable=self.info_var, background='red').pack(anchor=ttkc.NW, fill=ttkc.X)
        
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