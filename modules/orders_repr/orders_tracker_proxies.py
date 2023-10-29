import re
import os
from collections import Counter

from .base_dataclasses import *
from modules.file_handlers import EditionGrabberIterator


__all__ = ('Order', 'EditionProxy', 'PhotoProxy', 'OrderInfoProxy')


class ProxyObserver:
    __slots__ = 'update_flag', '_counter', 'name', 'path', 'dc_obj'

    def __init__(self, order_obj, path, name):
        self.update_flag = True
        self._counter = 0
        self.name = name
        self.path = f'{path}/{name}'
        self.dc_obj = self.init_observer(order_obj, name)

    @staticmethod
    def init_observer(order_obj, name):
        """Инициализирует датакласс dc, прикрепляет его к order_obj и возвращает его"""
        return order_obj

    def update_info(self):
        """Обновление информации в датаклассе."""
        if self._counter == 8:
            self._counter = 0
            self.update_flag = True
        if not self.update_flag:
            self._counter += 1
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

    def __eq__(self, other) -> bool:
        return self.name == other

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} <{self.name}>'


class EditionProxy(ProxyObserver):
    @staticmethod
    def init_observer(order_obj, name):
        obj = Edition(order_obj.name, name)
        order_obj.content += (obj, )
        return obj

    def get_info(self):
        """Ф-я подсчета изображений в тиражах и определяет тип совмещения"""
        cover_count = 0
        page_lst = []
        const = tuple()
        for catalog, images in EditionGrabberIterator(self.path, 'Exemplar', 'Constant'):
            if catalog != 'Constant':
                cover_exist = False
                page_count = 0
                for image in images:
                    if image.startswith('cover'):
                        cover_exist = True
                        continue
                    page_count += 1
                if cover_exist:
                    res = re.findall(r'\d{3}-(\d+)_pcs', catalog)
                    multiplier = int(res[0]) if res else 1
                    cover_count += multiplier
                    page_lst.extend([page_count] * multiplier)
            else:
                const = images
        page_count = sum(page_lst)
        complex_count = self.get_ccount(page_count, page_lst)
        combination = self.get_combination(cover_count, page_count, const)
        return cover_count, page_count, complex_count, combination

    @staticmethod
    def get_ccount(page_count, ex_list) -> str | None:
        """Метод для формирования комплексного счетчика"""
        if not page_count:
            return
        return ' '.join(f'{v}/{k}' for k, v in sorted(Counter(ex_list).items(), key=lambda x: (x[1], x[0])))

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
                res = len(os.listdir(f'{path}/{paper}/{form}')) * int(multiplier)
                if res == 0:
                    continue
                obj = None
                for dc_obj in lst:
                    if dc_obj.name == name:
                        obj = dc_obj
                        break
                if obj is None:
                    obj = Photo(self.dc_obj.name, name)
                    lst.append(obj)
                obj.count += res
        return tuple(lst)

    def check_info(self, res) -> bool:
        return self.dc_obj.photo == res

    def set_info(self, res):
        self.dc_obj.photo = res


class OrderInfoProxy(ProxyObserver):

    def get_info(self):
        """Парсим completed.htm с целью нахождения нужной нам информации"""
        name, address, price = self.dc_obj.customer_name, self.dc_obj.customer_address, self.dc_obj.price
        with open(self.path, 'r', encoding='utf-8') as file:
            string = file.read()
            p_name = re.findall(r'Уважаемый \(ая\), (.+) !</p>', string)
            p_address = re.findall(r'выдачи.+\n?.+\n?.+<strong>(.+)</strong>', string)
            p_price = re.findall(r'руб\..+<strong>(\d+\.?\d*)', string)
            if p_name:
                name = p_name[0]
            if p_address:
                address = p_address[0]
            if p_price:
                price = p_price[0]
        return name, address, price

    def check_info(self, res) -> bool:
        return (self.dc_obj.customer_name, self.dc_obj.customer_address, self.dc_obj.price) == res

    def set_info(self, res):
        self.dc_obj.customer_name = res[0]
        self.dc_obj.customer_address = res[1]
        self.dc_obj.price = res[2]
