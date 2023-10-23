from ..app_manager import AppManager
from ..grabbers import EditionGrabber
from math import ceil as m_ceil


class Handler:
    __slots__ = 'proxy', 'handler_option', 'total', 'cache', '__name__', '__doc__'
    storage = AppManager.storage

    def __init__(self):
        self.proxy = None
        self.handler_option = None
        self.total = 0
        self.cache = {}
        self.__name__ = self.__class__.__name__
        self.__doc__ = self.__class__.__doc__

    @staticmethod
    def mm_to_pixel(mm: int) -> int:
        """Возвращает значение в пикселях при разрешении в 300 dpi"""
        return m_ceil(mm * 11.808)

    @staticmethod
    def pixel_to_mm(pixel: int) -> int:
        return m_ceil(pixel / 11.808)

    def __call__(self, obj, **kwargs):
        self.proxy = obj
        self.handler_option = kwargs
        self.storage.pf.header.set(self.get_processing_frame_header())
        self.storage.pf.status.set('Подготовка изображений')
        self.storage.pf.pb['maximum'] = 1
        self.proxy.files = tuple(self.get_images_to_proxy_obj())
        self.preparing_images_for_processing()
        self.storage.pf.pb['value'] += 1
        self.total = self.storage.pf.pb['maximum'] = self.get_total_sum_of_images()
        self.storage.pf.pb['value'] = 0
        self.run()
        self.finish()

    def get_processing_frame_header(self) -> str:
        """Возвращает строку, которая будет использована как заголовок в processing_frame"""
        return f'Обработка заказа {self.proxy.name}'

    def get_images_to_proxy_obj(self) -> callable:
        """Обновляет атрибут files у объекта self.proxy кортежем из объектов EditionGrabber или None"""
        path = f'{self.storage.stg.z_disc}/{self.proxy.creation_date}/{self.proxy.name}'
        for i, edition in enumerate(self.proxy.content):
            if self.proxy.products[i]:
                yield EditionGrabber(f'{path}/{edition.name}')
            else:
                yield None

    def preparing_images_for_processing(self):
        """Абстрактная ф-я. Подготовка изображений до их непосредственной обработки.
        Планируется, что она будет использоваться для наделения кэша объектами изображений из Constant"""
        pass

    def get_total_sum_of_images(self) -> int:
        """В дочернем классе должна возвращать сумму изображений"""
        raise Exception('Функция get_total_sum_of_images должна быть переопределена в дочернем классе')

    def run(self):
        """Запускает основную логику обработчика файлов"""
        raise Exception('Функция run должна быть переопределена в дочернем классе')

    def finish(self):
        """По завершении, очищаем обработчик"""
        self.proxy = None
        self.handler_option = None
        self.total = 0
        self.cache.clear()
