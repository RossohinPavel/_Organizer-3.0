from modules.library.properties import *


__all__ = ('Album', 'Canvas', 'Journal', 'Layflat', 'Photobook', 'Photofolder',  'Subproduct')


class Product:
    """Абстракнтый класс - основание для наследования продуктов. Содержит обязательные свойства для продуктов."""
    rus_name = 'Продукт'
    main_prop = (full_name, segment, short_name, cover_print_mat)
    properties = ()

    def __init__(self, default_values: bool = False):
        for prop in (*self.main_prop, *self.properties):
            self.__dict__[prop.__name__] = None if not default_values else prop(self.__class__.__name__)

    @property
    def category(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'{self.__class__.__name__} <full_name = {self.full_name}>'


class Album(Product):
    rus_name = 'Полиграфические альбомы, PUR, FlexBind'
    properties = (product_format, lamination, cover_type, carton_length, carton_height, cover_clapan, cover_joint,
                  page_print_mat, dc_break, dc_overlap, dc_top_indent, dc_left_indent)


class Canvas(Product):
    rus_name = 'Фотохолсты'
    properties = (product_format, )


class Journal(Product):
    rus_name = 'Полиграфические фотожурналы'
    properties = (product_format, page_print_mat)


class Layflat(Product):
    rus_name = 'Полиграфические фотокниги Layflat'
    properties = (product_format, book_option, lamination, cover_type, carton_length, carton_height, cover_clapan,
                  cover_joint, page_print_mat)


class Photobook(Product):
    rus_name = 'Фотокниги на Фотобумаге'
    properties = (product_format, book_option, lamination, cover_type, carton_length, carton_height,
                  cover_clapan, cover_joint, page_print_mat, cover_canal, page_canal)


class Photofolder(Product):
    rus_name = 'Фотопапки'
    properties = (product_format, lamination, carton_length, carton_height)


class Subproduct(Product):
    rus_name = 'Остальное'
