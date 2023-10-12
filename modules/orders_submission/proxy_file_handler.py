from ..app_manager import AppManagerR


class FileHandlerProxy(AppManagerR):
    """Представление заказа для обработчиков файлов"""
    __slots__ = 'order', 'creation_date', 'target', 'miss'

    def __new__(cls, order_name: str, predicate: callable):
        """Пытаемся получить объект заказа из лога. Если удается, то на его основе создаем прокси объект.
        Добавлем только те объекты, которые есть библиотеке и для которых predicate вернул True"""
        order = cls.app_m.log.get(order_name)
        if order is None:
            return None
        obj = super().__new__(cls)
        obj.order = order.name
        obj.creation_date = order.creation_date
        obj.target = {}
        obj.miss = []
        for edition in order.content:
            product = cls.app_m.lib.get_product_obj_from_name(edition.name)
            if product and predicate(product):
                obj.target[edition] = product
            if product is None:
                obj.miss.append(edition.name)
        return obj
