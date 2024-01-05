from .data_base import DataBase
from ..app_manager import AppManager
from typing import NamedTuple
from ..trackers.order_tracker_proxies import *


class Photo(NamedTuple):
    """Инофрмация о фотопечати."""
    name: str                               # Имя тиража
    value: int                              # Счетчик отпечатков


class Edition(NamedTuple):
    """Информация о тираже."""
    name: str                               # Имя тиража
    covers: int                             # Счетчик обложек
    pages: int | None                       # Счетчик разворотов
    ccount: str | None                      # Комплексный счетчик обложек/разворотов
    comp: str | None                        # Тип совмещения тиража (актуально для книг)


class Order(NamedTuple):
    """Информация о заказе."""
    name: str                               # Имя заказа, он же его номер
    creation_date: str                      # Дата загрузки заказа на сервер
    customer_name: str                      # Имя заказчика
    customer_address: str                   # Адрес заказчика
    price: float                            # Общая сумма заказа
    photo: tuple[Photo, ...] | None         # Кортеж объектов фотопечати заказа
    content: tuple[Edition, ...] | None     # Кортеж объектов тиражей заказа


class Log(DataBase):
    """Класс предостовляющий доступ к чтению и записи лога заказов"""
    __slots__ = ()

    data_base = 'log.db'

    def __init__(self) -> None:
        super().__init__()
        AppManager.ot._border_name = self.get_newest_order_name()

    @DataBase.safe_connect
    def update_records(self, proxies: set[EditionProxy | PhotoProxy]) -> None:
        """Сборная ф-я для обновления библиотеки"""
        for proxy in sorted(proxies, key=lambda x: (x._order_proxy.name, x.name)):
            # Записываем информацию по заказу в лог, если к нам пришел непустой тираж
            if proxy._updated and proxy._order_proxy._updated:
                proxy._order_proxy._updated = False
                self.__update_table(proxy._order_proxy)
            
            # Пропускаем не обновившиеся прокси объекты
            if not proxy._updated: continue

            # Обновляем лог
            if isinstance(proxy, PhotoProxy):
                self.__update_photos(proxy)
            else:
                self.__update_table(proxy)
        self.connect.commit()

    def __update_table(self, proxy: OrderInfoProxy | EditionProxy) -> None:
        """Обновление данных в основной таблице информации о заказе"""
        self.cursor.execute(proxy.check_request)
        if self.cursor.fetchone()[0]:
            self.cursor.execute(*proxy.update_request)
        else:
            self.cursor.execute(*proxy.insert_request)
    
    def __update_photos(self, proxy: PhotoProxy) -> None:
        """Для записи фотопечати пришлось использовать отдельный метод"""
        for name in proxy.__dict__:
            self.cursor.execute(proxy.check_request(name))
            if self.cursor.fetchone()[0]:
                self.cursor.execute(*proxy.update_request(name))
            else:
                self.cursor.execute(*proxy.insert_request(name))

    @DataBase.safe_connect
    def get(self, order_name: str) -> Order | None:
        """Получение объекта заказа из лога."""
        self.cursor.execute('SELECT * FROM Orders WHERE name=?', (order_name, ))
        res = self.cursor.fetchone()
        if res: 
            return Order(*res[1:], self.__get_photos(order_name), self.__get_editions(order_name))  #type: ignore
    
    def __get_photos(self, order_name: str) -> tuple[Photo, ...] | None:
        """Вспомогательная ф-я для получения информации о фотопечати в заказе"""
        self.cursor.execute('SELECT name, value FROM Photos WHERE order_name=?', (order_name, ))
        res = self.cursor.fetchall()
        if res: return tuple(Photo(*r) for r in res)

    def __get_editions(self, order_name: str) -> tuple[Edition, ...] | None:
        """Вспомогательная ф-я для получения информации о тиражах в заказе"""
        self.cursor.execute('SELECT name, covers, pages, ccount, comp FROM Editions WHERE order_name=?', (order_name, ))
        res = self.cursor.fetchall()
        if res: return tuple(Edition(*r) for r in res)

    @DataBase.safe_connect
    def get_newest_order_name(self) -> str:
        """Получение последнего сканированного номера заказа"""
        self.cursor.execute('SELECT MAX(name) FROM Orders')
        return self.cursor.fetchone()[0]
