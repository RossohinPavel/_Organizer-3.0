import re
import os
from modules.order.order_dc import *

__all__ = ('OrderProxy', 'EditionProxy', 'PhotoProxy', 'OrderInfoProxy')


class OrderProxy:
    __slots__ = 'order', 'delete_flag'

    def __init__(self, path, creation_date, name):
        self.delete_flag = False
        self.order = Order(path, creation_date, name)

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
        obj = Edition(name)
        order_obj.content += (obj, )
        return obj

    def get_info(self):
        dct = {}
        path = self.path
        for name in os.listdir(path):
            if re.fullmatch(r'\d{3}(-\d+_pcs)?', name):
                dct[name] = tuple(x for x in os.listdir(f'{path}/{name}') if re.fullmatch(r'(cover|\d{3}_)_\d{3}(-\d+_pcs)?\.jpg', x))
            if name == 'Constant':
                dct[name] = tuple(x for x in os.listdir(f'{path}/{name}') if re.fullmatch(r'(cover|\d{3})_\d+_pcs\.jpg', x))
        dct.setdefault('Constant', tuple())
        return dct

    def check_info(self, res):
        return self.dc_obj.matrix_repr == res

    def set_info(self, res):
        self.dc_obj.matrix_repr = res


class PhotoProxy(ProxyObserver):
    paper_type = {'Глянцевая': 'Fuji Gl', 'Матовая': 'Fuji Mt'}

    def init_observer(self, order_obj, name):
        obj = PhotoEdition()
        order_obj.photo = obj
        return obj

    def get_info(self):
        dct = {}
        path = f'{self.path}/_ALL/Фотопечать'
        for paper in os.listdir(path):
            for form in os.listdir(f'{path}/{paper}'):
                paper_format, multiplier = form[5:].split('--')
                name = f'{self.paper_type.get(paper, "Fuji ???")} {paper_format}'
                dct[name] = dct.get(name, 0) + len(os.listdir(f'{path}/{paper}/{form}')) * int(multiplier)
        return dct

    def check_info(self, res):
        return self.dc_obj.matrix_repr == res

    def set_info(self, res):
        self.dc_obj.matrix_repr = res


class OrderInfoProxy(ProxyObserver):
    def init_observer(self, order_obj, name):
        obj = OrderInfo()
        order_obj.order_info = obj
        return obj

    def get_info(self):
        name, address, price = 'unknown', 'unknown', 0
        with open(self.path, 'r', encoding='utf-8') as file:
            string = file.read()
            f = re.findall(r'(Уважаемый \(ая\), .+</p>|Адрес\W+выдачи.+\W+.+|доставки\), руб\. : <strong>\d+)', string)
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
