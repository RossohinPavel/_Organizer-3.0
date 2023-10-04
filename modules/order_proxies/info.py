import re
from collections import Counter
from modules.app_manager import AppManagerR


class OrderProxy(AppManagerR):
    __slots__ = 'order_proxies'

    def __new__(cls, order_name):
        order = cls.app_m.Log.get(order_name)
        if order is not None:
            res = super().__new__(cls)
            res.order = cls.app_m.Log.get_order_obj(order)
            return res

    def get_order_content_info(self):
        return {**self.__get_ed_info(), **self.__get_photo_info()}

    def __get_photo_info(self) -> dict:
        return {} if self.order.photo is None else {'PHOTO': self.order.photo.matrix_repr}

    def __get_ed_info(self) -> dict:
        dct = {}
        for edition in self.order.content:
            product_name = edition.name[::-1].split('-')[0][::-1]
            print(product_name)
            dct[edition.name] = (*self.__book_count(edition.matrix_repr),)
        return dct

    def __book_count(self, matrix_repr) -> tuple:
        """Основной метод для подсчета изображений в книгах. Возвращает значения в следующем порядке:
        Общее кол-во обложек, общее кол-во разворотов, комплексный счетчик"""
        covers = pages = 0
        comp = Counter()
        for ex, ex_tpl in matrix_repr.items():
            if ex == 'Constant':
                continue
            multiplier = 1
            if re.fullmatch(r'\d{3}-\d+_pcs', ex):
                multiplier = int(re.split('[-_]', ex)[1])
            ex_pages = len(ex_tpl) - 1
            covers += multiplier
            pages += multiplier * ex_pages
            comp[ex_pages] += multiplier
        comp = ' '.join(f'{v}/{k}' for k, v in sorted(comp.items(), key=lambda x: (x[1], x[0])))
        return covers, pages, comp, self.__get_combination(covers, pages, matrix_repr['Constant'])

    @staticmethod
    def __get_combination(cover_count, page_count, const_list):
        """Метод для определения типа совмещения обложек и блоков. Для одиночной книги возвращаем None"""
        if cover_count != 1:
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
