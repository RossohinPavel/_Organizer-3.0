from re import findall
from collections import namedtuple


_oi = namedtuple(
    typename='OrderInfo',
    field_names=(
        'order_name',               # Номер заказа
        'creation_date',            # Дата создания заказа
        'customer_name',            # Имя заказчика
        'customer_address',         # Адрес заказчика
        'price',                    # Общая стоимость заказа
    ),
    # Значения по умолчанию для customer_name, customer_address и price
    defaults=('_unknown_', '_unknown_', 0.0)
)


class OrderInfo(_oi):
    __slots__ = ()
    pass


class OrderInfoProxy:
    """
        Объект слежения за файлом completed.htm содержащий в себе информацию о заказе.
        Повторяет некоторые эдементы ProxyObserver для получения общего интерфейса.
    """
    __slots__ = 'trackable', 'in_log', 'order_path', 'day', 'order', 'data'

    _patterns = {
        'customer_name': r'Уважаемый \(ая\), (.+) !</p>',
        'customer_address': r'выдачи.+\n?.+\n?.+<strong>(.+)</strong>',
        'price': r'руб\..+<strong>(\d+\.?\d*)'
    }

    def __init__(self, order_path: str, day: str, order: str) -> None:
        # Атрибуты управления объектом
        self.trackable = True       # Флаг отслеживание изменений
        self.in_log = False         # Флаг присутствия в логе

        # Информационные атрибуты
        self.order_path = order_path
        self.day = day
        self.order = order

        # Датакласс
        self.data = OrderInfo(order, day)

    def update_info(self):
        """Обновление информации в датаклассе. Логика будет отличаться от тиражных прокси."""
        # self._count будет служить меткой от повторного записи в библиотеку
        if self.trackable:
            # Пытаемся обновить информацию.
            try:
                self.data = self.get_info()
                # Повторно сканировать существующий completed нет необходимости.
                self.trackable = False
                # А флаг присутствиия в логе меняем на False, так как инфомрация обновилась
                self.in_log = False
            except:
                # В случае ошибки (не найден файл completed продолжаем искать его раз за разом)
                # Для большинства заказов он будет найден, остальные остануться со значением по умолчанию
                pass

    def get_info(self):
        """Парсим completed.htm с целью нахождения нужной нам информации"""
        with open(f'{self.order_path}/completed.htm', encoding='utf-8') as file:
            # создаем и возвращаем новый объект
            return eval(f'OrderInfo(self.order, self.day, {', '.join(self._arg_generator(file.read()))})')

    def _arg_generator(self, string):
        """Генератор именованных аргументов для создания кортежа OrderInfo"""
        for arg, pattern in self._patterns.items():
            # По паттерну находим нужную строку
            res = findall(pattern, string)
            if res:
                if arg == 'price': res[0] = float(res[0])
                yield f'{arg}={repr(res[0])}'
