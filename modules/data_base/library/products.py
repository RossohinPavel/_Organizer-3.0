from typing import NamedTuple


__all__ = ('Album', 'Canvas', 'Journal', 'Layflat', 'Photobook', 'Photofolder', 'Subproduct')


class ProductMethods:
    """Класс предоставляющий основные методы для продуктов."""
    __slots__ = ()

    @property
    def category(self): 
        """Возвращает категорию продукта"""
        return self.__class__.__name__


"""
    Последующие классы будут содержать 
    описание атрибутов для каждой категории продукции.
"""


class AlbumAttrs(NamedTuple):
    name: str               # Название продукта
    segment: str            # Общие особенности продукта  
    short_name: str
    product_format: str
    lamination: str
    cover_type: str         # Тип сборки обложки
    carton_length: int      # Технические размеры обложки
    carton_height: int
    cover_flap: int
    cover_joint: int
    cover_print_mat: str    # Печатный материал
    page_print_mat: str           
    dc_top_indent: int      # Индивидуальные особенности продукта
    dc_left_indent: int
    dc_overlap: int
    dc_break: int


class CanvasAttrs(NamedTuple):
    name: str               # Название продукта
    segment: str            # Общие особенности продукта
    short_name: str
    product_format: str
    cover_print_mat: str    # Печатный материал


class JournalAttrs(NamedTuple):
    name: str               # Название продукта
    segment: str            # Общие особенности продукта
    short_name: str
    product_format: str
    cover_print_mat: str    # Печатный материал
    page_print_mat: str


class LayflatAttrs(NamedTuple):
    name: str               # Название продукта
    segment: str            # Общие особенности продукта
    short_name: str
    product_format: str
    book_option: str
    lamination: str
    cover_type: str         # Тип сборки обложки
    carton_length: int      # Технические размеры обложки
    carton_height: int
    cover_flap: int
    cover_joint: int
    cover_print_mat: str    # Печатный материал
    page_print_mat: str


class PhotobookAttrs(NamedTuple):
    name: str               # Название продукта
    segment: str            # Общие особенности продукта
    short_name: str
    product_format: str     # Общие особенности продукта
    book_option: str
    lamination: str
    cover_type: str         # Тип сборки обложки
    carton_length: int      # Технические размеры обложки
    carton_height: int
    cover_flap: int
    cover_joint: int
    cover_print_mat: str    # Печатный материал
    page_print_mat: str
    cover_canal: str        # Индивидуальные особенности продукта
    page_canal: str


class PhotofolderAttrs(NamedTuple):
    name: str               # Название продукта
    segment: str            # Общие особенности продукта
    short_name: str
    product_format: str     # Общие особенности продукта
    lamination: str
    carton_length: int      # Технические размеры обложки
    carton_height: int
    cover_print_mat: str    # Печатный материал


class SubproductAttrs(NamedTuple):
    name: str               # Название продукта
    segment: str            # Общие особенности продукта
    short_name: str
    cover_print_mat: str    # Печатный материал


class Album(AlbumAttrs, ProductMethods):
    """Полиграфические Альбомы, Pur, FlexBind"""
    __slots__ = ()


class Canvas(CanvasAttrs, ProductMethods):
    """Фотохолсты"""
    __slots__ = ()


class Journal(JournalAttrs, ProductMethods):
    """Полиграфические фотожурналы"""
    __slots__ = ()


class Layflat(LayflatAttrs, ProductMethods):
    """Полиграфические фотокниги Layflat"""
    __slots__ = ()


class Photobook(PhotobookAttrs, ProductMethods):
    """Фотокниги на Фотобумаге"""
    __slots__ = ()


class Photofolder(PhotofolderAttrs, ProductMethods):
    """Фотопапки"""
    __slots__ = ()


class Subproduct(SubproductAttrs, ProductMethods):
    """Сувенирная, сопровождающая продукция"""
    __slots__ = ()


# Типизация продуктов
type Categories = Album | Canvas | Journal | Layflat | Photobook | Photofolder | Subproduct
