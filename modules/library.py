__all__ = ('Library', )
import sqlite3


class ProductGenerator:
    """Генерирует бланк (на основе dict) соответствующий той или иной категории продукта, которая была указана при
    инициализации.
    Можно указать следующие категории или их русские аналоги:
    'Photobook' - 'Фотокниги на Фотобумаге'
    'Layflat' - 'Полиграфические фотокниги Layflat'
    'Album' - 'Полиграфические альбомы, PUR, FlexBind',
    'Journal' - 'Полиграфические фотожурналы'
    'Photofolder' - 'Фотопапки'
    'Canvas' - 'Фотохолсты'
    'Subproduct' - 'Остальное'
    default_values=False отвечает за заполнение значениями по умолчанию (для Библиотеки)
    """

    def __new__(cls, category: str, default_values: bool = False):
        class_name = cls.translator(category, always_eng=True)
        if class_name is None:
            raise ValueError(f'Невозможно создать бланк для {category}')
        return eval(f'{class_name}({default_values})')

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


class Product(dict):
    """Класс описывающий продукт"""

    def __init__(self, default_values: bool = False):
        super().__init__()
        self.__set_full_name(default_values)
        self.__set_segment(default_values)
        self.__set_short_name(default_values)
        self.__set_product_format(default_values)
        self.__set_book_option(default_values)
        self.__set_lamination(default_values)
        self.__set_cover_type(default_values)
        self.__set_carton_size(default_values)
        self.__set_carton_clapan_and_joint(default_values)
        self.__set_print_mat(default_values)
        self.__set_photobook_canal(default_values)
        self.__set_decoding_attrs(default_values)

    def __str__(self) -> str:
        class_name = self.__class__.__name__ + '{'
        return class_name + f'\n{" " * len(class_name)}'.join(f'{k}: {v}' for k, v in self.items()) + '}'

    def __set_full_name(self, default_values):
        """Установка полного имени продукта"""
        full_name = None
        if default_values:
            full_name = ''
        self['full_name'] = full_name

    def __set_segment(self, default_values):
        """Функция для наделения бланка соответствующим категории кортежом сегментов"""
        segment = None
        if default_values:
            segment = ()
            if self.__class__.__name__ in ('Photobook', 'Layflat', 'Album', 'Canvas'):
                segment += ('Премиум',)
            if self.__class__.__name__ in ('Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Subproduct'):
                segment += ('Тираж',)
        self['segment'] = segment

    def __set_short_name(self, default_values):
        """Функция для наделения бланка соответствующим категории кортежом коротких имен"""
        short_name = None
        if default_values:
            values = {'Photobook': ('КС', 'ЛЮКС', 'кКожа', 'КК', 'ПС'), 'Layflat': ('ППК', 'ПК'),
                      'Album': ('ФБ', 'ПА', 'ПУР'), 'Journal': ('Журнал',), 'Photofolder': ('Дуо', 'Дуо гор', 'Трио'),
                      'Canvas': ('+холсты',), 'Subproduct': ('+полигр фото', '+открытки')}
            short_name = values[self.__class__.__name__]
        self['short_name'] = short_name

    def __set_product_format(self, default_values):
        """Функция для наделения бланка соответствующим категории кортежом форматов продукта"""
        if self.__class__.__name__ == 'Subproduct':
            return
        product_format = None
        if default_values:
            bf = (
                '10x10', '15x15', '15x20в', '20x15г', '20x20', '20x30в', '30x20г', '25x25', '30x30', '40x30г', '30x40в')
            canvas = ('30x45 верт', '30x45 гориз', '40x40', '40x60 верт', '40x60 гориз', '45x45', '50x50', '50x75 верт',
                      '50x75 гориз', '60x60', '60x90 верт', '60x90 гориз', '80x80', '80x120 верт', '80x120 гориз')
            res = {'Photobook': bf[:-1], 'Layflat': bf[4:9], 'Album': bf[4:], 'Journal': bf[4:6],
                   'Photofolder': bf[5:7], 'Canvas': canvas}
            product_format = res[self.__class__.__name__]
        self['product_format'] = product_format

    def __set_book_option(self, default_values):
        """Функция для наделения бланка соответствующим категории кортежом опций сборки"""
        if self.__class__.__name__ not in ('Photobook', 'Layflat'):
            return
        book_option = None
        if default_values:
            book_option = ('б/у', 'с/у', 'с/у1.2')
        self['book_option'] = book_option

    def __set_lamination(self, default_values):
        """Функция для наделения бланка соответствующим категории кортежом типов ламинации"""
        if self.__class__.__name__ not in ('Photobook', 'Layflat', 'Album', 'Photofolder'):
            return
        lamination = None
        if default_values:
            lamination = ('гля', 'мат')
        self['lamination'] = lamination

    def __set_cover_type(self, default_values):
        """Функция для наделения бланка соответствующим категории кортежом типов обложек"""
        if self.__class__.__name__ not in ('Photobook', 'Layflat', 'Album'):
            return
        cover_type = None
        if default_values:
            ct = ('Книга', 'Планшет', 'Люкс', 'Кожаный корешок', 'Кожаная обложка')
            cover_type = {'Photobook': ct, 'Layflat': ct[:2], 'Album': ct[:1]}[self.__class__.__name__]
        self['cover_type'] = cover_type

    def __set_carton_size(self, default_values):
        """Функция для наделения бланка соответствующим категории атрибутом длинны и высоты картонки обложки"""
        if self.__class__.__name__ not in ('Photobook', 'Layflat', 'Album', 'Photofolder'):
            return
        carton_length = carton_height = None
        if default_values:
            carton_length = carton_height = 0
        self['carton_length'] = carton_length
        self['carton_height'] = carton_height

    def __set_carton_clapan_and_joint(self, default_values):
        """Функция для наделения бланка соответствующим категории кортежем из значений длинны клапана обложки
        и кортежем значений ширины шарнира обложки"""
        if self.__class__.__name__ not in ('Photobook', 'Layflat', 'Album'):
            return
        cover_clapan = cover_joint = None
        if default_values:
            cover_clapan = (15, 20)
            cover_joint = (10, 15, 18)
        self['cover_clapan'] = cover_clapan
        self['cover_joint'] = cover_joint

    def __set_print_mat(self, default_values):
        """Функция для наделения бланка соответствующим категории кортежем печатного материала"""
        cover_print_mat = page_print_mat = None
        if default_values:
            cvr_photo = ('Fuji CA Matte 152x204', 'Fuji CA Matte 152x304', 'Fuji CA Matte 152x370',
                         'Fuji CA Matte 203x305', 'Fuji CA Matte 203x406', 'Fuji CA Matte 203x470',
                         'Fuji CA Matte 203x500', 'Fuji CA Matte 203x570', 'Fuji CA Matte 254x400',
                         'Fuji CA Matte 254x470', 'Fuji CA Matte 254x500', 'Fuji CA Matte 254x620',
                         'Fuji CA Matte 254x700', 'Fuji CA Matte 254x770', 'Fuji CA Matte 305x610',
                         'Fuji CA Matte 305x675')
            cvr_poly = ('Omela 500', 'Omela 700', 'Raflatac 500', 'Raflatac 700')
            pg_photo = ('Fuji CA Matte 152x304', 'Fuji CA Matte 152x406', 'Fuji CA Matte 203x305',
                        'Fuji CA Matte 203x400', 'Fuji CA Matte 203x600', 'Fuji CA Matte 254x512',
                        'Fuji CA Matte 300x102', 'Fuji CA Matte 305x402', 'Fuji CA Matte 305x610',
                        'Fuji CA Matte 305x810')
            pg_poly = ('Sappi SRA3', 'Sappi 320x620', 'UPM SRA4 170', 'UPM SRA4 150', 'UPM SRA4 250', 'UPM SRA3 170',
                       'UPM SRA3 250', 'Flex Bind 330x330', 'Flex Bind 320x450')
            cover_print_mat = {'Photobook': cvr_photo + cvr_poly, 'Layflat': cvr_poly, 'Album': cvr_poly,
                               'Journal': pg_poly, 'Photofolder': cvr_poly[:2], 'Canvas': ('CottonCanvas',),
                               'Subproduct': pg_poly}[self.__class__.__name__]
            page_print_mat = {'Photobook': pg_photo, 'Layflat': pg_poly[:-2], 'Album': pg_poly,
                              'Journal': pg_poly[:-2]}.get(self.__class__.__name__)

        self['cover_print_mat'] = cover_print_mat
        if self.__class__.__name__ in ('Photobook', 'Layflat', 'Album', 'Journal'):
            self['page_print_mat'] = page_print_mat

    def __set_photobook_canal(self, default_values):
        """Функция для наделения бланка соответствующим категории кортежем каналов печати частей фотокниг"""
        if self.__class__.__name__ != 'Photobook':
            return
        cover_canal = page_canal = None
        if default_values:
            cover_canal = ('160', '161', '162', '163', '164', '165', '166', '204', '205', '214', '240', '242', '243',
                           '245', '266', '36', 'ORAJET', 'POLI')
            page_canal = ('201', '214', '203', '204', '205', '207', '275', '274', '276', '271')
        self['cover_canal'] = cover_canal
        self['page_canal'] = page_canal

    def __set_decoding_attrs(self, default_values):
        """Функция для наделения бланка соответствующим категории атрибутами раскодировки альбомов"""
        if self.__class__.__name__ != 'Album':
            return
        dc_break = dc_overlap = dc_top_indent = dc_left_indent = None
        if default_values:
            dc_break = dc_overlap = dc_top_indent = dc_left_indent = 0
        self['dc_break'] = dc_break
        self['dc_overlap'] = dc_overlap
        self['dc_top_indent'] = dc_top_indent
        self['dc_left_indent'] = dc_left_indent


