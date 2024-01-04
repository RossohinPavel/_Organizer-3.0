from ..app_manager import AppManager
from ..mytyping import Callable, Self


class FileHandlerProxy:
    """Представление заказа для обработчиков файлов"""
    __slots__ = 'name', 'creation_date', 'content', 'products', 'files'

    def __new__(cls, order_name: str, predicate: callable) -> Self:
        """
            Пытаемся получить объект заказа из лога. 
            Если удается, то на его основе создаем прокси объект.
            Добавлем только те объекты, которые есть библиотеке
            и для которых predicate вернул True.
        """
        order = AppManager.log.get(order_name)

        if order is None: 
            return None   # type: ignore

        obj = super().__new__(cls)
        obj.name = order.name
        obj.creation_date = order.creation_date
        obj.content = list(order.content)   # type: ignore
        obj.products = list(predicate(AppManager.lib.get(e.name)) for e in order.content)   # type: ignore
        obj.files = list()
        return obj
