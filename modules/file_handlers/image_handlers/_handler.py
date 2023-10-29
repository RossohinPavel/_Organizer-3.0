from os import makedirs as os_makedirs
from PIL import Image, ImageDraw, ImageFont
from modules.app_manager import AppManager
from modules.file_handlers.grabbers import EditionGrabber


class Handler:
    """Абстрактный класс предостовляющий реализующий основную логику обработчиков"""
    __slots__ = '__name__', 'proxy', 'source', 'destination', 'middle_path'
    storage = AppManager.storage
    grabber_mode = tuple()

    def __init__(self):
        self.__name__ = self.__class__.__name__
        self.proxy = None
        self.source = None
        self.destination = None
        self.middle_path = None

    @staticmethod
    def mm_to_pixel(mm: int) -> float:
        """Возвращает значение в пикселях при разрешении в 300 dpi."""
        return mm * 11.811

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
                self.proxy.files.append(EditionGrabber(f'{path}/{self.proxy.content[index].name}', self.grabber_mode))
                index += 1

    def get_total_sum_of_images(self) -> int:
        """В дочернем классе должна возвращать сумму изображений"""
        raise Exception('Функция get_total_sum_of_images должна быть переопределена в дочернем классе')

    def __call__(self, obj, **kwargs):
        # Подготовка обрабочика к работе. Получение основных настроек.
        self.proxy = obj
        self.storage.pf.header.set(self.get_processing_frame_header())
        self.storage.pf.status.set('Подготовка изображений')
        self.storage.pf.pb['maximum'] = 1
        # Получаем ссылки на диск-источник и диск, с которого идет печать.
        self.source, self.destination = self.storage.stg.z_disc, self.storage.stg.o_disc
        # Формируем промежуточный путь, который на этих дисках одинаковый.
        self.middle_path = f'{self.proxy.creation_date}/{self.proxy.name}'
        # Дополняем kwargs именем заказа
        kwargs['order'] = self.proxy.name
        # Обновляем прокси объект. Наполняем его объектами для итерации по файлам
        self.get_images_to_proxy_obj()
        self.storage.pf.pb['value'] += 1
        # Старт основной логики обработки
        self.storage.pf.pb['maximum'] = self.get_total_sum_of_images()
        self.storage.pf.pb['value'] = 0
        # Итерируемся по файловым объектам
        for index, file_grabber in enumerate(self.proxy.files):
            # Получаем имя тиража и тип его совмещения. Эта информация будет использована в ходе дальнейшей обработки
            kwargs['edt_name'] = self.proxy.content[index].name
            kwargs['comp'] = self.proxy.content[index].comp
            self.handler_run(self.proxy.products[index], file_grabber, kwargs)
        self.proxy = self.source = self.destination = self.middle_path = None

    def handler_run(self, product, file_grabber, kwargs):
        """Запускает основную логику обработчика файлов"""
        raise Exception('Функция run должна быть переопределена в дочернем классе')
