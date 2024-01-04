# Импорты необходимые для работы самого Обработчика
from modules.app_manager import AppManager
from .._proxy import FileHandlerProxy
from .._grabbers import EditionGrabber

# Импорты необходимые для работы дочерних классов по обработке изображений
from math import ceil as m_ceil
from os import makedirs as os_makedirs
from PIL import Image, ImageDraw, ImageFont

# Импорты для типизации
from ...mytyping import Edition, Categories


class Handler:
    """Абстрактный класс предостовляющий реализующий основную логику обработчиков"""
    __slots__ = '__name__', 'order_name', 'option', 'source', 'destination', 'files'

    grabber_mode = tuple()  # Режим, в котором работает EditionGrabber. Свой для каждого обработчика

    def __init__(self) -> None:
        self.__name__ = self.__class__.__name__
        # Переменная для хранения имени заказа
        self.order_name: str
        
        # Маркер дополнительной опции обработки
        self.option: bool = False

        # Переменные пути
        self.source: str                        # Переменная для хранения пути, источника файлов
        self.destination: str                   # Переменная для хранения пути назначения
        
        # Список для хранения файловых объектов
        self.files: list[EditionGrabber | None] = []   

    @staticmethod
    def mm_to_pixel(mm: int | float) -> float:
        """Возвращает значение в пикселях при разрешении в 300 dpi."""
        return mm * 11.811

    def _update_files(self, content: tuple[Edition], products: tuple[Categories | None]) -> None:
        """
            Итерируется по тиражам и наполняет список self.files объектами EditionGrabber.
            Добавлет этот объект, если для тиража есть определившийся продукт, 
            в остальных случаях - добавляет None.
        """
        for i, edition in enumerate(content):
            file_obj = None
            if products[i]:
                file_obj = EditionGrabber(f'{self.source}/{edition.name}', self.grabber_mode)
            self.files.append(file_obj) 

    def get_total_sum_of_images(self) -> int:
        """В дочернем классе должна возвращать сумму изображений"""
        raise Exception('Функция get_total_sum_of_images должна быть переопределена в дочернем классе')

    def __call__(self, proxy: FileHandlerProxy, option: bool) -> None:
        # Общая конфигурация прокси объекта
        AppManager.pf.header.step(proxy.name)
        AppManager.pf.operation.step('Подготовка изображений')

        # Устанавливаем имя заказа
        self.order_name = proxy.name

        # Обновляем маркер дополнительной обработки
        self.option = option

        # Получаем ссылки на диск-источник и диск, с которого идет печать.
        tail = f'{proxy.creation_date}/{proxy.name}'
        self.source = f'{AppManager.stg.z_disc}/{tail}'
        self.destination =  f'{AppManager.stg.o_disc}/{tail}'

        # Обновляем Обработчик. Наполняем список files.
        self._update_files(proxy.content, proxy.products)

        # Конфигурация Процессинг фрейма
        AppManager.pf.operation.reset()
        AppManager.pf.operation.maximum = sum(1 for f in self.files if f)
        AppManager.pf.filebar.maximum(self.get_total_sum_of_images())

        # Старт основной логики обработки
        for i, file_grabber in enumerate(self.files):
            # Запускаем функцию обрабочика, если есть файловый объект тиража 
            # (соответственно и продукт для этого тиража).
            if file_grabber:
                content = proxy.content[i]
                AppManager.pf.operation.step(content.name)
                self.handler_run(content, proxy.products[i], file_grabber)

        # Сброс значений
        self._reset_to_default()

    def handler_run(self, edition: Edition, product: Categories, file_grabber: EditionGrabber):
        """Запускает основную логику обработчика файлов"""
        raise Exception('Функция handler_run должна быть переопределена в дочернем классе')
    
    def _reset_to_default(self) -> None:
        """Сброс значений на начальные"""
        self.source = self.destination = self.order_name = ''
        self.files.clear()
