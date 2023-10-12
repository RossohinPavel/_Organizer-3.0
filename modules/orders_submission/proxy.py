from ..app_manager import AppManagerR


class OrderProxy(AppManagerR):
    __slots__ = 'order', 'product_comp'

    def __new__(cls, order_name):
        """Пытаемся получить объект заказа из лога. Если удается, то на его основе создаем прокси объект"""
        order = cls.app_m.log.get(order_name)
        if order is not None:
            res = super().__new__(cls)
            res.order = order
            res.product_comp = {x.name: cls.app_m.lib.get_product_obj_from_name(x.name) for x in order.content}
            return res
