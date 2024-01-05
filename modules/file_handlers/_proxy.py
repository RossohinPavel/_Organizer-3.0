from ..app_manager import AppManager
from typing import Callable, Self, TypeVar


V = TypeVar('V')


class FileHandlerProxy:
    """Представление заказа для обработчиков файлов"""
    __slots__ = ('name', 'creation_date', 'content', 'products', 'files')

    def __new__(cls, order_name: str, predicate: Callable[[V], V | None]) -> Self | None:
        """
            Пытаемся получить объект заказа из лога. 
            Если удается, то на его основе создаем прокси объект.
            Добавлем только те объекты, которые есть библиотеке
            и для которых predicate вернул True.
        """
        order = AppManager.log.get(order_name)

        if order is None: 
            return None

        obj = super().__new__(cls)

        # Атрибуты информации
        obj.name = order.name
        obj.creation_date = order.creation_date

        # Коллекции для работы прокси объекта
        obj.content = order.content     # Ссылка на коллекцию тиражей заказа
        obj.products = tuple()          # Ссылка на коллекцию продуктов, соответсвующих тиражам

        # Наполняем obj.products объектами продуктов
        if order.content:
            obj.products = tuple(predicate(AppManager.lib.get(e.name)) for e in order.content)  #type: ignore

        return obj
