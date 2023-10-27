from ..app_manager import AppManager
from ..grabbers import EditionGrabber


class Handler:
    __slots__ = '__name__', '__doc__', 'proxy', 'cache',
    storage = AppManager.storage

    def __init__(self):
        self.__name__ = self.__class__.__name__
        self.__doc__ = self.__class__.__doc__
        self.proxy = None
        self.cache = {}

    @staticmethod
    def mm_to_pixel(mm: int) -> int:
        """Возвращает значение в пикселях при разрешении в 300 dpi."""
        return mm * 11.811

    def __call__(self, obj, **kwargs):
        self.proxy = obj
        self.cache.update(kwargs)
        self.storage.pf.header.set(self.get_processing_frame_header())
        self.storage.pf.status.set('Подготовка изображений')
        self.storage.pf.pb['maximum'] = 1
        self.get_images_to_proxy_obj()
        self.preparing_images_for_processing()
        self.storage.pf.pb['value'] += 1
        self.storage.pf.pb['maximum'] = self.get_total_sum_of_images()
        self.storage.pf.pb['value'] = 0
        self.run()
        self.finish()

    def get_processing_frame_header(self) -> str:
        """Возвращает строку, которая будет использована как заголовок в processing_frame"""
        return f'Обработка заказа {self.proxy.name}'

    def get_images_to_proxy_obj(self) -> callable:
        """Обновляет атрибуты content, products, files у proxy объекта. Убирает лишние тиражи"""
        path = f'{self.storage.stg.z_disc}/{self.proxy.creation_date}/{self.proxy.name}'
        index = 0
        while index < len(self.proxy.content):
            if self.proxy.products[index] is None:
                del self.proxy.content[index]
                del self.proxy.products[index]
            else:
                self.proxy.files.append(EditionGrabber(f'{path}/{self.proxy.content[index].name}'))
                index += 1

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
        self.cache.clear()
