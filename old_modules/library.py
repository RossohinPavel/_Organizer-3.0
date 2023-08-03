import sqlite3
from functools import lru_cache
import threading as th


class Library:
    """
    Класс для работы с базой данных библиотеки продуктов.
    """
    __instance = None
    __db = '../data/library.db'
    __timeout = 10

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @staticmethod
    def get_categories() -> tuple:
        """Возвращает кортеж из доступных категорий"""
        return 'Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Canvas', 'Subproduct'

    @classmethod
    def translator(cls, category: str, always_eng=False) -> str:
        """Используется для перевода русского названия продукта в английское и обратно"""
        rus = ('Фотокниги на Фотобумаге', 'Полиграфические фотокниги Layflat', 'Полиграфические альбомы, PUR, FlexBind',
               'Полиграфические фотожурналы', 'Фотопапки', 'Фотохолсты', 'Остальное')
        if category in rus:
            return cls.get_categories()[rus.index(category)]
        else:
            return category if always_eng else rus[cls.get_categories().index(category)]

    @classmethod
    def blank(cls, category: str) -> dict[str: tuple | int]:
        """Генерирует словарь с соответствующим category (продукту) атрибутами и их возможными значениями
        :param category: str: 'Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Canvas', 'Subproduct' или
        русский аналог
        :return: dict[str: tuple | int]
        """
        category = cls.translator(category, always_eng=True)
        attrs_funcs = (lambda b, c: b.update({'full_name': c}), cls.__segment, cls.__short_name, cls.__product_format,
                       cls.__book_option, cls.__lamination, cls.__cover_type, cls.__carton_length,
                       cls.__carton_height, cls.__cover_clapan, cls.__cover_joint, cls.__print_mat('cover'),
                       cls.__print_mat('page'), cls.__canals, )
        blank = {}
        for func in attrs_funcs:
            func(blank, category)
        return blank

    @staticmethod
    def __segment(blank: dict, category: str):
        """Функция для наделения бланка соответствующим категории кортежом сегментов"""
        segment = ()
        if category in ('Photobook', 'Layflat', 'Album', 'Canvas'):
            segment += ('Премиум',)
        if category in ('Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Subproduct'):
            segment += ('Тираж',)
        blank['segment'] = segment

    @staticmethod
    def __short_name(blank: dict, category: str):
        """Функция для наделения бланка соответствующим категории кортежом коротких имен"""
        dct = {'Photobook': ('КС', 'ЛЮКС', 'кКожа', 'КК', 'ПС'), 'Layflat': ('ППК', 'ПК'), 'Album': ('ФБ', 'ПА', 'ПУР'),
               'Journal': ('Журнал',), 'Photofolder': ('Дуо', 'Дуо гор', 'Трио'), 'Canvas': ('+холсты',),
               'Subproduct': ('+полигр фото', '+открытки')}
        blank['short_name'] = dct[category]

    @staticmethod
    def __product_format(blank: dict, category: str):
        """Функция для наделения бланка соответствующим категории кортежом форматов продукта"""
        bf = ('10x10', '15x15', '15x20в', '20x15г', '20x20', '20x30в', '30x20г', '25x25', '30x30', '40x30г', '30x40в')
        canvas = ('30x45 верт', '30x45 гориз', '40x40', '40x60 верт', '40x60 гориз', '45x45', '50x50', '50x75 верт',
                  '50x75 гориз', '60x60', '60x90 верт', '60x90 гориз', '80x80', '80x120 верт', '80x120 гориз')
        res = {'Photobook': bf, 'Layflat': bf[4:9], 'Album': bf[4:], 'Journal': bf[4:6], 'Photofolder': bf[5:7],
               'Canvas': canvas}.get(category)
        if res:
           blank['product_format'] = res

    @staticmethod
    def __book_option(blank: dict, category: str):
        """Функция для наделения бланка соответствующим категории кортежом опций сборки"""
        if category in ('Photobook', 'Layflat'):
            blank['book_option'] = ('б/у', 'с/у', 'с/у1.2')

    @staticmethod
    def __lamination(blank: dict, category: str):
        """Функция для наделения бланка соответствующим категории кортежом типов ламинации"""
        if category in ('Photobook', 'Layflat', 'Album', 'Photofolder'):
            blank['lamination'] = ('гля', 'мат')

    @staticmethod
    def __cover_type(blank: dict, category: str):
        """Функция для наделения бланка соответствующим категории кортежом типов обложек"""
        ct = ('Книга', 'Планшет', 'Люкс', 'Кожаный корешок', 'Кожаная обложка')
        res = {'Photobook': ct, 'Layflat': ct[:2], 'Album': ct[:1]}.get(category)
        if res:
            blank['cover_type'] = res

    @staticmethod
    def __carton_length(blank: dict, category: str):
        """Функция для наделения бланка соответствующим категории атрибутом длинны картонки обложки"""
        if category in ('Photobook', 'Layflat', 'Album', 'Photofolder'):
            blank['carton_length'] = 0

    @staticmethod
    def __carton_height(blank: dict, category: str):
        """Функция для наделения бланка соответствующим категории атрибутом высоты картонки обложки"""
        if category in ('Photobook', 'Layflat', 'Album', 'Photofolder'):
            blank['carton_height'] = 0

    @staticmethod
    def __cover_clapan(blank: dict, category: str):
        """Функция для наделения бланка соответствующим категории кортежем из значений длинны клапана обложки"""
        if category in ('Photobook', 'Layflat', 'Album'):
            blank['cover_clapan'] = (15, 20)

    @staticmethod
    def __cover_joint(blank: dict, category: str):
        """Функция для наделения бланка соответствующим категории кортежем из значений длинны шарнира обложки"""
        if category in ('Photobook', 'Layflat', 'Album'):
            blank['cover_joint'] = (10, 15, 18)

    @staticmethod
    def __print_mat(side: str = 'cover') -> callable:
        """Функция для наделения бланка соответствующим категории кортежем печатного материала"""
        cvr_photo = ('Fuji CA Matte 152x204', 'Fuji CA Matte 152x304', 'Fuji CA Matte 152x370', 'Fuji CA Matte 203x305',
                     'Fuji CA Matte 203x406', 'Fuji CA Matte 203x470', 'Fuji CA Matte 203x500', 'Fuji CA Matte 203x570',
                     'Fuji CA Matte 254x400', 'Fuji CA Matte 254x470', 'Fuji CA Matte 254x500', 'Fuji CA Matte 254x620',
                     'Fuji CA Matte 254x700', 'Fuji CA Matte 254x770', 'Fuji CA Matte 305x610', 'Fuji CA Matte 305x675')
        cvr_poly = ('Omela 500', 'Omela 700', 'Raflatac 500', 'Raflatac 700')
        pg_photo = ('Fuji CA Matte 152x304', 'Fuji CA Matte 152x406', 'Fuji CA Matte 203x305', 'Fuji CA Matte 203x400',
                    'Fuji CA Matte 203x600', 'Fuji CA Matte 254x512', 'Fuji CA Matte 300x102', 'Fuji CA Matte 305x402',
                    'Fuji CA Matte 305x610', 'Fuji CA Matte 305x810')
        pg_poly = ('Sappi SRA3', 'Sappi 320x620', 'UPM SRA4 170', 'UPM SRA4 150', 'UPM SRA4 250', 'UPM SRA3 170',
                   'UPM SRA3 250', 'Flex Bind 330x330', 'Flex Bind 320x450')

        def cover(blank: dict, category: str):
            """Замыкание для получение печатного материала обложки"""
            dct = {'Photobook': cvr_photo + cvr_poly, 'Layflat': cvr_poly, 'Album': cvr_poly, 'Journal': pg_poly,
                   'Photofolder': cvr_poly[:2], 'Canvas': ('CottonCanvas',), 'Subproduct': pg_poly}
            blank['cover_print_mat'] = dct[category]

        def page(blank: dict, category: str):
            """Замыкание для получение печатного материала разворотов"""
            dct = {'Photobook': pg_photo, 'Layflat': pg_poly[:-2], 'Album': pg_poly, 'Journal': pg_poly[:-2]}
            res = dct.get(category)
            if res:
                blank['page_print_mat'] = dct[category]

        if side == 'page':
            return page

        return cover

    @staticmethod
    def __canals(blank: dict, category: str):
        """Функция для наделения бланка для фотокниги кортежами каналов для обложек и разворотов"""
        if category == 'Photobook':
            blank['cover_canal'] = ('160', '161', '162', '163', '164', '165', '166', '204', '205', '214', '240', '242',
                                    '243', '245', '266', '36', 'ORAJET', 'POLI')
            blank['page_canal'] = ('201', '214', '203', '204', '205', '207', '275', '274', '276', '271')

    @staticmethod
    def __decoding(blank: dict, category: str):
        """Функция для наделения бланка для полиграфического альбома соответствующими атрибутами для раскодировки"""
        if category == 'Album':
            blank.update({'dc_break': 0, 'dc_overlap': 0, 'dc_top_indent': 0, 'dc_left_indent': 0})

    # @staticmethod
    # def __safe_connect(func):
    #     """Декоратор для безопасного подключения к БД"""
    #     def wrapper(instance, *args, **kwargs):
    #         with sqlite3.connect(Library.__db, timeout=Library.__timeout) as connect:
    #             cursor = connect.cursor()
    #             return func(instance, cursor, *args, **kwargs)
    #
    #     wrapper.__name__ = func.__name__
    #     wrapper.__doc__ = func.__doc__
    #     return wrapper
    #
    # @lru_cache
    # @__safe_connect
    # def get_product_values(self, cursor, category: str, full_name: str) -> dict:
    #     """
    #     Метод для получения данных из бд в виде словаря
    #     :param cursor: Объект курсора, который передается декоратором
    #     :param category: Категория продукта / название таблицы
    #     :param full_name: Имя продукта
    #     """
    #     if self._cache_clear:
    #         print('Очистка кэша')
    #         self.get_product_values.cache_clear()
    #     print('сработал метод')
    #     keys = tuple(self.blank(category))
    #     sql_req = ', '.join(f'\"{x}\"' for x in keys)
    #     cursor.execute(f'SELECT {sql_req} FROM {category} WHERE full_name=\'{full_name}\'')
    #     values = cursor.fetchone()
    #     return {keys[i]: values[i] for i in range(len(keys))}


# if __name__ == '__main__':
#     obj = Library()
#     test_func = lambda x: print(id(x))
#     t1 = th.Thread(target=test_func, args=(obj, ))
#     t2 = th.Thread(target=test_func, args=(obj, ))
#     t1.start()
#     t2.start()