from .common import *
from modules.order_proxies.info import OrderProxy


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
        src.MyButton(master=self.container, text='Скопировать инфо').pack(anchor='s', expand=1)

    def main(self, order_name):
        proxy = OrderProxy(order_name)
        if proxy is None:
            self.header_var.set(f'Не могу найти заказ {order_name}')
            return
        self.header_var.set(f'{proxy.order.name} - {proxy.order.customer_name}')
        order_dct = proxy.get_order_content_info()
        print(order_dct)