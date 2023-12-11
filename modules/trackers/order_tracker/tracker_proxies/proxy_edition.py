from re import findall, fullmatch
from collections import Counter
from ._proxy import *
from ....file_iterators import edition_iterator


"""Именованный кортеж для хранения информации о тираже"""
Edition = namedtuple(
    typename='Edition',
    field_names=(
        'order_name',       # Имя заказа
        'name',             # Название тиража
        'covers',           # Общее количество обложек в заказе
        'pages',            # Общее количество разворотов в заказе.
        'ccount',           # Комплексный счетчик "Кол-во экз / кол-во разворотв в экз"
        'comp'              # Тип совмещения заказа
    ),
    # Значения по умолчанию для covers, pages, ccount, comp
    defaults=(0, None, None, None)
)


class EditionProxy(ProxyObserver):
    """Объект слежения за тиражами"""
    __slots__ = ()

    def get_default_dataclass(self) -> DATA:
        return Edition(self.info_proxy.order, self.name)

    def get_info(self) -> DATA:
        """Ф-я подсчета изображений в тиражах. Определяет тип совмещения"""
        cover_count = 0
        page_lst = []
        const = tuple()
        for catalog, images in edition_iterator(self._path, 'Exemplar', 'Constant'):
            if catalog != 'Constant':
                cover_exist = False
                page_count = 0
                for image in images:
                    if image.startswith('cover'):
                        cover_exist = True
                        continue
                    page_count += 1
                if cover_exist:
                    res = findall(r'\d{3}-(\d+)_pcs', catalog)
                    multiplier = int(res[0]) if res else 1
                    cover_count += multiplier
                    page_lst.extend([page_count] * multiplier)
            else:
                const = images
        page_count = sum(page_lst)
        complex_count = self.get_ccount(page_count, page_lst)
        combination = self.get_combination(cover_count, page_count, const)
        return Edition(self.info_proxy.order, self.name, cover_count, page_count, complex_count, combination)

    @staticmethod
    def get_ccount(page_count: int, ex_list: list) -> str | None:
        """Метод для формирования комплексного счетчика в формате <30/3 2/4>"""
        if not page_count: return

        return ' '.join(f'{v}/{k}' for k, v in sorted(Counter(ex_list).items(), key=lambda x: (x[1], x[0])))

    @staticmethod
    def get_combination(cover_count: int, page_count: int, const_list: Iterator | tuple) -> str | None:
        """
            Метод для определения типа совмещения обложек и блоков.
            Анализ на основе подсчета постоянных изображений.
        """

        # Возвращаем None, если это одна книжка в тираже или счетчик разворотов = 0.
        # Совмещать штучную продукцию нет смысла))
        if page_count == 0 or cover_count == 1: return

        # Вспомогательные переменные для подсчета
        cover_exist = False
        const_page_count = 0

        # Итерируемся по константам. Ищем файл Cover и считаем постоянные развороты.
        for name in const_list:
            if fullmatch(r'cover_\d+_pcs\.jpg', name):
                cover_exist = True
            if fullmatch(r'\d\d\d_\d+_pcs\.jpg', name):
                const_page_count += int(name.split('_')[1])
        
        # Возвращаем значения, соответствующие подсчету
        if cover_exist and const_page_count == page_count: return "Копии"
        if cover_exist: return 'О_О'
        if const_page_count == page_count: return 'В_О'
        return 'Индивидуально'
