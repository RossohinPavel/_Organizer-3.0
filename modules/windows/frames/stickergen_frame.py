from .common import *
from modules.info_proxies import StickerGenProxy


class StickGenFrame(LabeledFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Генератор наклеек', **kwargs)
        self.container.pack(expand=1)
        ONVFrame(master=self.container, func=self.main, width=50, height=50).pack(pady=(3, 0), fill='both')
        src.ttk.Frame(master=self.container, borderwidth=1, relief='solid').pack(fill='x')
        self.header_var = src.tk.StringVar(master=self)
        src.ttk.Label(master=self.container, textvariable=self.header_var).pack(anchor='nw', fill='x')
        self.info_var = src.tk.StringVar(master=self)
        src.ttk.Label(master=self.container, textvariable=self.info_var).pack(anchor='nw', fill='both')
        src.MyButton(master=self.container, text='Скопировать инфо', command=self.to_clipboard).pack(anchor='s', expand=1)

    def main(self, order_name):
        proxy = StickerGenProxy(order_name)
        if proxy is None:
            self.header_var.set(f'Не могу найти заказ {order_name}')
            return
        self.header_var.set(f'{proxy.order.name} - {proxy.order.customer_name}')
        self.info_var.set(proxy.create_sticker())
        self.to_clipboard()

    def to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.info_var.get().encode('windows-1251').decode('windows-1251'))
