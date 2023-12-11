from ._proxy import *
from ....file_iterators import photo_iterator


class Photo(dict):
    """Словарь для хранения информации о фотопечати"""
    __slots__ = ('order_name', )

    def __init__(self, order_name: str):
        # Имя заказа сохраняем как атрибут объекта
        self.order_name = order_name


class PhotoProxy(ProxyObserver):
    """Объект слежения за фотопечатью"""
    __slots__ = ()

    def get_default_dataclass(self) -> DATA:
        return Photo(self.info_proxy.order)
    
    def get_info(self) -> DATA:
        """Ф-я подсчета фотопечати в заказе."""
        # Создем новый объект
        data = Photo(self.info_proxy.order)

        # Итерируемся по фотопечати в заказе
        for paper, format, pages_it in photo_iterator(self._path):
            # Отсекаем слово Фото из имени
            format = format.split()[1]

            # Получаем строку формата и мультипликатор изображений
            format, multiplier = format.split('--')

            # Обновляем значения словаря
            multiplier = int(multiplier)
            data[f'{paper} {format}'] = sum(multiplier for _ in pages_it)

        return data
