import re
import os
from collections import Counter
from modules.logs_dataclasses import *

__all__ = ('OrderProxy', 'EditionProxy', 'PhotoProxy', 'OrderInfoProxy')


class OrderProxy:
    """Прокси класс для обновления информации в датаклассе объекта заказа"""
    __slots__ = 'delete_flag', 'path', 'order'

    def __init__(self, path, creation_date, name):
        self.delete_flag = False
        self.path = f'{path}/{creation_date}/{name}'
        self.order = Order(name, creation_date)

    def __repr__(self):
        return f'Proxy <Order={self.order.name}>'

    def __hash__(self):
        return hash(self.order.name)

    def __eq__(self, other):
        res = self.order.name == other
        if res:
            self.delete_flag = False
        return res


class ProxyObserver:
    __slots__ = 'update_flag', 'name', 'path', 'dc_obj'

    def __init__(self, order_obj, path, name):
        self.update_flag = True
        self.name = name
        self.path = f'{path}/{name}'
        self.dc_obj = self.init_observer(order_obj, name)

    def init_observer(self, order_obj, name):
        """Инициализирует датакласс dc, прикрепляет его к order_obj и возвращает его"""
        raise Exception('Ф-я init_observer должна быть переопределена в дочернем классе с сохранением структуры')

    def update_info(self):
        """Обновление информации в датаклассе."""
        if not self.update_flag:
            return
        res = self.get_info()
        if self.check_info(res):
            self.update_flag = False
        else:
            self.set_info(res)

    def get_info(self):
        """Возвращает полученную информацию"""
        raise Exception(f'ф-я get_info должна быть переопределена {self.__class__.__name__}')

    def check_info(self, res):
        """Проверка информации res на совпадение"""
        raise Exception(f'ф-я check_info должна быть переопределена {self.__class__.__name__}')

    def set_info(self, res):
        """Установка информации соответствующему атрибуту"""
        raise Exception(f'ф-я set_info должна быть переопределена в {self.__class__.__name__}')

    def __eq__(self, other):
        return self.name == other

    def __repr__(self):
        return f'{self.__class__.__name__} <{self.name}>'


class EditionProxy(ProxyObserver):
    def init_observer(self, order_obj, name):
        obj = Edition(order_obj.name, name)
        order_obj.content += (obj, )
        return obj

    def get_info(self):
        """Ф-я подсчета изображений в тиражах и определяет тип совмещения"""
        ex = []
        const = tuple()
        for catalog in os.listdir(self.path):
            catalog_path = f'{self.path}/{catalog}'
            if re.fullmatch(r'\d{3}', catalog):
                ex.append(sum(1 for x in os.listdir(catalog_path) if re.fullmatch(r'\d{3}__\d{3}\.jpg', x)))
                continue
            if re.fullmatch(r'\d{3}-\d+_pcs', catalog):
                multiplier = int(re.split('[-_]', catalog)[1])
                pic_length = sum(1 for x in os.listdir(catalog_path) if re.fullmatch(r'\d{3}__\d{3}-\d+_pcs\.jpg', x))
                ex.extend(pic_length for _ in range(multiplier))
            if catalog == 'Constant':
                const = iter(x for x in os.listdir(catalog_path) if re.fullmatch(r'(cover|\d{3})_\d+_pcs\.jpg', x))
                continue
        cover_count = len(ex)
        page_count = sum(ex)
        return cover_count, page_count, self.get_ccount(ex), self.get_combination(cover_count, page_count, const)

    @staticmethod
    def get_ccount(ex_list) -> str:
        """Метод для формирования комплексного счетчика"""
        res = ' '.join(f'{v}/{k}' for k, v in sorted(Counter(ex_list).items(), key=lambda x: (x[1], x[0])))
        return res if res else None

    @staticmethod
    def get_combination(cover_count, page_count, const_list):
        """Метод для определения типа совмещения обложек и блоков. Для одиночной книги возвращаем None"""
        if page_count == 0 or cover_count == 1:
            return
        cover_exist = False
        const_page_count = 0
        for name in const_list:
            if re.fullmatch(r'cover_\d+_pcs\.jpg', name):
                cover_exist = True
            if re.fullmatch(r'\d\d\d_\d+_pcs\.jpg', name):
                const_page_count += int(name.split('_')[1])
        if cover_exist and const_page_count == page_count:
            return "Копии"
        if cover_exist:
            return 'О_О'
        if const_page_count == page_count:
            return 'В_О'
        return 'Индивидуально'

    def check_info(self, res):
        return (self.dc_obj.covers, self.dc_obj.pages, self.dc_obj.ccount, self.dc_obj.comp) == res

    def set_info(self, res):
        self.dc_obj.covers, self.dc_obj.pages, self.dc_obj.ccount, self.dc_obj.comp = res


class PhotoProxy(ProxyObserver):
    paper_type = {'Глянцевая': 'Fuji Gl', 'Матовая': 'Fuji Mt'}

    def init_observer(self, order_obj, name):
        return order_obj

    def get_info(self):
        """Ф-я подсчета фотопечати в заказе."""
        path = f'{self.path}/_ALL/Фотопечать'
        if not os.path.exists(path):
            return tuple()
        lst = []
        for paper in os.listdir(path):
            for form in os.listdir(f'{path}/{paper}'):
                paper_format, multiplier = form[5:].split('--')
                name = f'{self.paper_type.get(paper, "Fuji ???")} {paper_format}'
                obj = None
                for dc_obj in lst:
                    if dc_obj.name == name:
                        obj = dc_obj
                        break
                if obj is None:
                    obj = Photo(self.dc_obj.name, name)
                    lst.append(obj)
                obj.count += len(os.listdir(f'{path}/{paper}/{form}')) * int(multiplier)
        return tuple(lst)

    def check_info(self, res):
        return self.dc_obj.photo == res

    def set_info(self, res):
        self.dc_obj.photo = res


class OrderInfoProxy(ProxyObserver):
    def init_observer(self, order_obj, name):
        return order_obj

    def get_info(self):
        """Парсим completed.htm с целью нахождения нужной нам информации"""
        name, address, price = self.dc_obj.customer_name, self.dc_obj.customer_address, self.dc_obj.price
        with open(self.path, 'r', encoding='utf-8') as file:
            f = re.findall(r'(Уважаемый \(ая\), .+</p>|Адрес\W+выдачи.+\W+.+|доставки\), руб\. : <strong>\d+)', file.read())
            if f[0]:
                name = f[0][16:-6]
            if f[1]:
                res = re.split(r'</?strong>', f[1])
                if len(res) > 2 and res[1]:
                    address = res[1]
            if f[2]:
                price = int(re.split(r'<strong>', f[2])[-1])
        return name, address, price

    def check_info(self, res):
        return (self.dc_obj.customer_name, self.dc_obj.customer_address, self.dc_obj.price) == res

    def set_info(self, res):
        self.dc_obj.customer_name = res[0]
        self.dc_obj.customer_address = res[1]
        self.dc_obj.price = res[2]
