from collections import namedtuple
from typing import Iterator, TYPE_CHECKING, Any


if TYPE_CHECKING:
    from .proxy_edition import Edition
    from .proxy_info import OrderInfoProxy
    from .proxy_photo import Photo


type DATA = Photo | Edition


class ProxyObserver:
    """Реализует общую логику наблюдения за объектом"""
    __slots__ = '_count', 'trackable', 'info_proxy', '_path', 'name', 'data', '_hash'

    def __init__(self, info_proxy: Any, order_path: str, name: str) -> None:
        # Атрибуты управления прокси-объектом
        self._count = 0                     # Счетчик итераций обновления объекта
        self.trackable = True               # Метка для обновления

        # Информационные атрибуты
        self.info_proxy: OrderInfoProxy = info_proxy        # ссылка на прокси объект информации о заказе
        self._path = f'{order_path}/{name}' # Абсолютный путь до заказа
        self.name = name

        # Создаем пустой датакласс для объекта. 
        # Он будет использован для сравнения с 1 сканированным результатом.
        # Необходим для отсеивания пустых тиражей.
        self.data = self.get_default_dataclass()

        # На основе номера заказа и имени тиража высчитываем хэш сумму. 
        # Она будет использоваться для записи во множество.
        self._hash = hash(order_path.rsplit('/', 1)[-1] + name)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ProxyObserver):
            return self._hash == __value._hash
        
        return self._hash == hash(__value)
    
    def __hash__(self) -> int:
        return self._hash
    
    def get_default_dataclass(self) -> DATA:     #type: ignore
        """
        Возвращает Объект со значениями по умолчанию. 
        Этот объект в дальнейшем используется для сравнения и выявления пустых тиражей
        """
        raise Exception(f'Ф-я <__get_default_dataclass> должна быть переопределна в классе {self.__class__.__name__}')

    def update_info(self):
        """Обновление информации в датаклассе."""
        # Каждые 20 минут (Цикл трекера - 150 секунд, 8 итераций -> 20 минут)
        # Устанавливаем метки на начальное положение для инициализации повтороного сканирования.
        if self._count == 8:
            self._count = 0
            self.trackable = True
        
        # Если объект не нуждается в обновлении, увеличиваем счетчик на 1 и пропускаем скан
        if not self.trackable:
            self._count += 1
            return

        # Получаем объект и сравниваем его с предыдущим сканированием
        res = self.get_info()
        if self.data == res:
            self.trackable = False  # Если объекты равны, переводим флаг в False
        else:
            self.data = res         # Иначе обновляем data

    def get_info(self) -> DATA:
        """Возвращает полученную информацию"""
        raise Exception(f'В классе <{self.__class__.__name__}> должен быть переопределен метод <get_info>')
