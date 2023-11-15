class FileHandlerProxy:
    """Представление заказа для обработчиков файлов"""
    __slots__ = 'name', 'creation_date', 'content', 'products', 'files'

    def __new__(cls, order_name: str, predicate: callable):
        """Пытаемся получить объект заказа из лога. Если удается, то на его основе создаем прокси объект.
        Добавлем только те объекты, которые есть библиотеке и для которых predicate вернул True"""
        order = AppManager.storage.log.get(order_name)
        if order is None:
            return None
        obj = super().__new__(cls)
        obj.name = order.name
        obj.creation_date = order.creation_date
        obj.content = list(order.content)
        obj.products = list(predicate(AppManager.storage.lib.get_product_obj_from_name(e.name)) for e in order.content)
        obj.files = list()
        return obj