class Photobook(Product): pass
class Layflat(Product): pass
class Album(Product): pass
class Journal(Product): pass
class Photofolder(Product): pass
class Canvas(Product): pass
class Subproduct(Product): pass


class Library:
    """Класс для работы с базой данных библиотеки продуктов."""
    __instance = None
    __cache = {}
    __db = 'data/library.db'
    __timeout = 10
    product_gen = ProductGenerator

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @staticmethod
    def __safe_connect(do_commit=False):
        """Декоратор для безопасного подключения к БД"""
        def decorator(func):
            def wrapper(instance, *args, **kwargs):
                with sqlite3.connect(Library.__db, timeout=Library.__timeout) as connect:
                    cursor = connect.cursor()
                    res = func(instance, cursor, *args, **kwargs)
                    if do_commit:
                        connect.commit()
                    return res

            wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
            return wrapper
        return decorator

    @classmethod
    def __cache_clearing(cls, full_name: str):
        """Очищаем кэш от изменившихся или удаленных из БД продуктов"""
        print('сработал метод очистки кэша')
        if full_name in cls.__cache:
            del cls.__cache[full_name]

    @__safe_connect()
    def get_product_headers(self, cursor) -> dict:
        """Метод возвращает из базы данных имена всех продуктов.\nФормирует словарь: {тип: (имя1, имя2, ...)}"""
        dct = {}
        for category in self.product_gen.get_categories():
            cursor.execute(f"SELECT full_name FROM {category}")
            dct.update({ProductGenerator.translator(category): tuple(x[0] for x in cursor.fetchall())})
        return dct

    @__safe_connect(True)
    def delete(self, cursor, category: str, full_name: str):
        """
        Метод для удаления продукта из библиотеки.
        :param cursor: Ссылка на объект cursor базы данных
        :param category: Категория продукта / название таблицы
        :param full_name: Имя продукта
        """
        cursor.execute(f'DELETE FROM {self.product_gen.translator(category, True)} WHERE full_name=\'{full_name}\'')
        self.__cache_clearing(full_name)



# if __name__ == '__main__':
#     print(dir(Library))
#     Library._Library__db = f'../{Library._Library__db}'
#     tests.product_test(ProductGenerator)
