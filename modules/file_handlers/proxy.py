from ..app_manager import AppManager
from ..mytyping import Callable, Self, TypeVar


V = TypeVar('V')


class FileHandlerProxy:
    """Представление заказа для обработчиков файлов"""
    __slots__ = 'name', 'creation_date', 'content', 'products', 'files'

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

        # Списки для работы обработчика
        obj.content = []        # Список, в котором хранитятся оригинальные объекты тирежей
        obj.products = []       # Список, в котором хранятся объекты продуктов, соответствующие тиражам
        obj.files = []          # Список файловых объектов. Будет заполнен конкретным обрабочиком

        # Наполняем списки объектами тиражей и соответствующими продуктами
        if order.content:
            for e in order.content:
                obj.content.append(e)
                obj.products.append(predicate(AppManager.lib.get(e.name)))  #type: ignore

        return obj
