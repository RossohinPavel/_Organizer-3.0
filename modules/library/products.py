from dataclasses import dataclass


class Product:
    """Абстракнтый класс - основание для наследования продуктов. Содержит обязательные свойства для продуктов."""

    @property
    def category(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'{self.__class__.__name__} <full_name={self.full_name}>'

    def __iter__(self):
        yield from self.__dict__

    def __contains__(self, item):
        return hasattr(self, item)

    def items(self):
        """Возвращает итератор по атрибутам и их значениям продукта"""
        yield from self.__dict__.items()

    def values(self):
        """Возвращает итератор по значениям продукта"""
        yield from self.__dict__.values()


@dataclass
class Album(Product):
    full_name: str = None               # Полное имя продукта
    segment: str = None                 # Общие особенности продукта
    short_name: str = None
    product_format: str = None
    lamination: str = None
    cover_type: str = None              # Тип сборки обложки
    carton_length: int = None           # Технические размеры обложки
    carton_height: int = None
    cover_clapan: int = None
    cover_joint: int = None
    cover_print_mat: str = None         # Печатный материал
    page_print_mat: str = None
    dc_top_indent: int = None           # Индивидуальные особенности продукта
    dc_left_indent: int = None
    dc_overlap: int = None
    dc_break: int = None


@dataclass
class Canvas(Product):
    full_name: str = None  # Полное имя продукта
    segment: str = None  # Общие особенности продукта
    short_name: str = None
    product_format: str = None
    cover_print_mat: str = None  # Печатный материал


@dataclass
class Journal(Product):
    full_name: str = None               # Полное имя продукта
    segment: str = None                 # Общие особенности продукта
    short_name: str = None
    product_format: str = None
    cover_print_mat: str = None         # Печатный материал
    page_print_mat: str = None


@dataclass
class Layflat(Product):
    full_name: str = None               # Полное имя продукта
    segment: str = None                 # Общие особенности продукта
    short_name: str = None
    product_format: str = None
    book_option: str = None
    lamination: str = None
    cover_type: str = None              # Тип сборки обложки
    carton_length: int = None           # Технические размеры обложки
    carton_height: int = None
    cover_clapan: int = None
    cover_joint: int = None
    cover_print_mat: str = None         # Печатный материал
    page_print_mat: str = None


@dataclass
class Photobook(Product):
    full_name: str = None               # Полное имя продукта
    segment: str = None                 # Общие особенности продукта
    short_name: str = None
    product_format: str = None
    book_option: str = None
    lamination: str = None
    cover_type: str = None              # Тип сборки обложки
    carton_length: int = None           # Технические размеры обложки
    carton_height: int = None
    cover_clapan: int = None
    cover_joint: int = None
    cover_print_mat: str = None         # Печатный материал
    page_print_mat: str = None
    cover_canal: str = None             # Индивидуальные особенности продукта
    page_canal: str = None


@dataclass
class Photofolder(Product):
    full_name: str = None               # Полное имя продукта
    segment: str = None                 # Общие особенности продукта
    short_name: str = None
    product_format: str = None
    lamination: str = None
    carton_length: int = None           # Технические размеры обложки
    carton_height: int = None
    cover_print_mat: str = None         # Печатный материал


@dataclass
class Subproduct(Product):
    full_name: str = None               # Полное имя продукта
    segment: str = None                 # Общие особенности продукта
    short_name: str = None
    cover_print_mat: str = None         # Печатный материал
