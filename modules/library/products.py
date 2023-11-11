from typing import NamedTuple


__all__ = ('Album', 'Canvas', 'Journal', 'Layflat', 'Photobook', 'Photofolder', 'Subproduct')


class Album(NamedTuple):
    """Полиграфически Альбомы, Pur, FlexBind"""
    full_name: str                # Полное имя продукта
    segment: str                  # Общие особенности продукта  
    short_name: str
    product_format: str
    lamination: str
    cover_type: str               # Тип сборки обложки
    carton_length: int            # Технические размеры обложки
    carton_height: int
    cover_flap: int
    cover_joint: int
    cover_print_mat: str          # Печатный материал
    page_print_mat: str           
    dc_top_indent: int            # Индивидуальные особенности продукта
    dc_left_indent: int
    dc_overlap: int
    dc_break: int

    @property
    def category(self): return self.__class__.__name__


class Canvas(NamedTuple):
    """Фотохолсты"""
    full_name: str                # Полное имя продукта
    segment: str                  # Общие особенности продукта
    short_name: str
    product_format: str
    cover_print_mat: str          # Печатный материал

    @property
    def category(self): return self.__class__.__name__


class Journal(NamedTuple):
    """Полиграфические фотожурналы"""
    full_name: str                # Полное имя продукта
    segment: str                  # Общие особенности продукта
    short_name: str
    product_format: str
    cover_print_mat: str          # Печатный материал
    page_print_mat: str

    @property
    def category(self): return self.__class__.__name__


class Layflat(NamedTuple):
    """Полиграфические фотокниги Layflat"""
    full_name: str                # Полное имя продукта
    segment: str                  # Общие особенности продукта
    short_name: str
    product_format: str
    book_option: str
    lamination: str
    cover_type: str               # Тип сборки обложки
    carton_length: int            # Технические размеры обложки
    carton_height: int
    cover_flap: int
    cover_joint: int
    cover_print_mat: str          # Печатный материал
    page_print_mat: str

    @property
    def category(self): return self.__class__.__name__


class Photobook(NamedTuple):
    """Фотокниги на Фотобумаге"""
    full_name: str                # Полное имя продукта
    segment: str                  # Общие особенности продукта
    short_name: str
    product_format: str           # Общие особенности продукта
    book_option: str
    lamination: str
    cover_type: str               # Тип сборки обложки
    carton_length: int            # Технические размеры обложки
    carton_height: int
    cover_flap: int
    cover_joint: int
    cover_print_mat: str          # Печатный материал
    page_print_mat: str
    cover_canal: str              # Индивидуальные особенности продукта
    page_canal: str

    @property
    def category(self): return self.__class__.__name__


class Photofolder(NamedTuple):
    """Фотопапки"""
    full_name: str                # Полное имя продукта
    segment: str                  # Общие особенности продукта
    short_name: str
    product_format: str           # Общие особенности продукта
    lamination: str
    carton_length: int            # Технические размеры обложки
    carton_height: int
    cover_print_mat: str          # Печатный материал

    @property
    def category(self): return self.__class__.__name__


class Subproduct(NamedTuple):
    """Сувенирная, сопровождающая продукция"""
    full_name: str                # Полное имя продукта
    segment: str                  # Общие особенности продукта
    short_name: str
    cover_print_mat: str          # Печатный материал

    @property
    def category(self): return self.__class__.__name__
