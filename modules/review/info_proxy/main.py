from ...app_manager import AppManager

# Типизация
from typing import Iterator, Self
from ..library import Product
from ..log import Order, Edition


class InfoProxy:
    """Прокси-объект, содержащий в себе объект заказа и записи из библиотеки"""
    __slots__ = 'order', 'product_comp'

    def __new__(cls, order_name: str) -> Self | None:
        """
            Пытаемся получить объект заказа из лога. 
            Если удается, то на его основе создаем прокси объект
        """
        order = AppManager.log.get(order_name)
        
        if order is not None:
            res = super().__new__(cls)

            # ссылка на заказ
            res.order = order

            # Соответствующие тиражам продукты из библиотеки
            res.product_comp = tuple(AppManager.lib.get(x.name) for x in order.content)  # type: ignore

            return res
    
    def __init__(self, order_name: str) -> None:
        self.order: Order
        self.product_comp: tuple[Product, ...]
