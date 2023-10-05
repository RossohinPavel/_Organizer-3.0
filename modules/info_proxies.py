from modules.app_manager import AppManagerR


class OrderProxy(AppManagerR):
    __slots__ = 'order', 'product_comp'

    def __new__(cls, order_name):
        order = cls.app_m.log.get(order_name)
        if order is not None:
            res = super().__new__(cls)
            res.order = order
            res.product_comp = {}
            return res
